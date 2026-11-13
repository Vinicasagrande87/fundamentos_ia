# Registro de uso de Inteligência Artificial — AS

**Projeto:** Recomendação de treinos personalizados em academia · **Aluno:** Vinicius Casagrande · Fundamentos de IA — ADS/ULBRA, 2026/2

**Uso de IA no projeto:** Sim
**Ferramentas:** Claude (Anthropic), via Claude Code e Claude web; ChatGPT (OpenAI), nas atividades iniciais.

**Como a IA foi usada, em geral:**
- escrever e executar código (pandas, scikit-learn, matplotlib);
- estruturar e redigir documentos e slides a partir de resultados já produzidos;
- buscar e resumir fontes públicas (Atividade 14);
- servir de tutor para estudar a apresentação.

**Como foi verificado:**
- todo número citado nos documentos sai de um notebook executado no repositório;
- os notebooks foram reexecutados do início ao fim com as versões de `requirements.txt`;
- quando um texto escrito antes da execução contradizia a saída, o texto foi corrigido, e não o número (exemplos na Atividade 15 e na AS, abaixo).

---

## Por atividade

| Atividade | Uso da IA | Produção própria (decisões do estudante) |
|---|---|---|
| 4 — Base de dados | Script de simulação (`gerar_dataset.py`) e notebook de análise exploratória | Variáveis do perfil, critério de geração dos dados, variável-alvo, as 4 categorias de treino |
| 5 — Qualidade dos dados | Código de contagem (ausentes, duplicados, valores únicos, classes), relatório e slides da AP1 | Gravidade de cada problema e identificação do viés de acesso a equipamento |
| 6–8 — Pipeline e limpeza | Código de limpeza e tabela de decisões | Escolha entre alternativas de tratamento e critério de divisão treino/teste |
| 9 — Primeiro modelo | Código de treino e avaliação (matriz de confusão, F1, `export_text`, comparação com a regra) | Justificativa do modelo e a leitura de que o 0,90 reflete a regra sintética, não dados reais |
| 10 — Avaliação | Código de `classification_report`, overfitting, duplicatas, validação cruzada e `balanced`. Slides da AP2 | Recall de Treino D como métrica principal, pelo custo do erro. Tradução dos erros para o domínio |
| 11 — Revisão técnica | Estrutura do documento e do backlog | Pontos fortes e fracos, respostas às perguntas de defesa, prazos do backlog |
| 12 — K-means | Código do agrupamento e do cruzamento com o erro | Interpretação dos grupos e do ponto cego |
| 13 — Rede neural | Código do MLP e da comparação com os mesmos folds | Decisão de manter a árvore |
| 14 — Fitbod | Busca e síntese de fontes públicas | Escolha do Fitbod, hipótese de sistema híbrido, conexão com o projeto |
| 15 — Relatório crítico | Notebook de medição (validação repetida pareada, regra de segurança, subgrupos, remoção da idade), relatório e README | Remover a idade, usar a regra como encaminhamento ao professor (não troca automática), classificar o risco como Médio |
| **AS** | Ver abaixo | Ver abaixo |

## Entrega da AS (Encontros 16–17)

**Uso da IA:**
- montagem e execução do notebook final `AS_ViniciusCasagrande_ADS.ipynb`, que regera a base, reproduz o tratamento e mede todos os modelos nos mesmos folds;
- redação do relatório final, dos slides e deste registro;
- preparação do guia de estudo para a apresentação (não incluído no repositório).

**Achados que surgiram na execução e corrigiram o que estava escrito:**
1. **Rede neural x árvore de profundidade 5.** Sem a idade, a rede neural tinha recall de D bem maior que a árvore de profundidade 5 **fora** da cobertura da regra (0,82 contra 0,60). O argumento anterior, de que os dois modelos "empatavam", deixou de valer.
2. **Profundidade da árvore.** A leitura das regras (`export_text`) mostrou que, com 5 níveis, a árvore não chega à exceção "iniciante de hipertrofia com ≤2 dias". A IA propôs medir outras profundidades. A tabela (§5 do notebook) mostrou que a **profundidade 6** resolve o ramo e supera a rede fora da regra.
3. **Leituras corrigidas depois de ver as saídas:** a ordem das perguntas da árvore e quais subgrupos ficam abaixo da média.

**Decisões do estudante:**
- adotar a árvore `max_depth=6`, sem idade e sem balanceamento, como modelo final, depois de conferir a tabela de profundidades e a comparação com a rede;
- responder ao feedback da Atividade 14 separando as métricas dentro e fora da regra de segurança;
- manter a regra de segurança como encaminhamento ao professor;
- o roteiro e a condução da apresentação.

**Limite assumido:** o que está neste repositório precisa ser defendido por mim nas perguntas da AS. Revisei cada número e cada decisão do relatório antes da entrega.
