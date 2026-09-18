# Projeto: Recomendação de Treinos Personalizados em Academia

Projeto desenvolvido na disciplina **Fundamentos de Inteligência Artificial — ADS/ULBRA**, construído de forma incremental ao longo do semestre.

---

## 1. Contexto e definição do problema

**Domínio:** Academia — recomendação de treinos e exercícios personalizados.

**Descrição do problema:** o projeto busca recomendar automaticamente uma categoria de treino adequada para um aluno de academia, a partir do seu perfil (idade, objetivo, nível de experiência, dias disponíveis por semana, restrições físicas e equipamento disponível).

**Público / contexto de aplicação:** alunos de academia e profissionais de educação física que precisam montar ou sugerir treinos de forma mais rápida e personalizada.

**Justificativa (por que IA):** montar um treino adequado depende de cruzar várias variáveis do aluno ao mesmo tempo (objetivo, experiência, disponibilidade, limitações físicas), o que é trabalhoso de fazer manualmente para um grande número de alunos. Um modelo de IA pode aprender esse padrão a partir de exemplos e sugerir a recomendação de forma consistente e escalável.

> *(Ajuste este bloco se o texto final da Atividade 1 tiver alguma redação diferente da que você entregou.)*

---

## 2. Tipo de problema e abordagem de IA

**Tipo de problema:** classificação supervisionada — o modelo aprende, a partir de exemplos rotulados, a prever a categoria de treino recomendada para um novo aluno.

**Abordagem escolhida:** Árvore de Decisão (Decision Tree), definida na Atividade 3, por ser interpretável (permite visualizar as regras de decisão) e adequada a um problema com atributos majoritariamente categóricos.

**Entradas (features):**
- `idade`
- `objetivo`
- `nivel_experiencia`
- `dias_disponiveis_semana`
- `restricao_fisica`
- `equipamento_disponivel`

**Saída (label/target):** `treino_recomendado` (Treino A, B, C ou D)

**Soluções semelhantes analisadas:**

1. **Fitbod** — https://fitbod.me
   App comercial que gera treinos de musculação personalizados usando aprendizado de máquina, considerando objetivo, nível de condicionamento, equipamento disponível e histórico de desempenho do usuário. É semelhante ao projeto por usar as mesmas dimensões de entrada (objetivo, nível, equipamento) para recomendar um treino. Diferença: o Fitbod ajusta o treino de forma contínua e individual a cada sessão (aprendizado incremental por usuário), enquanto este projeto propõe um classificador único treinado sobre uma base de vários alunos, que recomenda uma categoria de treino (A, B, C ou D) a partir do perfil, sem ajuste sessão a sessão.

2. **BodBot** — https://bodbot.com
   Aplicativo de planejamento de treinos que usa IA para montar rotinas adaptativas com base em objetivo, nível de experiência e equipamento disponível, redistribuindo o plano conforme o progresso do usuário. Semelhante ao projeto por partir do mesmo tipo de perfil de entrada para gerar uma recomendação de treino. Diferença: o BodBot opera como um sistema de planejamento contínuo e individualizado (replaneja a cada treino), enquanto este projeto trata o problema como uma classificação estática — dado um perfil, prever a categoria de treino mais adequada, sem histórico de sessões anteriores.

**Limitações e riscos conhecidos:**
- **Base de dados simulada, não real** — o modelo pode aprender padrões artificiais das regras usadas na simulação, que não necessariamente se repetem no comportamento de alunos reais. *Mitigação:* substituir a base simulada por dados reais nos Encontros 5 e 8, reavaliando o modelo após a troca.
- **Poucas variáveis de entrada** — o perfil do aluno é resumido em 6 atributos, o que pode ser insuficiente para capturar nuances relevantes (ex.: histórico de lesões, preferências de exercício, tempo de sessão). *Mitigação:* revisar a lista de atributos junto com a limpeza/preparação dos dados, incorporando novas variáveis se necessário.
- **Simplificação da recomendação em apenas 4 categorias de treino** — pode não representar bem a variedade real de treinos possíveis. *Mitigação:* avaliar, após os primeiros testes do modelo, se granularidade maior (mais categorias) é necessária ou se um esquema diferente (ex.: recomendação de exercícios individuais) seria mais adequado.

