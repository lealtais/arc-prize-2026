# [TÍTULO DO PAPER] Compositional Test-Time Program Synthesis with Hypothesis Pruning for ARC-AGI-2

**Subtitle**: Um framework neuro-simbólico leve para indução de transformações relacionais em tempo de teste com verificação exata.  
**Track**: ARC-AGI-2 (ou ARC-AGI-3)  
**Submission ID**: `[INSERIR_SEU_SUBMISSION_ID_DO_KAGGLE_AQUI]`  
**Public Notebook Link**: `[INSERIR_LINK_DO_NOTEBOOK_PUBLICO_AQUI]`  
**Limite de Palavras**: Máximo de 1.500 palavras (Este template está estruturado exatamente nos 6 critérios dos juízes).

---

## 1. Abstract & Executive Summary (~150 palavras)
- **Problema**: Modelos puramente baseados em pré-treinamento falham quando confrontados com novas regras composicionais nunca vistas antes no ARC-AGI.
- **Nossa Abordagem**: Propomos uma arquitetura de síntese de programas em tempo de teste (*Test-Time Program Synthesis*) que combina uma linguagem de domínio específico (DSL) geométrica/relacional com indução de mapeamentos invariantes e poda rápida baseada em invariantes de dimensão e objetos.
- **Resultado Principal**: Descrever a pontuação obtida no Leaderboard (`Accuracy`) e o custo computacional reduzido por tarefa.

---

## 2. Theory: Why the Method Works (~300 palavras)
*(Critério do Júri: **Theory** — explicar POR QUE funciona, não apenas como funciona)*
- **Princípio da Descrição Mínima (Minimum Description Length - MDL / Navalha de Occam)**:
  - No ARC, existem infinitas funções $f(X) = Y$ que mapeiam uma entrada em uma saída se memorizarmos pixels. Porém, a função verdadeira que gerou a tarefa possui **baixa complexidade de Kolmogorov** quando expressa em termos de *Core Knowledge priors* (objetos, simetrias, topologia, contagem).
- **Verificação Exata como Filtro de Hipóteses**:
  - Enquanto redes neurais sofrem com erros acumulativos em raciocínio multi-passo, a execução simbólica nos pares de demonstração $(X_{\text{train}}, Y_{\text{train}})$ fornece um sinal de recompensa binário/estrutural livre de alucinação, reduzindo exponencialmente o espaço de hipóteses.

---

## 3. Method & Completeness (~350 palavras)
*(Critério do Júri: **Completeness** — detalhamento completo da arquitetura submetida)*
1. **Extração de Invariantes Estruturais (Perception Layer)**:
   - Análise de mudança de dimensão $(H_{\text{in}}, W_{\text{in}}) \to (H_{\text{out}}, W_{\text{out}})$, preservação de histograma de cores e componentes conexos.
2. **DSL Relacional e Composicional (Program Space)**:
   - Primitivas geométricas (grupo diedral $D_4$: rotações e reflexões), operadores de recorte topológico (`crop_nonzero`, `bounding_box`), e operadores de recoloração relacional.
3. **Busca Guiada por Invariantes (Search & Pruning)**:
   - Em vez de testar todas as composições $f_k \circ \dots \circ f_1$ cegamente, usamos as invariantes observadas nos pares de demonstração para podar subárvores incompatíveis antes da execução.
4. **Seleção Dual (`attempt_1` e `attempt_2`)**:
   - Ranqueamento por consistência exata nos pares de treino + desempate por menor comprimento de programa (MDL).

---

## 4. Novelty & Universality (~250 palavras)
*(Critérios do Júri: **Novelty** e **Universality**)*
- **O que há de novo (Novelty)**:
  - Separação explícita entre *indução geométrica/topológica* e *indução de bijeção cromática tardia* (*Late Color Binding*), permitindo que a busca descubra a estrutura espacial mesmo quando as cores mudam dinamicamente.
- **Por que é Universal (Universality)**:
  - Nenhuma regra foi codificada especificamente para um puzzle individual. O motor de busca opera sobre qualquer domínio de transformação matricial 2D onde exista uma regra funcional entre pares de entrada/saída.

---

## 5. Empirical Analysis, Ablations & Accuracy (~250 palavras)
*(Critério do Júri: **Accuracy**)*
| Configuração do Sistema | Tarefas Resolvidas (Treino/Eval) | Tempo Médio / Tarefa |
| :--- | :---: | :---: |
| Apenas Primitivas Profundidade 1 | X% | ~0.05s |
| + Composição Profundidade 2-3 | Y% | ~0.40s |
| + Late Color Binding + Invariant Pruning | **Z%** | ~0.25s |

- Incluir análise de casos de sucesso e análise honesta dos modos de falha (ex: tarefas que exigem contagem aritmética de longo alcance ou simulação física multi-passo).

---

## 6. Progress Toward AGI (~150 palavras)
*(Critério do Júri: **Progress**)*
- Como essa submissão ajuda qualquer pesquisador a avançar no ARC Prize?
- Demonstra que mesmo um orçamento computacional enxuto consegue resolver transformações composicionais quando acoplamos **poda por invariantes** + **indução simbólica verificável**, servindo como um módulo determinístico que pode ser plugado em qualquer LLM/VLM para eliminar erros de execução espacial.
