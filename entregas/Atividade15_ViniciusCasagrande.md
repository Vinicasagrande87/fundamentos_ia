# Atividade 15 — Relatório crítico do projeto

**Projeto:** Recomendação de treinos personalizados em academia · **Aluno:** Vinicius Casagrande · **Encontro 15** · Etapa: entrega final (entrega única)

**Evidência numérica:** todos os números deste relatório saem de `atividade15_academia.ipynb`, executado do início ao fim, com as seções citadas entre parênteses (§). Modelo final: árvore de decisão, `max_depth=5`, `class_weight='balanced'`. Métrica principal: **recall de Treino D**, o treino adaptado para quem não tem equipamento, tem restrição física e é iniciante, ou tem poucos dias.

---

## 1. Principais resultados

Todos os valores são da validação cruzada (k=5, 300 alunos), salvo indicação.

| Resultado | Modelo | Baseline (sempre "Treino D") | O que significa, sem jargão |
|---|---|---|---|
| Acurácia | **0,84** (±0,03) | 0,31 | De cada 100 alunos, o sistema indica para 84 o treino que a regra do projeto considera correto. Chutar sempre o treino mais comum acertaria 31. |
| Recall de Treino D (métrica principal) | **0,76** | 1,00 | De cada 4 alunos que precisam do treino adaptado, 3 o recebem e **1 é mandado para um treino mais intenso do que deveria**. O baseline "acerta" todos porque manda todo mundo para o treino adaptado, e por isso erra 7 de cada 10 alunos no geral. |
| Precisão de Treino D | 0,84 | 0,31 | Quando o sistema indica o treino adaptado, em 84% das vezes era mesmo o caso. Nos outros 16%, o aluno recebe um treino mais leve do que poderia fazer. |
| F1-macro | 0,84 | 0,12 | O desempenho é parecido entre os 4 treinos. Não é um sistema que acerta um treino e ignora os outros. |
| Acurácia no split único (número da AP2) | 0,90 | 0,30 | Foi um sorteio favorável. O mesmo modelo, em 30 divisões treino/teste diferentes, vai de **0,70 a 0,92** (§3). O número confiável é o 0,84. |
| Teto possível nesta base | 0,92 | — | 8% dos rótulos foram trocados de propósito na geração. Nenhum modelo passa de ~92%, e o modelo está a 8 pontos desse teto. |
| Configuração proposta para a AS (sem idade + regra de segurança, §10) | acurácia 0,88 · recall de D **0,89** | 0,31 · 1,00 | Os alunos que precisavam do treino adaptado e não o receberam caem de 22 para 10, em 92. Esse número é otimista (ver limitação 1). |

**Leitura crítica:** o modelo funciona **na base que eu criei**: ele recupera quase toda a regra que usei para gerar os rótulos. Isso não mostra que ele recomendaria bem para alunos reais. Nenhum aluno real foi usado em nenhuma etapa.

## 2. Limitações do modelo

| # | Limitação | Evidência | Impacto prático |
|---|---|---|---|
| 1 | **Base sintética de 300 alunos.** Os rótulos são a minha regra (`recomenda_treino`) mais 8% de ruído. | Teto de 0,92. A regra de segurança só "custa" um aluno porque copia um trecho da regra de geração (§8). | Nenhum número vale para alunos reais. O modelo aprende a minha opinião sobre treino, não a de um profissional. A regra de segurança parece não ter custo porque é circular. |
| 2 | **Instabilidade entre execuções.** | Acurácia de 0,70 a 0,92 em 30 splits (§3). A mesma árvore deu 0,9167 no Colab e 0,90 aqui: 1 aluno de diferença por versão do scikit-learn (§2). | Diferenças menores que ~3 pontos não são distinguíveis. O ganho do `class_weight='balanced'` (0,84 contra 0,8267) **não se confirmou no recall de D**: em 50 folds pareados, ele perde em 10 e ganha em 8 (§4). |
| 3 | **Poucos exemplos das combinações mais delicadas.** | Ponto cego (emagrecimento + restrição + iniciante): 18 alunos, 22% com rótulo ruidoso, colados a 40 vizinhos de Treino B (§7). Exceção da hipertrofia (iniciante com ≤2 dias): **7 alunos, todos errados** (§6). | Os alunos mais vulneráveis, iniciantes com limitação, são justamente onde o modelo mais erra. Um modelo mais complexo não resolve: a rede neural reduziu os erros espalhados (17 contra 25), mas não os do ponto cego (6 contra 7). É falta de evidência, não de capacidade. |
| 4 | **Variáveis importantes ausentes:** grau e tipo da restrição, liberação médica, histórico de lesões, condição cardiovascular, peso, sexo. | "Restrição lombar" é o pior subgrupo: acurácia 0,65 e erro real de 26%, contra 5% sem restrição (§9). | Uma lombalgia leve e uma hérnia recebem o mesmo tratamento. O sistema não sabe quando uma restrição é grave. |
| 5 | **Desbalanceamento leve (1,7:1) não é a causa do recall baixo.** | Balancear não melhorou o recall de D em 50 folds (§4). | Técnicas de balanceamento (pesos, oversampling) não são a alavanca certa neste projeto. A alavanca são dados e regras (§5 e §7). |

