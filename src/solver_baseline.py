"""
Baseline Neuro-Simbólico / Program Synthesis para o ARC-AGI-2.
A ideia central:
1. Cada tarefa ARC possui pares de demonstração (train: [(input, output), ...]) e pares de teste (test: [(input, ?)]).
2. Definimos uma biblioteca composicional de primitivas de transformação de grades (DSL).
3. Para cada tarefa nova, realizamos busca em largura/feixe (Beam Search / Program Synthesis) no tempo de teste (Test-Time Adaptation)
   para encontrar programas compostos f(grid) que satisfaçam EXATAMENTE todos os pares de demonstração.
4. Aplicamos os melhores programas encontrados na grade de teste (gerando até 2 tentativas por tarefa, padrão oficial do ARC).
"""

from typing import Callable, Dict, List, Optional, Tuple
import numpy as np

Grid = np.ndarray
TransformFn = Callable[[Grid], Grid]


# =====================================================================
# 1. Primitivas da DSL (Domain-Specific Language) para Grades 2D
# =====================================================================

def identity(g: Grid) -> Grid:
    return g.copy()


def rot90(g: Grid) -> Grid:
    return np.rot90(g, 1)


def rot180(g: Grid) -> Grid:
    return np.rot90(g, 2)


def rot270(g: Grid) -> Grid:
    return np.rot90(g, 3)


def flip_h(g: Grid) -> Grid:
    return np.fliplr(g)


def flip_v(g: Grid) -> Grid:
    return np.flipud(g)


def transpose(g: Grid) -> Grid:
    return g.T.copy()


def crop_nonzero(g: Grid) -> Grid:
    """Recorta o bounding box mínimo dos pixels não-zero (cor != 0)."""
    coords = np.argwhere(g != 0)
    if coords.size == 0:
        return g.copy()
    r0, c0 = coords.min(axis=0)
    r1, c1 = coords.max(axis=0) + 1
    return g[r0:r1, c0:c1].copy()


def invert_binary_colors(g: Grid) -> Grid:
    """Se a grade tiver exatamente 2 cores, inverte uma pela outra."""
    unique = np.unique(g)
    if len(unique) != 2:
        return g.copy()
    out = g.copy()
    c0, c1 = unique[0], unique[1]
    out[g == c0] = c1
    out[g == c1] = c0
    return out


PRIMITIVES: Dict[str, TransformFn] = {
    "identity": identity,
    "rot90": rot90,
    "rot180": rot180,
    "rot270": rot270,
    "flip_h": flip_h,
    "flip_v": flip_v,
    "transpose": transpose,
    "crop_nonzero": crop_nonzero,
    "invert_binary_colors": invert_binary_colors,
}


# =====================================================================
# 2. Aprendizado de Mapeamento de Cores (Color Remapping Induction)
# =====================================================================

def learn_color_map(train_pairs: List[Tuple[Grid, Grid]]) -> Optional[Dict[int, int]]:
    """Verifica se existe uma bijeção/função consistente de cores entre input e output."""
    mapping: Dict[int, int] = {}
    for inp, out in train_pairs:
        if inp.shape != out.shape:
            return None
        for c_in, c_out in zip(inp.flat, out.flat):
            c_in, c_out = int(c_in), int(c_out)
            if c_in in mapping and mapping[c_in] != c_out:
                return None
            mapping[c_in] = c_out
    return mapping


def apply_color_map(g: Grid, mapping: Dict[int, int]) -> Grid:
    out = g.copy()
    for c_in, c_out in mapping.items():
        out[g == c_in] = c_out
    return out


# =====================================================================
# 3. Síntese de Programas por Busca Composicional (Profundidade <= 2)
# =====================================================================

