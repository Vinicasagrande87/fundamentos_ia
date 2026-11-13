# Relatório final do projeto — AS

**Projeto:** Recomendação de treinos personalizados em academia · **Aluno:** Vinicius Casagrande · **Disciplina:** Fundamentos de Inteligência Artificial — ADS/ULBRA, 2026/2 · **Apresentação:** 19/11/2026 (Encontro 17)

**Repositório:** https://github.com/Vinicasagrande87/fundamentos_ia · **Notebook final:** `AS_ViniciusCasagrande_ADS.ipynb`, executado do início ao fim. Todos os números deste relatório saem dele, com a seção citada como (§). **Uso de IA:** `entregas/AS_ViniciusCasagrande_ADS_UsoDeIA.md`.

Este relatório é a evolução do relatório crítico da Atividade 15 (`entregas/Atividade15_ViniciusCasagrande.md`, mantido como foi entregue). O que mudou desde então está na seção 3.

---

## 1. Problema, público e evolução

**Problema.** Na matrícula, o professor precisa escolher o treino inicial do aluno cruzando objetivo, experiência, dias disponíveis, restrição física e equipamento. O sistema sugere 1 de 4 categorias (A: musculação, B: cardio + circuito, C: funcional, D: peso corporal adaptado) a partir desses dados. É o **ponto de partida** do aluno, não a progressão semana a semana.

**Público.** Professores de educação física, que recebem a sugestão e decidem. O afetado é o aluno.

**Por que importa.** O erro caro é o aluno que precisava do treino adaptado (Treino D) receber um treino mais exigente. Na prática, é um iniciante com dor lombar fazendo musculação pesada: risco de lesão e de desistência no primeiro mês. Por isso a métrica principal é o **recall de Treino D**: de cada 100 alunos que precisavam do treino adaptado, quantos o receberam.

**O que mudou no entendimento do problema desde a AP2:**

| Na AP2 eu dizia | Hoje eu digo, com medição |
|---|---|
| "O modelo acerta 90%." | Esse 0,90 foi um sorteio favorável de um único split. O número de referência é a média da validação cruzada repetida, **0,86**, e o mesmo modelo varia de 0,80 a 0,95 conforme o sorteio (§7). |
| "O `balanced` melhora o recall de D." | Não melhora: em 50 folds pareados, ganha em 8 e perde em 10 (Atividade 15). Saiu do modelo. |
| A idade era só mais uma variável. | A idade era um **atalho espúrio**: a regra real não a usa, e ela fazia o modelo atender pior os mais jovens e os mais velhos. Saiu do modelo (§10). |
| A pergunta era "qual modelo acerta mais?". | A pergunta é **onde o modelo erra, com quem, e o que o professor precisa revisar**. |

A evolução também é conceitual. O projeto deixou de "prever o treino" e passou a ser um **sistema de apoio**: o modelo sugere, uma regra de segurança encaminha os casos de risco ao professor, e cada métrica é reportada separando o que o modelo decide do que a regra decide.

## 2. Dados, preparação e diagnóstico

**Origem e condições.** A base tem 300 alunos **sintéticos**: nenhum aluno real, nenhuma medição. O script `gerar_dataset.py` (seed 1053) gera o perfil com distribuições que escolhi para parecer uma academia típica (Atividade 4). O rótulo vem de uma **regra escrita por mim** (`recomenda_treino`), e depois 8% dos rótulos (24 alunos) são trocados ao acaso para simular exceções. O notebook final **regera a base do zero** e confirma que ela é idêntica ao CSV do repositório (§2).

**Tratamento (Atividade 8, reproduzido no §3).** Três passos determinísticos, sem nada aprendido dos dados, então sem risco de vazamento antes do split:
1. `aluno_id` sai das features, para o modelo não decorar IDs.
2. O texto é padronizado, corrigindo a inconsistência de grafia apontada no diagnóstico da Atividade 5.
3. Nível e equipamento viram categorias ordenadas.

**Diagnóstico:**

| Problema | Achado | Efeito no resultado |
|---|---|---|
| Valores ausentes | Nenhum | Nada foi imputado ou inventado |
| Desbalanceamento | Moderado: D 31%, B 18% | Um chute fixo já acerta 31%, e esse é o baseline |
| Ruído de rótulo | 24 de 300 (8%) | **Teto de ~0,92** para qualquer modelo |
| Ruído desigual | 12% nos iniciantes, 4% nos intermediários | O ruído cai mais no grupo de maior risco (§10) |
| Combinações raras | Algumas células têm 5 a 20 alunos | É nelas que o modelo erra: a limitação da base vira limitação do modelo |