## 3. Possíveis vieses (auditoria)

**Quem está e quem ficou de fora.** A base tem pessoas de 16 a 51 anos, 54% iniciantes, no máximo uma restrição por pessoa e só 22 alunos (7%) sem equipamento. **Ficaram de fora:** pessoas com mais de 51 anos, gestantes, pessoas com deficiência ou mais de uma restrição, cardiopatas. Também não há variável de gênero, renda ou etnia. Ou seja, o sistema não tem como saber que está atendendo alguém fora do perfil.

**Métrica principal por subgrupo (recall de D, §9, figura recall_D_subgrupo_atividade15.png):**

| Subgrupo | Recall de D | Comentário |
|---|---|---|
| 25-34 anos | 0,88 | — |
| 16-24 anos / 35+ anos | **0,67 / 0,68** | **A idade não aparece na regra de geração.** Mesmo assim, os mais jovens e os mais velhos são atendidos pior. |
| Restrição lombar | 0,67 (acurácia 0,65) | Pior subgrupo em acurácia. |
| Objetivo hipertrofia | **0,54** | Exceção "iniciante com ≤2 dias" mal aprendida (7 alunos, 7 erros). |
| Base inteira | 0,76 | — |

Com 20 a 40 alunos de Treino D por subgrupo, diferenças de 5 a 10 pontos podem ser ruído. Já as de 20 pontos, como as da idade e da hipertrofia, não são.

**Verificação de proxy.** A idade é um atributo sensível (discriminação etária) e **não deveria influenciar o treino**: a regra que gerou os dados nem a usa. Mesmo assim, a árvore a usa em 6 nós, mesmo com balanceamento, porque cortes de idade separam por acaso rótulos ruidosos do treino (§9). Remover a idade deixa o modelo **igual ou melhor**: a acurácia sobe de 0,835 para 0,844 e o recall de D de 0,76 para 0,78, e a diferença entre as faixas etárias diminui (16-24: 0,67 → 0,74; 35+: 0,68 → 0,72). **Decisão: a idade sai do modelo da AS.** Dois outros cuidados:
- `restricao_fisica` é **dado de saúde**, sensível pela LGPD (art. 5º, II). É necessária para a segurança, mas exige consentimento e não pode ser usada para outro fim.
- `equipamento_disponivel` funciona como **proxy de condição socioeconômica** (treinar em casa sem equipamento). É legítima para escolher o treino, mas quem não tem equipamento tem a menor acurácia (0,77).

**Decisões humanas registradas nos dados.** Os rótulos são decisões **minhas**, escritas como regra, e nunca foram validadas por um profissional de educação física. Exemplo: "na hipertrofia, quem tem restrição vai sempre para o funcional". Se a base fosse trocada por prescrições reais de professores, o modelo herdaria os vieses deles, por exemplo direcionar mulheres para cardio ou pessoas mais velhas para treinos leves sem avaliação. A auditoria por subgrupo precisaria ser refeita.

## 4. Riscos de uso indevido

**Nível de risco: Médio.** A recomendação afeta **saúde** (risco de lesão), mas é uma sugestão de categoria de treino, revisável por um professor e reversível na sessão seguinte. **Passa a Alto** se for usada sem revisão humana, direto para o aluno num app.

- **Custo do erro:** o erro grave é o falso negativo de D. Um iniciante com dor lombar recebe cardio + circuito ou musculação pesada e se machuca. O erro leve é o falso positivo: treino mais leve que o possível, com frustração e risco de abandono.
- **Quem paga:** o aluno, no corpo, e a academia, em responsabilidade e perda de alunos.
- **Pode contestar?** Em parte. A árvore permite mostrar a regra que levou à recomendação (`export_text`), o que um modelo opaco não permitiria. Mas um iniciante raramente sabe que deveria questionar. Por isso a regra de segurança é proposta como **encaminhamento para o professor**, e não como troca automática.