def evaluate_program(
    fn: TransformFn, train_pairs: List[Tuple[Grid, Grid]]
) -> float:
    """Retorna 1.0 se o programa acerta 100% dos exemplos de treino, ou similaridade parcial."""
    scores = []
    for inp, target in train_pairs:
        try:
            pred = fn(inp)
        except Exception:
            return 0.0
        if pred.shape != target.shape:
            scores.append(0.0)
        else:
            scores.append(float(np.mean(pred == target)))
    return float(np.mean(scores))


def synthesize_program(
    train_pairs: List[Tuple[Grid, Grid]]
) -> List[Tuple[str, TransformFn, float]]:
    """
    Busca programas de profundidade 1 e 2 + mapeamento de cor que melhor explicam os pares de treino.
    """
    candidates: List[Tuple[str, TransformFn, float]] = []

    # Profundidade 1
    for name1, fn1 in PRIMITIVES.items():
        score = evaluate_program(fn1, train_pairs)
        candidates.append((name1, fn1, score))

    # Profundidade 2 (composição fn2(fn1(x)))
    for name1, fn1 in PRIMITIVES.items():
        if name1 == "identity":
            continue
        for name2, fn2 in PRIMITIVES.items():
            if name2 == "identity":
                continue
            comp_name = f"{name2}({name1})"
            comp_fn = lambda g, f1=fn1, f2=fn2: f2(f1(g))
            score = evaluate_program(comp_fn, train_pairs)
            candidates.append((comp_name, comp_fn, score))
            if score == 1.0:
                break

    # Teste de mapeamento de cores pós-transformação geométrica
    for name1, fn1 in PRIMITIVES.items():
        transformed_pairs = []
        valid = True
        for inp, out in train_pairs:
            try:
                transformed_pairs.append((fn1(inp), out))
            except Exception:
                valid = False
                break
        if valid:
            cmap = learn_color_map(transformed_pairs)
            if cmap is not None:
                comp_name = f"color_map({name1})"
                comp_fn = lambda g, f1=fn1, cm=cmap: apply_color_map(f1(g), cm)
                score = evaluate_program(comp_fn, train_pairs)
                candidates.append((comp_name, comp_fn, score))

    candidates.sort(key=lambda x: x[2], reverse=True)
    return candidates


def solve_task(task: dict) -> List[List[List[int]]]:
    """
    Recebe um dicionário de task no formato oficial do ARC:
    {'train': [{'input': [[...]], 'output': [[...]]}], 'test': [{'input': [[...]]}]}
    Retorna as 2 melhores predições (attempt_1, attempt_2) para cada item de teste.
    """
    train_pairs = [
        (np.array(p["input"], dtype=int), np.array(p["output"], dtype=int))
        for p in task["train"]
    ]
    ranked = synthesize_program(train_pairs)
    best_fn_1 = ranked[0][1]
    best_fn_2 = ranked[1][1] if len(ranked) > 1 else ranked[0][1]

    predictions = []
    for test_item in task["test"]:
        test_inp = np.array(test_item["input"], dtype=int)
        pred_1 = best_fn_1(test_inp).tolist()
        pred_2 = best_fn_2(test_inp).tolist()
        predictions.append({"attempt_1": pred_1, "attempt_2": pred_2})
    return predictions


if __name__ == "__main__":
    # Exemplo rápido de fumaça: tarefa onde a regra secreta é girar 90 graus + trocar cor 1 por 2
    sample_task = {
        "train": [
            {
                "input": [[1, 0], [1, 1]],
                "output": [[0, 2], [2, 2]],
            },
            {
                "input": [[0, 1], [1, 0]],
                "output": [[2, 0], [0, 2]],
            },
        ],
        "test": [{"input": [[1, 1], [0, 1]]}],
    }
    ranked_programs = synthesize_program(
        [
            (np.array(p["input"]), np.array(p["output"]))
            for p in sample_task["train"]
        ]
    )
    print(f"Melhor programa descoberto: {ranked_programs[0][0]} (score={ranked_programs[0][2]:.2f})")
    preds = solve_task(sample_task)
    print("Predição para o teste (attempt_1):", preds[0]["attempt_1"])