---

## 3. Base de dados

**Arquivo:** `dataset_academia.csv`
**Registros:** 300 alunos simulados
**Colunas:** `aluno_id`, `idade`, `objetivo`, `nivel_experiencia`, `dias_disponiveis_semana`, `restricao_fisica`, `equipamento_disponivel`, `treino_recomendado`

**Origem:** dados sintéticos, gerados em Python (pandas + numpy) a partir dos critérios definidos na Atividade 4 — distribuições estatísticas plausíveis para cada atributo e regras de associação entre o perfil do aluno e o treino recomendado, com 8% de ruído aleatório para simular exceções. A geração é reprodutível pelo script `gerar_dataset.py` (seed fixa = 1053). Uso livre para fins acadêmicos (dataset próprio, sem restrição de licença). Será substituída por dados reais nos Encontros 5 e 8, quando o tratamento e a limpeza forem trabalhados.

**Script gerador:** `gerar_dataset.py` (parâmetros das distribuições, regras de associação e seed)
**Notebook de análise:** `atividade4_academia.ipynb` (executado, com saídas e gráficos visíveis)

### Dicionário de dados

| Variável | Descrição | Tipo | Valores possíveis | Entrada/Saída | Observações |
|---|---|---|---|---|---|
| `aluno_id` | Identificador único do aluno simulado | Numérica discreta | 1 a 300 | — | Apenas identificação, não é feature |
| `idade` | Idade do aluno em anos | Numérica contínua | 16 a 65 anos | Entrada | Distribuição ~normal, média ~29 anos |
| `objetivo` | Objetivo principal do aluno | Categórica nominal | Emagrecimento, Hipertrofia, Condicionamento | Entrada | Sem valores ausentes |
| `nivel_experiencia` | Nível de experiência com treino | Categórica ordinal | Iniciante, Intermediário, Avançado | Entrada | Ordem implícita de progressão |
| `dias_disponiveis_semana` | Dias por semana disponíveis para treinar | Numérica discreta | 1 a 6 dias | Entrada | Média ~3,5 dias |
| `restricao_fisica` | Restrição física relevante | Categórica nominal | Nenhuma, Joelho, Ombro, Lombar | Entrada | Maioria sem restrição |
| `equipamento_disponivel` | Nível de acesso a equipamentos | Categórica ordinal | Completo, Limitado, Nenhum | Entrada | Reflete o tipo de local de treino |
| `treino_recomendado` | Categoria de treino recomendada | Categórica nominal | Treino A, B, C, D | **Saída (label)** | Variável-alvo do modelo |

### Estatísticas descritivas

**Variáveis numéricas**

| Variável | Média | Desvio padrão | Mínimo | Máximo |
|---|---|---|---|---|
| idade | 29,29 | 7,71 | 16 | 51 |
| dias_disponiveis_semana | 3,44 | 1,27 | 1 | 6 |

*Interpretação:* público concentrado em jovens adultos (média ~29 anos), com dispersão relevante (desvio de quase 8 anos, faixa de 16 a 51). A maioria dos alunos treina entre 3 e 4 dias por semana.

**Variáveis categóricas**

| Variável | Contagem por categoria |
|---|---|
| objetivo | Hipertrofia: 114 · Emagrecimento: 103 · Condicionamento: 83 |
| nivel_experiencia | Iniciante: 161 · Intermediário: 100 · Avançado: 39 |
| restricao_fisica | Nenhuma: 208 · Joelho: 34 · Lombar: 34 · Ombro: 24 |
| equipamento_disponivel | Completo: 168 · Limitado: 110 · Nenhum: 22 |
| treino_recomendado (label) | Treino D: 92 · Treino C: 80 · Treino A: 74 · Treino B: 54 |