## 3. Modelo, treinamento e justificativa

**Modelo final:** árvore de decisão com `max_depth=6`, **sem a variável idade** e sem balanceamento, usando 14 features one-hot (objetivo, nível, restrição, equipamento e dias). Em volta dela há uma **regra de segurança**: alunos com restrição física e iniciantes, ou sem equipamento, vão para **revisão do professor**, com sugestão de Treino D (§8).

**O que foi tentado antes, medido do mesmo jeito (validação cruzada 5 folds repetida 10 vezes, §5):**

| Modelo | Acurácia | Recall de D | Recall de D **fora da regra** | Decisão |
|---|---|---|---|---|
| Baseline (sempre o mais frequente) | 0,31 | 1,00 | 1,00 | Referência. Manda todo mundo para D |
| Árvore d=5, com idade (AP2) | 0,83 | 0,77 | 0,59 | Substituída |
| Árvore d=5 balanced, com idade (Atividade 15) | 0,84 | 0,76 | 0,60 | Substituída |
| Árvore d=5 balanced, sem idade (proposta da Atividade 15) | 0,84 | 0,78 | 0,60 | Substituída |
| Rede neural MLP (16 neurônios), sem idade | 0,86 | 0,86 | 0,82 | Descartada (ver abaixo) |
| **Árvore d=6, sem idade (final)** | **0,86** | **0,84** | **0,89** | **Escolhida** |

**Por que a profundidade passou de 5 para 6: foi a explicabilidade que mostrou.**
- Lendo as regras da árvore de profundidade 5, o ramo *hipertrofia → sem restrição → com equipamento* terminava em Treino A para todos.
- A regra real tem uma exceção: **iniciante com até 2 dias vai para D**. Para chegar a essa pergunta, a árvore precisa de 6 níveis.
- Com 5 níveis, esses alunos sempre recebiam musculação. Era um erro de **capacidade**, e por isso a rede neural acertava esses casos.
- Na varredura de profundidades (4 a sem limite, §5), a acurácia quase não muda (0,84 a 0,86). O recall de D fora da regra pula de 0,68 para **0,89** na profundidade 6. De 7 em diante, não melhora mais e a acurácia cai: a árvore começa a decorar ruído.

**Por que a árvore e não a rede neural.**
- **Acurácia:** empatam (5 vitórias, 2 empates e 3 derrotas em 10 repetições).
- **Recall de D na base inteira:** a rede é um pouco melhor (+0,02), mas essa vantagem está **dentro** da cobertura da regra, onde quem decide é o professor.
- **Fora da regra:** a árvore ganha **nas 10 repetições** (+0,07).
- **Explicabilidade:** a árvore mostra as regras que usou. O problema da profundidade só foi encontrado porque as regras eram legíveis. Numa rede neural, ele não apareceria.

**Suposições do algoritmo.**
- A árvore supõe que a resposta se descreve por **cortes sucessivos, uma variável por vez**. Vale aqui, porque a regra real é uma sequência de "se... então".
- Ela não supõe escala nem normalidade, então não é preciso normalizar.
- A suposição que **falha** é ter exemplos suficientes em cada folha. Duas folhas da árvore final se ajustaram a rótulos ruidosos (§9). A acurácia no treino (0,93) passa um pouco do teto de 0,92: é um overfitting leve, que fica contido pela regra de segurança.

**Treinamento.**
- **Avaliação:** split 80/20 estratificado (`random_state=42`, o mesmo da AP2, para continuidade) e, como número de referência, validação cruzada estratificada 5 folds repetida 10 vezes.
- **Comparação justa:** todos os modelos são avaliados nos **mesmos** folds, e uma comparação diz "ganha em X de 10 repetições", não "a média é maior".
- **Versões:** fixadas em `requirements.txt`.

## 4. Resultados, baseline e interpretação

**Resultado principal (média de 10×5 validações cruzadas):**

| Métrica | Modelo final | Baseline | Em linguagem simples |
|---|---|---|---|
| Acurácia | **0,86** | 0,31 | De cada 100 alunos, 86 recebem o treino que a regra considera correto. O chute fixo acerta 31. |
| Recall de Treino D (principal) | **0,84** | 1,00 | De cada 100 alunos que precisam do treino adaptado, 84 o recebem. O baseline "acerta" todos porque manda **todo mundo** para o treino adaptado, e por isso erra 7 de cada 10 alunos no geral. |
| Precisão de Treino D | 0,85 | 0,31 | Quando o sistema sugere o treino adaptado, 85% das vezes era o caso. Nos outros, o aluno recebe um treino mais leve do que poderia. |
| Teto possível | 0,92 | — | O modelo está a 6 pontos do máximo que esta base permite. |

