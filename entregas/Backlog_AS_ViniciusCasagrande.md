# Backlog da AS — Projeto Recomendação de Treinos Personalizados em Academia

Atualizado na Atividade 11 (Revisão técnica da AP2), com base nas investigações feitas na entrega final da Atividade 10 (`atividade10_academia.ipynb`, seções 13 a 15) e nas duas perguntas de defesa deixadas pela professora no feedback da Atividade 10. Atualizado de novo na Atividade 12 (agrupamento K-means cruzado com o erro do modelo, `atividade12_academia.ipynb`) e na Atividade 13 (rede neural x árvore, `atividade13_academia.ipynb`).

## Concluído

- [x] Treinar baseline e primeiro modelo (Atividade 9)
- [x] Matriz de confusão, F1 por classe e verificação de vazamento (Atividade 9)
- [x] Métrica principal escolhida e justificada pelo custo do erro — recall de Treino D (Atividade 10)
- [x] Teste de overfitting treino vs. teste — sem sinal de memorização (Atividade 10)
- [x] Verificação de duplicatas entre treino e teste e de ordem cronológica (Atividade 10)
- [x] Validação cruzada (k=5) do modelo original — média 0,8267, desvio padrão 0,0291, fold mais fraco 0,7833 (Atividade 10, seção 13)
- [x] Teste de `class_weight='balanced'` no split único — recall de Treino D 0,7778 → 0,8333; acurácia 0,90 → 0,9167; nenhuma classe piorou (Atividade 10, seção 14)
- [x] Comparação das regras da árvore (`export_text`) com a regra de geração (`recomenda_treino`) — identificado atalho espúrio por idade em pelo menos 2 dos 4 falsos negativos de Treino D (Atividade 10, seção 15)
- [x] Slides finais da AP2 consolidados (`entregas/AP2_Final_ViniciusCasagrande.pptx`)
- [x] Revisão técnica pós-AP2 com pontos fortes, fracos, hipóteses de causa e melhorias (Atividade 11)
- [x] Agrupamento K-means (k=4) dos alunos cruzado com o erro do modelo na validação cruzada — ponto cego localizado no grupo "Emagrecimento com limitação física" (36 alunos, 39% de erro contra 17% na média; 7 dos 9 erros reais são falsos negativos de Treino D de iniciantes com restrição) (Atividade 12)
- [x] Validação cruzada (k=5) com `class_weight='balanced'` — acurácia 0,84 ± 0,0291 (contra 0,8267 do modelo original), recall de Treino D 0,7637 (contra 0,7310): melhora aparente (Atividade 13). **Revisto na Atividade 15:** na comparação pareada de 50 folds, o balanced não melhora o recall de D (ganha em 8, perde em 10)
- [x] Rede neural (MLPClassifier, 1 camada de 16 neurônios ReLU) comparada com a árvore na mesma divisão e nos mesmos folds — empate na validação cruzada (0,83), derrota no split único (0,87 contra 0,90), overfitting maior e o ponto cego da Atividade 12 continua. **Decisão: não usar rede neural no projeto final**, manter a árvore (Atividade 13)
- [x] **Atividade 15** (`atividade15_academia.ipynb`): validação cruzada repetida (10×5) com comparação pareada. O balanced ganha na acurácia em 22, empata em 22 e perde em 6 de 50 folds, mas **não melhora o recall de D**. O ganho de recall de D da rede é de +0,05 (ganha em 30 de 50 folds, pequeno e ruidoso). A regra de segurança altera 8 previsões, 7 certas, sem custo em A, B e C. A hipertrofia tem todo o seu erro real nos 7 alunos da exceção "iniciante com ≤2 dias". A idade é um atalho espúrio, e removê-la melhora o modelo. README reestruturado e relatório crítico final.

## A fazer — rumo ao Encontro 17 (AS)

