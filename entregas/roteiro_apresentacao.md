# Roteiro de fala — AP1 (≈ 5 minutos)

Dica: grave em blocos, um slide por vez, se ficar mais confortável — depois é só juntar os vídeos. Fale com suas palavras, isso aqui é um guia, não texto para decorar.

---

## Slide 1 — Título (≈15s)

"Meu projeto é um sistema de recomendação de treinos personalizados para academia. Ele sugere exercícios com base em informações que o próprio aluno fornece: saúde, peso e o resultado que ele busca com o treino."

---

## Slide 2 — Problema e justificativa (≈40s)

"O problema que eu escolhi resolver é: como recomendar automaticamente um treino adequado pra um aluno, considerando o perfil dele — idade, objetivo, experiência, disponibilidade e restrições físicas.

Isso é útil tanto para o próprio aluno quanto para professores de educação física, porque montar um treino personalizado pra cada pessoa, na mão, não escala quando você tem muitos alunos.

Por isso faz sentido usar IA aqui: um modelo consegue aprender esse padrão a partir de exemplos e aplicar de forma consistente pra qualquer novo aluno."

---

## Slide 3 — Tipo de problema e soluções semelhantes (≈40s)

"Esse é um problema de classificação supervisionada: a partir de um conjunto de características de entrada — idade, objetivo, nível de experiência, dias disponíveis, restrição física e equipamento — o modelo prevê uma categoria de treino, que é a variável de saída.

Existem soluções parecidas no mercado, como o Fitbod e o BodBot, que também usam objetivo, nível e equipamento para montar treinos. A diferença é que eles ajustam o treino sessão a sessão, de forma individual e contínua. O meu projeto é mais simples: um classificador único, treinado sobre uma base de vários alunos, que recomenda uma categoria de treino a partir do perfil, sem esse ajuste incremental."

---

## Slide 4 — Abordagem escolhida (≈35s)

"A abordagem que escolhi foi Árvore de Decisão. Escolhi essa técnica por dois motivos: primeiro, porque ela é interpretável — dá pra visualizar exatamente as regras que levaram a cada recomendação. Segundo, porque meus dados são majoritariamente categóricos, como objetivo e equipamento disponível, e árvore de decisão lida bem com esse tipo de atributo.

Pensei também em um sistema de regras fixas, mas isso exigiria eu prever manualmente todas as combinações possíveis de seis atributos, o que não escala. A árvore aprende essas combinações direto dos dados e continua sendo explicável."

---

## Slide 5 — Base de dados (≈35s)

"Minha base tem 300 alunos simulados, com 8 colunas — 6 delas são as features de entrada e uma é a variável de saída.

Os dados são sintéticos: eu gerei em Python, com pandas e numpy, a partir de distribuições estatísticas e regras de associação entre o perfil do aluno e o treino recomendado, com 8% de ruído proposital pra simular exceções reais.

É um dataset próprio, de uso livre pra fins acadêmicos. E já está no plano: essa base simulada vai ser substituída por dados reais nos Encontros 5 e 8."

---

## Slide 6 — Dicionário de dados (≈30s)

"Aqui está o dicionário de dados resumido. Seis variáveis de entrada — idade, objetivo, nível de experiência, dias disponíveis, restrição física e equipamento — e uma variável de saída, o treino recomendado, que pode ser Treino A, B, C ou D.

Não vou ler cada linha, mas destaco que boa parte das variáveis é categórica, e que a base atual não tem valores ausentes."

---

## Slide 7 — Análise inicial (≈40s)

"Na análise inicial, a idade média dos alunos é de 29,3 anos, com desvio padrão de quase 8 anos — então tem uma dispersão relevante, de 16 a 51 anos. A disponibilidade média é de 3,4 dias por semana.

Olhando a distribuição do treino recomendado, as quatro categorias ficaram com frequências relativamente próximas — o Treino D é o mais frequente, com 92 alunos, e o Treino B o menos frequente, com 54. Isso é importante porque um bom equilíbrio entre as classes favorece o treinamento do classificador mais pra frente."

---

## Slide 8 — Diagnóstico de qualidade (≈45s)

"Fiz um diagnóstico de qualidade da base. Não há dados ausentes nem duplicados — mas isso é meio artificial, porque a base é sintética. Encontrei inconsistências de nomenclatura, algumas variáveis ordinais registradas como texto, e um ruído de rótulo de 8%, que foi proposital.

Tem também um desbalanceamento leve entre as classes, e um viés que já identifiquei: alunos sem nenhum equipamento disponível, que são cerca de 7% da base, têm quase sempre o mesmo treino recomendado — o Treino D — porque essa foi a regra que usei pra gerar os dados. Isso é um viés de amostragem que preciso ter cuidado quando trocar pela base real.

As ações de tratamento já estão planejadas: troca pela base real nos Encontros 5 e 8, padronização da nomenclatura, e reavaliação se quatro categorias de treino são suficientes."

---

## Slide 9 — Próximos passos (≈30s)

"Como próximos passos: no Encontro 8 eu preparo e trato os dados; no Encontro 9, treino o modelo de árvore de decisão; depois avalio o desempenho com métricas como F1-macro e matriz de confusão, olhando também o desempenho por subgrupo; e por fim, apresento o projeto completo na AP2.

Obrigado! Fico à disposição para perguntas."

---

**Tempo total estimado: ~4min50s a 5min10s** — dentro do limite. Se sobrar tempo, você pode expandir um pouco os slides 2, 7 ou 8, que são os que mais pesam na rubrica (problema/justificativa e diagnóstico de qualidade).
