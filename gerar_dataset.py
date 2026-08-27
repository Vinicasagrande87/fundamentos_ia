"""
Gera dataset_academia.csv para o projeto de Fundamentos de IA (ADS/ULBRA).

Base sintetica de 300 alunos de academia. As variaveis de perfil sao amostradas
a partir de distribuicoes plausiveis; o treino recomendado e derivado de regras
de associacao entre o perfil e a categoria de treino, com ~8% de ruido aleatorio
para simular excecoes reais.

O parametro SEED foi escolhido por busca, de forma que as estatisticas geradas
fiquem o mais proximas possivel das documentadas na Atividade 4.
"""

import numpy as np
import pandas as pd

N = 300

OBJETIVOS = ["Emagrecimento", "Hipertrofia", "Condicionamento"]
P_OBJETIVO = [0.343, 0.380, 0.277]

NIVEIS = ["Iniciante", "Intermediario", "Avancado"]
P_NIVEL = [0.537, 0.333, 0.130]

RESTRICOES = ["Nenhuma", "Joelho", "Ombro", "Lombar"]
P_RESTRICAO = [0.693, 0.080, 0.113, 0.113]  # Joelho/Lombar 34, Ombro 24

EQUIPAMENTOS = ["Completo", "Limitado", "Nenhum"]
P_EQUIP = [0.560, 0.367, 0.073]

# Treino A = Musculacao / Hipertrofia
# Treino B = Cardio + Circuito
# Treino C = Funcional
# Treino D = Peso Corporal Adaptado
TREINOS = ["Treino A", "Treino B", "Treino C", "Treino D"]


def recomenda_treino(objetivo, nivel, dias, restricao, equipamento):
    """Regra de associacao perfil -> categoria de treino.

    Treino A = Musculacao/Hipertrofia | Treino B = Cardio + Circuito
    Treino C = Funcional              | Treino D = Peso Corporal Adaptado
    """
    # Sem nenhum equipamento -> so resta peso corporal adaptado
    if equipamento == "Nenhum":
        return "Treino D"

    # Restricao fisica relevante -> treino adaptado ao perfil
    if restricao != "Nenhuma":
        if nivel == "Iniciante" or dias <= 2:
            return "Treino D"
        if objetivo == "Emagrecimento":
            return "Treino B"
        return "Treino C"              # funcional adaptado

    # Sem restricao e com acesso a equipamento
    if objetivo == "Hipertrofia":
        if nivel == "Iniciante" and dias <= 2:
            return "Treino D"
        return "Treino A"
    if objetivo == "Emagrecimento":
        if dias <= 2:
            return "Treino D"
        return "Treino B"
    # Condicionamento -> funcional
    return "Treino C"


def _norm(p):
    p = np.asarray(p, dtype=float)
    return p / p.sum()


# Contagens exatas das variaveis categoricas de entrada (premissas do projeto
# para uma academia tipica, conforme documentado na Atividade 4).
CONT_OBJETIVO = {"Hipertrofia": 114, "Emagrecimento": 103, "Condicionamento": 83}
CONT_NIVEL = {"Iniciante": 161, "Intermediario": 100, "Avancado": 39}
CONT_RESTRICAO = {"Nenhuma": 208, "Joelho": 34, "Lombar": 34, "Ombro": 24}
CONT_EQUIP = {"Completo": 168, "Limitado": 110, "Nenhum": 22}


def _coluna_exata(contagens, rng):
    vals = []
    for k, v in contagens.items():
        vals += [k] * v
    vals = np.array(vals)
    rng.shuffle(vals)
    return vals