> Atualização da Atividade 15: os itens "Reportar validação cruzada como número de referência", "Regra de segurança" (medição) e "README completo" foram feitos. Itens novos: **remover `idade` das features** e **aplicar a regra de segurança como encaminhamento ao professor** no modelo final, reexecutando a avaliação completa (Encontro 16).

| Item | Descrição | Status | Encontro |
|---|---|---|---|
| ~~Promover `class_weight='balanced'` a padrão~~ | Substituído: a Atividade 15 mostrou que o balanced não melhora o recall de D. O modelo da AS passa a ser a árvore sem `idade` + regra de segurança como encaminhamento ao professor (item novo da nota acima) | Substituído | 15 |
| Testar profundidade maior e Random Forest | Varredura de profundidade 4 a sem limite: **`max_depth=6`** resolve o ramo "iniciante de hipertrofia com ≤2 dias" (recall de D fora da regra 0,60 → 0,89) e passa a ser o modelo final. Random Forest não foi testada | Feito em parte (AS) | 16 |
| Reportar validação cruzada como número de referência | Atualizar slides e relatórios para apresentar "~0,83 (validação cruzada, desvio 0,03)" como o número principal, não o 0,90 do split único isolado | Feito (Atividade 15) | 12 |
| Feature de interação restrição × iniciante | Criar `restricao_e_iniciante` e testá-la junto com `class_weight='balanced'` (validação cruzada), reportando o erro por grupo do K-means da Atividade 12, não só a acurácia global | A fazer | 13-14 |
| Regra de segurança sobre a saída do modelo | Avaliar uma regra fixa acima da árvore: aluno com restrição física e iniciante → Treino D (ou revisão do professor), medindo quanto o recall de Treino D sobe e quanto custa em falsos positivos | Feito (Atividade 15) | 13-14 |
| Avaliar troca da base sintética por dados reais (ou redução do ruído proposital) | Discutir se o teto de ~8% de ruído de rótulo limita demais qualquer métrica, e se vale a pena buscar dados reais de alunos de academia | A fazer | 13-14 |
| Notebook final executável de ponta a ponta | `AS_ViniciusCasagrande_ADS.ipynb`: regera a base, reproduz o tratamento, executado do início ao fim sem erros | Feito (AS) | 16 |
| README completo | Com instruções de execução atualizadas, referenciando todos os artefatos finais do projeto | Feito (Atividade 15) | 15 |
| Relatório final do projeto | `entregas/AS_ViniciusCasagrande_ADS_Relatorio.md` / `.pdf` | Feito (AS) | 16 |
| Análise ética e crítica | Auditoria por subgrupo com o modelo final (notebook §10), proxies (idade, saúde/LGPD, equipamento), risco e uso indevido (relatório §5) | Feito (AS) | 16 |
| Evidências de execução | Notebook final com todas as saídas visíveis e figuras salvas (`matriz_confusao_final.png`, `recall_D_subgrupo_final.png`) | Feito (AS) | 16 |
| Registro final de limitações e melhorias futuras | Relatório final §6 e notebook §11 | Feito (AS) | 16 |

## Perguntas de defesa pendentes (respondidas na Atividade 11, a confirmar na AS)

1. **Em que situação `class_weight='balanced'` pioraria o resultado?** Quando a classe majoritária já é difícil de acertar e perde peso relativo — os novos erros na maioria pesariam mais do que os ganhos nas minorias. Também é possível que a melhora observada seja específica do split atual (`random_state=42`), não se repetindo em todos os folds da validação cruzada — é exatamente o que o item "Validação cruzada com class_weight='balanced'" vai verificar.
2. **Com 3.000 registros em vez de 300, o que aconteceria com o desvio padrão de 0,0291 da validação cruzada?** O erro padrão de uma média cai aproximadamente na proporção de 1 sobre a raiz quadrada do tamanho da amostra; 10x mais dados tenderiam a reduzir o desvio para a ordem de ~0,009. Isso confirma que a instabilidade observada é sintoma de uma base pequena, e que a média da validação cruzada (~0,83) é uma estimativa mais confiável do que qualquer split único.
