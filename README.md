# 🧠 ARC Prize 2026 — Sprint de 4 Dias (Code + Paper Track)

Repositório estruturado para competir no **ARC Prize 2026** (submissão de código no **ARC-AGI-2 / ARC-AGI-3** + artigo técnico no **Paper Track** até **9 de novembro de 2026 às 23:59 UTC**).

---

## 📌 O que é o ARC Prize 2026?

O **ARC (Abstraction and Reasoning Corpus)**, criado por **François Chollet** (criador do Keras), é o benchmark mais famoso do mundo para medir **Inteligência Geral Artificial (AGI)**.

Ao contrário de benchmarks comuns onde a IA decora padrões de milhões de exemplos, no ARC a IA recebe **quebra-cabeças visuais inéditos** (grades coloridas de 1x1 a 30x30 no ARC-AGI-2, ou ambientes interativos no ARC-AGI-3) com apenas **2 a 4 exemplos de demonstração** e precisa descobrir a regra lógica na hora (**Test-Time Adaptation / Síntese de Programas**).

### As 3 frentes da competição:
1. **ARC-AGI-2 (Puzzles Estáticos)**: Grades 2D onde você recebe pares `(input, output)` de treino e precisa prever a grade `output` do teste.
2. **ARC-AGI-3 (Ambientes Interativos - Novo em 2026)**: Agentes que exploram ambientes ocultos em múltiplos passos para descobrir as regras do jogo na hora.
3. **Paper Track (Este desafio - US$ 75.000 + Bônus de US$ 375.000)**:
   - Não é apenas um campeonato de código: é um prêmio para o **melhor artigo técnico (Writeup de até 1.500 palavras)** explicando a solução que você submeteu no ARC-AGI-2 ou ARC-AGI-3.
   - **Importante**: Para ser elegível no Paper Track, você **precisa fazer pelo menos uma submissão válida** no leaderboard do ARC-AGI-2 ou ARC-AGI-3 e anexar seu **Submission ID** + **Notebook Público do Kaggle** + **Imagem de Capa**.

---

## 🏆 Critérios de Avaliação do Paper Track (0 a 5 pontos cada)

Os juízes (incluindo François Chollet e Mike Knoop) avaliam 6 critérios com peso igual:
1. **Accuracy (Precisão)**: Pontuação da sua submissão no leaderboard.
2. **Universality (Universalidade)**: Quão geral é o método (não pode ser um monte de regras feitas à mão só para os puzzles conhecidos).
3. **Progress (Progresso)**: Quanto o seu método ajuda a comunidade a chegar mais perto de resolver o ARC.
4. **Theory (Teoria)**: Explicar **por que** funciona (e não apenas *como* foi programado).
5. **Completeness (Completude)**: Clareza, reprodutibilidade e cobertura completa do código no Notebook público.
6. **Novelty (Novidade)**: Originalidade em relação às pesquisas públicas anteriores (ex: combinar busca em árvore + síntese de programas + refinamento de hipóteses).

---

## ⏱️ Plano de Guerra de 4 Dias (05/Nov a 09/Nov)

- **Dia 1 (Hoje - 05/Nov)**: Setup do repositório, download dos dados via `kagglehub`, escolha da trilha (recomendado: **ARC-AGI-2** pela rapidez de submissão em 4 dias) e primeira submissão baseline no Kaggle para garantir o `Submission ID`.
- **Dia 2 (06/Nov)**: Implementação do método principal (ex: **Neuro-Symbolic Program Synthesis + Test-Time Verification** — geração de regras em DSL/Python e filtragem exata nos exemplos de demonstração).
- **Dia 3 (07/Nov)**: Submissão final do Notebook Público no Kaggle, coleta de métricas, gráficos de ablação e geração da **Cover Image** obrigatória para a Media Gallery.
- **Dia 4 (08-09/Nov)**: Redação e revisão final do **Kaggle Writeup (< 1.500 palavras)** focado nos 6 critérios da banca e clique no botão **Submit** antes das 23:59 UTC (20:59 no horário de Brasília).

---

## 📂 Estrutura do Repositório

```text
arc-prize-2026/
├── data/                       # Dados baixados pelo kagglehub (ignorado no git)
├── notebooks/
│   └── arc_2026_submission.ipynb # Notebook pronto para publicar no Kaggle
├── paper/
│   ├── writeup_template.md     # Template do artigo (< 1.500 palavras) nos 6 critérios
│   └── media/                  # Imagens e diagramas para a Media Gallery do Kaggle
├── src/
│   ├── download_data.py        # Script com kagglehub para baixar os arquivos
│   └── solver_baseline.py      # Motor de busca/síntese de transformações em grades
├── requirements.txt
└── README.md
```

## 🚀 Como começar

```bash
pip install -r requirements.txt
python src/download_data.py
python src/solver_baseline.py
```