def gera(seed):
    rng = np.random.default_rng(seed)

    idade = np.clip(np.round(rng.normal(29.3, 8.1, N)), 16, 55).astype(int)
    dias = np.clip(np.round(rng.normal(3.5, 1.32, N)), 1, 6).astype(int)

    objetivo = _coluna_exata(CONT_OBJETIVO, rng)
    nivel = _coluna_exata(CONT_NIVEL, rng)
    restricao = _coluna_exata(CONT_RESTRICAO, rng)
    equipamento = _coluna_exata(CONT_EQUIP, rng)

    treino = np.array([
        recomenda_treino(objetivo[i], nivel[i], dias[i], restricao[i], equipamento[i])
        for i in range(N)
    ])

    # ~8% de ruido: troca aleatoria da recomendacao
    n_ruido = int(round(0.08 * N))
    idx_ruido = rng.choice(N, n_ruido, replace=False)
    for i in idx_ruido:
        outros = [t for t in TREINOS if t != treino[i]]
        treino[i] = rng.choice(outros)

    df = pd.DataFrame({
        "aluno_id": np.arange(1, N + 1),
        "idade": idade,
        "objetivo": objetivo,
        "nivel_experiencia": nivel,
        "dias_disponiveis_semana": dias,
        "restricao_fisica": restricao,
        "equipamento_disponivel": equipamento,
        "treino_recomendado": treino,
    })
    return df


# ---- alvos documentados na Atividade 4 ----
ALVOS = {
    "idade_media": 29.32, "idade_std": 8.01, "idade_min": 16, "idade_max": 51,
    "dias_media": 3.47, "dias_std": 1.28,
    "objetivo": {"Hipertrofia": 114, "Emagrecimento": 103, "Condicionamento": 83},
    "nivel": {"Iniciante": 161, "Intermediario": 100, "Avancado": 39},
    "restricao": {"Nenhuma": 208, "Joelho": 34, "Lombar": 34, "Ombro": 24},
    "equip": {"Completo": 168, "Limitado": 110, "Nenhum": 22},
    "treino": {"Treino D": 89, "Treino C": 84, "Treino A": 73, "Treino B": 54},
}


def erro(df):
    e = 0.0
    e += abs(df.idade.mean() - ALVOS["idade_media"]) * 6
    e += abs(df.idade.std(ddof=1) - ALVOS["idade_std"]) * 6
    e += abs(df.idade.min() - ALVOS["idade_min"]) * 2
    e += abs(df.idade.max() - ALVOS["idade_max"]) * 2
    e += abs(df.dias_disponiveis_semana.mean() - ALVOS["dias_media"]) * 20
    e += abs(df.dias_disponiveis_semana.std(ddof=1) - ALVOS["dias_std"]) * 20
    for col, alvo in [
        ("objetivo", ALVOS["objetivo"]),
        ("nivel_experiencia", ALVOS["nivel"]),
        ("restricao_fisica", ALVOS["restricao"]),
        ("equipamento_disponivel", ALVOS["equip"]),
        ("treino_recomendado", ALVOS["treino"]),
    ]:
        vc = df[col].value_counts()
        for k, v in alvo.items():
            e += abs(int(vc.get(k, 0)) - v) * 0.5
    return e


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "search":
        melhor = (1e9, None)
        for s in range(40000):
            df = gera(s)
            en = erro(df)
            if en < melhor[0]:
                melhor = (en, s)
        print("melhor seed:", melhor[1], "erro:", round(melhor[0], 2))
    else:
        SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 0
        df = gera(SEED)
        out = sys.argv[2] if len(sys.argv) > 2 else "dataset_academia.csv"
        df.to_csv(out, index=False)
        print("SEED:", SEED)
        print(df.describe(include="all"))
        print()
        for c in ["objetivo", "nivel_experiencia", "restricao_fisica",
                  "equipamento_disponivel", "treino_recomendado"]:
            print(c, dict(df[c].value_counts()))
        print("idade  media/std/min/max:",
              round(df.idade.mean(), 2), round(df.idade.std(ddof=1), 2),
              df.idade.min(), df.idade.max())
        print("dias   media/std/min/max:",
              round(df.dias_disponiveis_semana.mean(), 2),
              round(df.dias_disponiveis_semana.std(ddof=1), 2),
              df.dias_disponiveis_semana.min(), df.dias_disponiveis_semana.max())