**Para onde vão os erros caros** (uma rodada de validação cruzada, matriz `matriz_confusao_final.png`, §6):
- Dos 92 alunos que precisavam de D, **17** receberam outro treino: 8 foram para musculação (A), 5 para cardio + circuito (B) e 4 para funcional (C).
- O erro mais perigoso é o de musculação, porque coloca carga em quem precisava de adaptação.

**O que cada erro significa na academia.**
- **Precisava de D e recebeu A/B/C:** risco de lesão. É o erro **alto**.
- **Recebeu D sem precisar:** treino leve demais. É o erro **baixo**, que o professor ajusta na primeira semana.
- **Troca entre A, B e C:** progresso mais lento. É o erro **médio**.

**A regra de segurança muda o que as métricas medem (resposta ao feedback da Atividade 14).**
- A regra copia um trecho da regra que **gerou os rótulos**: nos 72 alunos que ela cobre, a regra de geração manda D para **todos**.
- Dentro da cobertura, a regra acerta **por construção**. Se eu somasse esse acerto ao do modelo, o recall de D do sistema (0,95) mediria a regra concordando consigo mesma.
- Por isso, separo:

| Recorte (uma rodada de validação cruzada, §8) | Alunos | Alunos D | Recall de D | Falsos negativos de D |
|---|---|---|---|---|
| **Fora da cobertura: o modelo decide (métrica do modelo)** | 228 | 30 | **0,83** | 5 |
| Dentro da cobertura: o que a árvore faria sozinha | 72 | 62 | 0,81 | 12 |
| Dentro da cobertura: a regra (circular nesta base) | 72 | 62 | 1,00 | 0 |
| **Custo da regra:** alunos enviados à fila do professor | **72 (24%)** | — | — | — |

O número que reporto como desempenho do **modelo** é o de fora da cobertura. O ganho da regra só pode ser medido com alunos reais, contra a decisão do professor. A cobertura é um **custo**: 1 em cada 4 alunos vai para revisão, e isso precisa caber na rotina da academia.

## 5. Explicabilidade, vieses e riscos

**Explicabilidade (§9).** As regras da árvore final foram impressas com `export_text`:
- **Variáveis.** As 6 features mais importantes correspondem exatamente às 5 variáveis da regra real: restrição, objetivo, nível, dias e equipamento. **Nenhum nó usa idade.**
- **O ramo corrigido.** Em hipertrofia sem restrição com ≤2 dias, a árvore agora pergunta "é iniciante?".
- **Duas folhas perigosas.** A leitura das regras encontrou *hipertrofia + restrição no joelho + iniciante + ≤2 dias → Treino A* e *condicionamento + restrição + iniciante + ≤2 dias → Treino A*. São **iniciantes com restrição recebendo treino de carga**: folhas com poucos alunos que se ajustaram a rótulos ruidosos.
- **A regra contém essas folhas.** Os dois perfis estão dentro da cobertura da regra de segurança e nunca recebem a previsão automática. É o argumento mais concreto para a regra existir.

**Auditoria de viés por subgrupo (recall de D, §10, figura `recall_D_subgrupo_final.png`):**

| Subgrupo | Atividade 15 (d=5, com idade) | Modelo final | Leitura |
|---|---|---|---|
| 16-24 / 25-34 / 35+ anos | 0,67 / 0,88 / 0,68 | **0,82 / 0,83 / 0,80** | A diferença por idade praticamente desapareceu |
| Hipertrofia | 0,54 | **0,82** | Efeito da profundidade 6 |
| Restrição lombar | 0,67 | **0,62** (acurácia 0,65) | **Pior grupo do modelo final** |
| Intermediários / avançados com D | 0,63 / 0,80 | 0,75 / 0,60 | Poucos alunos (16 e 5), mas abaixo da média |
| Emagrecimento | 0,84 | 0,78 | Piorou: emagrecimento com ≤2 dias fora da regra |
| Base inteira | 0,76 | 0,82 | — |

Mudaram duas coisas ao mesmo tempo (sair a idade e aprofundar a árvore). A seção 5 do notebook isola o efeito da profundidade.

