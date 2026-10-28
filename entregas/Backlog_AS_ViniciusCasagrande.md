# Backlog da AS — Projeto Recomendação de Treinos Personalizados em Academia

Atualizado na Atividade 11 (Revisão técnica da AP2), com base nas investigações feitas na entrega final da Atividade 10 (`atividade10_academia.ipynb`, seções 13 a 15) e nas duas perguntas de defesa deixadas pela professora no feedback da Atividade 10. Atualizado de novo na Atividade 12 (agrupamento K-means cruzado com o erro do modelo, `atividade12_academia.ipynb`).

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

## A fazer — rumo ao Encontro 17 (AS)

| Item | Descrição | Status | Encontro |
|---|---|---|---|
| Validação cruzada com `class_weight='balanced'` | Repetir a validação cruzada k=5 com o balanceamento ativado, comparar média/desvio com os 0,8267 ± 0,0291 do modelo original, para confirmar se a melhora observada no split único é real e estável | A fazer | 12 |
| Promover `class_weight='balanced'` a padrão | Se confirmado no item anterior, substituir o modelo nas seções 1–11 do notebook e reexecutar toda a avaliação (matriz de confusão, métricas por classe, comparação com baseline) com essa configuração | A fazer | 12-13 |
| Testar profundidade maior e Random Forest | Treinar árvore com `max_depth=7` e um `RandomForestClassifier`, comparar `feature_importances_` com a árvore atual, verificar se o atalho por idade identificado na seção 15 persiste | A fazer | 13-14 |
| Reportar validação cruzada como número de referência | Atualizar slides e relatórios para apresentar "~0,83 (validação cruzada, desvio 0,03)" como o número principal, não o 0,90 do split único isolado | A fazer | 12 |
| Feature de interação restrição × iniciante | Criar `restricao_e_iniciante` e testá-la junto com `class_weight='balanced'` (validação cruzada), reportando o erro por grupo do K-means da Atividade 12, não só a acurácia global | A fazer | 13-14 |
| Regra de segurança sobre a saída do modelo | Avaliar uma regra fixa acima da árvore: aluno com restrição física e iniciante → Treino D (ou revisão do professor), medindo quanto o recall de Treino D sobe e quanto custa em falsos positivos | A fazer | 13-14 |
| Avaliar troca da base sintética por dados reais (ou redução do ruído proposital) | Discutir se o teto de ~8% de ruído de rótulo limita demais qualquer métrica, e se vale a pena buscar dados reais de alunos de academia | A fazer | 13-14 |
| Notebook final executável de ponta a ponta | Com a configuração definitiva do modelo (resultado dos itens acima), executado do início ao fim sem erros, com todas as saídas e figuras visíveis | A fazer | 15 |
| README completo | Com instruções de execução atualizadas, referenciando todos os artefatos finais do projeto | A fazer | 15 |
| Relatório final do projeto | Documento consolidado com todo o histórico do projeto, da proposta (AP1) ao modelo final | A fazer | 16 |
| Análise ética e crítica | Aprofundar o viés de acesso a equipamento já identificado no diagnóstico de qualidade (Atividade 5), o ponto cego em alunos com restrição física fora da hipertrofia (Atividade 12) e a limitação de usar base sintética em vez de dados reais | A fazer | 16 |
| Evidências de execução | Notebook exportado com saídas visíveis, capturas de tela organizadas no repositório, comprovando a execução do pipeline completo | A fazer | 16 |
| Registro final de limitações e melhorias futuras | Consolidar esta revisão técnica (Atividade 11) e os resultados dos itens acima num registro único para a AS | A fazer | 17 |

## Perguntas de defesa pendentes (respondidas na Atividade 11, a confirmar na AS)

1. **Em que situação `class_weight='balanced'` pioraria o resultado?** Quando a classe majoritária já é difícil de acertar e perde peso relativo — os novos erros na maioria pesariam mais do que os ganhos nas minorias. Também é possível que a melhora observada seja específica do split atual (`random_state=42`), não se repetindo em todos os folds da validação cruzada — é exatamente o que o item "Validação cruzada com class_weight='balanced'" vai verificar.
2. **Com 3.000 registros em vez de 300, o que aconteceria com o desvio padrão de 0,0291 da validação cruzada?** O erro padrão de uma média cai aproximadamente na proporção de 1 sobre a raiz quadrada do tamanho da amostra; 10x mais dados tenderiam a reduzir o desvio para a ordem de ~0,009. Isso confirma que a instabilidade observada é sintoma de uma base pequena, e que a média da validação cruzada (~0,83) é uma estimativa mais confiável do que qualquer split único.