*Interpretação:* objetivos relativamente equilibrados, com leve predominância de Hipertrofia. Maioria dos alunos é iniciante e sem restrição física. As classes do label ficaram razoavelmente balanceadas, o que favorece o treinamento futuro do classificador.

### Visualização inicial

Duas visualizações geradas no notebook:
1. **Histograma da distribuição de idade** — concentração entre 20 e 35 anos, leve assimetria à direita.
2. **Gráfico de barras dos treinos recomendados** — quatro categorias com frequências próximas, leve predominância dos treinos D (Peso Corporal Adaptado) e C (Funcional).

### Observações e limitações da base (ponto de partida para os Encontros 5 e 8)

- Base é 100% simulada — ainda não há dados reais de alunos.
- Limpeza e tratamento de dados (valores ausentes, outliers) não foram feitos nesta etapa, conforme orientado.
- Ruído de 8% foi adicionado para simular exceções reais, mas pode não representar fielmente a variabilidade de dados reais.

---

## 4. Qualidade dos dados — diagnóstico (Atividade 5 / Encontro 5)

Investigação de qualidade da base, executada no notebook `atividade5_academia.ipynb` (com todas as
saídas visíveis) e sintetizada no `relatorio_qualidade_dados.pdf`.

**Principais achados (base atual, simulada):**

| Eixo | Resultado |
|---|---|
| Dimensões | 300 linhas × 8 colunas |
| Dados ausentes | 0 em todas as colunas (0%) — artificial da geração sintética |
| Duplicados | 0 linhas idênticas, 0 `aluno_id` repetido; 7 colisões de perfil+rótulo (esperadas) |
| Inconsistências | `nivel_experiencia` sem acento vs dicionário; ordinais como texto nominal; dicionário diz idade "16–65", base vai até 51; 8% de ruído de rótulo (24 registros contradizem a regra de geração) |
| Desbalanceamento | leve — Treino D 30,7% vs Treino B 18,0% (razão 1,7:1) |
| Viés principal | acesso a equipamento: grupo "sem equipamento" (7,3%) tem rótulo praticamente fixo (Treino D) pela própria regra de geração — viés de amostragem + rotulagem |

A tabela de diagnóstico completa (problema · onde aparece · gravidade · ação de tratamento · quando),
as ações de tratamento justificadas e a discussão de vieses estão no relatório. O tratamento em si
será executado no Encontro 8.

**Slides da AP1:** `entregas/AP1_ViniciusCasagrande.pdf` — panorama do projeto (problema, abordagem, base, diagnóstico, vieses,
próximos passos).

---

## 5. Pipeline do projeto (Atividade 7)

O pipeline completo do projeto — da coleta do perfil do aluno até a recomendação final de treino — está documentado em:

- `Atividade7_Esboco_ViniciusCasagrande.pdf` — primeira versão do pipeline, tipo de aprendizado, features/label, verificação de vazamento e plano de divisão dos dados.
- `Atividade7_Final_ViniciusCasagrande.pdf` — versão consolidada, com status de cada etapa (feito/falta), formatos de entrada e saída detalhados e verificação de vazamento concluída.

**Resumo do pipeline:** coleta do perfil → preparação e limpeza dos dados → divisão treino/teste (80/20, estratificada) → treinamento da Árvore de Decisão (com validação cruzada k=5) → avaliação (F1-macro, matriz de confusão, desempenho por subgrupo) → recomendação da categoria de treino (A, B, C ou D).

**Tipo de aprendizado:** supervisionado, classificação multiclasse — justificativa completa na Atividade 7 (seção 3).

---

## 6. Limpeza e preparação da base (Atividade 8)

O tratamento da base está documentado em `atividade8_academia.ipynb`, executado do início ao fim, com:

- Recapitulação do diagnóstico de qualidade (Atividade 5).
- 7 transformações/decisões aplicadas (remoção de `aluno_id` das features, padronização de nomenclatura, tipagem ordinal, atualização do dicionário de dados, e decisão consciente de **não** corrigir o ruído de rótulo nem o desbalanceamento nesta etapa).
- Tabela de decisões completa (transformação · coluna · motivo · impacto · risco).
- Verificação de vazamento de resposta concluída (sem vazamento identificado).