- **Quem está representado.** Pessoas de 16 a 51 anos, no máximo uma restrição por pessoa e sem grau de gravidade. **Ficaram de fora:** maiores de 51 anos, gestantes, cardiopatas, pessoas com deficiência ou com mais de uma restrição. O sistema não tem como saber que está atendendo alguém fora desse perfil.
- **Verificação de proxy.**
  - `idade` era um atalho espúrio e foi removida.
  - `restricao_fisica` é **dado de saúde**, sensível pela LGPD (art. 5º, II). Ela é necessária para a segurança, mas exige consentimento e não pode ter outro uso.
  - `equipamento_disponivel` funciona como **proxy socioeconômico**: indica quem treina em casa sem equipamento.
- **Consequência real.** Quem continua mal atendido é o aluno com **restrição lombar que não é iniciante**, porque a regra de segurança não o cobre. É exatamente um perfil com risco de lesão.
- **Decisões humanas nos dados.** Os rótulos são **decisões minhas**, nunca validadas por um profissional. Com prescrições reais de professores, o modelo herdaria os vieses deles, e a auditoria precisaria ser refeita.

**Risco: Médio.** O sistema mexe com saúde, mas cada sugestão é revisável por um professor e reversível na sessão seguinte. **Vira Alto** se for usado sem revisão humana, como um app direto ao aluno.

**Cenário de uso indevido.** Uma academia usa a saída como prescrição automática para economizar o tempo dos professores, inclusive para pessoas de 65 anos ou cardiopatas. O modelo nunca viu esses perfis e responde com a mesma "certeza". Outros desvios possíveis:
- divulgar "90% de acerto", o número da AP2;
- usar a previsão "Treino D" para marcar alunos como "de risco" e encarecer planos.

**Mitigação:** a saída é sempre uma sugestão, e os casos de risco vão para a fila de revisão.

## 6. Limitações e próximos passos

**Limitações.**
1. **Base sintética.** O modelo recupera a minha regra mais o ruído. Nada foi validado com alunos reais.
2. **Uma pergunta mais fácil que a de um app real** (pergunta do feedback da Atividade 14).
   - O projeto decide só o ponto de partida, a partir de um perfil estático.
   - Por isso não sofre do problema de "precisar de 10 a 15 treinos registrados", mas também **não sabe se a recomendação funcionou** (aderência, dor, evolução).
   - Ele cobre o primeiro dia, que apps como o Fitbod fazem mal. Não substitui a progressão.
3. **300 alunos.** O split único varia de 0,80 a 0,95 (§7). Diferenças de 1 a 2 pontos entre modelos só valem se aparecerem na comparação pareada.
4. **Faltam variáveis:** grau da restrição, liberação médica, histórico de lesões.
5. **O custo real da regra de segurança é desconhecido.** Nesta base ele é zero por construção.

**Próximos passos.**

| Passo | Problema que resolve | O que medir |
|---|---|---|
| Dados reais com consentimento, com a decisão do professor como rótulo | Limitação 1 | Recall de D por subgrupo, não só o global |
| Estender a regra para "restrição lombar, qualquer nível" | Pior subgrupo do modelo final | Quantos alunos a mais vão para a fila, e quantos encaminhamentos o professor rejeita |
| Adicionar grau da restrição e liberação médica | "Lombar" mistura casos leves e graves | Recall de D dentro de Lombar, antes e depois |
| Registrar a aderência nas primeiras semanas | Limitação 2 | Quantos alunos de cada treino continuam após 4 semanas |

## 7. Documentação e reprodutibilidade

- **Notebook final:** `AS_ViniciusCasagrande_ADS.ipynb`.
  - Roda do início ao fim sem depender dos notebooks anteriores.
  - Regera a base, reproduz o tratamento e confere os dois contra os CSVs do repositório.
  - No Colab, a primeira célula clona o repositório.
  - Localmente: `pip install -r requirements.txt` e depois `jupyter nbconvert --to notebook --execute AS_ViniciusCasagrande_ADS.ipynb`.
- **Base:** `dataset_academia.csv` (bruta) e `dataset_academia_tratado.csv`, ou `python gerar_dataset.py 1053` para regerar.
- **Histórico das decisões:** README (seções 1 a 16) e notebooks `atividade4` a `atividade15`.
- **Limitação de reprodutibilidade conhecida:** com outra versão do scikit-learn, o split único pode variar em 1 aluno (Atividade 15). A validação cruzada repetida não muda.