**Cenários de uso indevido:**
1. **Fora do contexto:** uma academia usa o sistema sem professor para todos os alunos novos, inclusive pessoas de 65 anos ou cardiopatas. O modelo nunca viu ninguém acima de 51 anos nem essas condições, e mesmo assim responde com a mesma "certeza", porque sempre devolve uma das 4 categorias.
2. **Confiança excessiva:** divulgar "90% de acerto" (o split único da AP2), quando o número confiável é 84%, e numa base sintética.
3. **Desvio de finalidade:** usar a variável de restrição ou a previsão "Treino D" para marcar alunos como "de risco" e negar matrícula ou encarecer planos.

## 5. Melhorias futuras

| Melhoria | Problema específico que resolve | Evidência / o que medir |
|---|---|---|
| **Remover a idade das features** | Atalho espúrio por idade (Atividade 10), que espalha o erro de forma desigual entre faixas etárias | Já medido: acurácia e recall de D sobem e a diferença por idade diminui (§9). Implementar no modelo final. |
| **Regra de segurança como encaminhamento ao professor:** restrição + iniciante, ou sem equipamento → revisão / Treino D | Ponto cego da Atividade 12 e os 3 alunos sem equipamento que recebem um treino que exige equipamento | No modelo sem idade: recall de D 0,79 → 0,89 e falsos negativos 19 → 10. Altera 9 de 300 previsões, as 9 eram mesmo Treino D, e o recall de A, B e C não muda (§8 e §10). Com dados reais, medir quantos encaminhamentos o professor rejeitaria. |
| **Coletar exemplos reais das combinações raras**, com rótulo dado por profissional: iniciantes com restrição (sobretudo lombar) e iniciantes de hipertrofia com ≤2 dias | Erro de evidência: 18 e 7 alunos, que nenhum modelo mais complexo resolveu (Atividade 13, §7) | Meta: pelo menos ~50 alunos por combinação. Reavaliar o recall de D por subgrupo, e não só o global. |
| **Adicionar grau da restrição e liberação médica** | "Restrição lombar" é o pior subgrupo (erro real de 26%) e hoje não distingue casos leves de graves | Recall de D e erro real dentro de Lombar antes e depois. |
| **Fixar versões (`requirements.txt`) e reportar validação cruzada repetida com comparação pareada** | Instabilidade: a mesma árvore deu 0,9167 no Colab e 0,90 aqui, e o split único varia de 0,70 a 0,92 | `requirements.txt` já criado no repositório. Na AS, toda comparação entre modelos é apresentada como "ganha em X de 50 folds". |

## 6. Estrutura da apresentação da AS (~8 min + 4 min de perguntas)

| Tempo | Tópico | Conteúdo e evidência |
|---|---|---|
| 0:00–0:45 | Problema e público | Recomendar 1 de 4 treinos a partir de 6 dados do aluno. Para professores de academia. |
| 0:45–1:45 | Dados | Base sintética (300 alunos, regra própria + 8% de ruído). Teto de 0,92. Limitação nº 1, dita logo no início. |
| 1:45–3:00 | Resultado contra baseline | 0,84 contra 0,31. Recall de D 0,76: "1 em cada 4 alunos que precisam do treino adaptado não o recebe". Por que o recall de D é a métrica principal. |
| 3:00–4:15 | O que eu testei e descartei | Split único de 0,70 a 0,92. O balanced não melhora o recall de D (8 contra 10 folds). Rede neural: ganho pequeno e ruidoso, decisão de manter a árvore. |
| 4:15–5:30 | O ponto cego e a regra de segurança | Erro de evidência contra erro de capacidade. 18 alunos, 22% de ruído. Sobre o modelo sem idade, a regra altera 9 previsões (todas certas) e o recall de D vai a 0,89, com a ressalva de que a regra é circular. |
| 5:30–6:45 | Auditoria de viés e risco | Idade como proxy (0,67 / 0,88 / 0,68, removida). Lombar. Risco Médio, que vira Alto sem revisão. Cenário de uso indevido. |
| 6:45–7:30 | Limitações e melhorias | As 5 melhorias da tabela, cada uma ligada ao problema. |
| 7:30–8:00 | Conclusão | O que o projeto faz (recupera a regra e mostra onde ela falha) e o que não faz (não foi validado com nenhum aluno real). |
| 8:00–12:00 | Perguntas | Respostas preparadas: por que não usar a rede neural; se 0,84 é melhor que 0,8267; por que a restrição não piora o erro na hipertrofia; o custo da regra de segurança; por que remover a idade se o objetivo é personalizar. |

## 7. README

README reestruturado com: título e descrição em uma frase, problema e público, dados (origem e licença), dicionário de variáveis, **como executar** (Colab e local, com `requirements.txt`), resultados com métricas e baseline, limitações conhecidas, declaração de uso de IA e link para este relatório. O histórico das atividades 1 a 15 foi mantido abaixo dessas seções.