**Arquivos:**
- `dataset_academia.csv` — base original, **intacta**.
- `dataset_academia_tratado.csv` — base tratada, salva e verificada por releitura.
- `gerar_dataset.py` — script reprodutível de geração da base (seed = 1053).

**Pendente para o Encontro 9:** codificação numérica das variáveis categóricas (a ser ajustada apenas no conjunto de treino, após o split) e a divisão treino/teste em si.

---

## 7. Estrutura do repositório

```
├── README.md
├── gerar_dataset.py                        # script reprodutível de geração da base
├── dataset_academia.csv                    # base original simulada — 300 alunos, 8 colunas (intacta)
├── dataset_academia_tratado.csv            # base tratada (Atividade 8), salva e verificada
├── atividade4_academia.ipynb               # notebook de análise exploratória (Atividade 4)
├── atividade5_academia.ipynb               # notebook de diagnóstico de qualidade (Atividade 5, executado)
├── atividade8_academia.ipynb               # notebook de limpeza e preparação da base (Atividade 8, executado)
├── relatorio_qualidade_dados.pdf           # relatório curto de qualidade dos dados + tabela de diagnóstico
├── grafico_analise_inicial.png             # figura da análise exploratória
├── grafico_desbalanceamento.png            # figura do desbalanceamento das classes
└── entregas/                               # arquivos de entrega individual (modelo padrão, esboços e slides)
    ├── Atividade4_Final_ViniciusCasagrande_corrigido.pdf
    ├── Atividade5_Esboco_ViniciusCasagrande.docx / .pdf
    ├── Atividade5_Final_ViniciusCasagrande.docx / .pdf
    ├── Atividade6_ViniciusCasagrande.docx
    ├── Atividade7_Esboco_ViniciusCasagrande.docx
    ├── Atividade7_Final_ViniciusCasagrande.docx
    ├── Atividade8_Final_ViniciusCasagrande.docx / .pdf
    ├── AP1_ViniciusCasagrande.pdf           # slides da AP1 (nome exigido pelo enunciado)
    ├── AP1_ViniciusCasagrande.pptx          # slides da AP1 (fonte editável, versão mais recente)
    ├── slides_ap1.pptx                      # slides da AP1 — versão anterior, fonte do PDF acima
    └── roteiro_apresentacao.md              # roteiro de apoio para a apresentação da AP1
```

---

## 8. Backlog do projeto

- [x] Definição do problema e domínio (Atividade 1)
- [x] Contextualização da solução de IA (Atividade 2)
- [x] Escolha e justificativa da abordagem técnica (Atividade 3)
- [x] Base de dados simulada + dicionário de dados (Atividade 4)
- [x] Diagnóstico de qualidade dos dados + discussão de vieses (Atividade 5 / Encontro 5)
- [ ] Preparação e tratamento dos dados para o modelo (Encontro 8)
- [ ] Treinamento do modelo — Árvore de Decisão (Encontro 9)
- [ ] Avaliação do modelo (F1-macro, matriz de confusão, desempenho por subgrupo)
- [ ] Apresentação final do projeto

---

## Declaração de uso de Inteligência Artificial

**Uso de IA nesta entrega:** Sim
**Ferramenta:** Claude (Anthropic)
**Utilização:** apoio na geração do script de simulação do dataset, na construção e execução dos notebooks de análise exploratória e de diagnóstico de qualidade (código pandas para contagens de ausentes, duplicados, valores únicos e proporção de classes), na reprodução da regra de geração para quantificar o ruído de rótulo, e na redação e formatação deste README, do relatório de qualidade e dos slides da AP1.
**Produção própria:** as decisões sobre variáveis do perfil do aluno, critério de geração dos dados simulados, escolha da variável-alvo, classificação de gravidade dos problemas de qualidade, escolha entre alternativas de tratamento, identificação e análise do viés de acesso a equipamento e interpretação dos resultados são do estudante.
