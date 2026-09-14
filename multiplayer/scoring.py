# ============================================================
# SISTEMA DE PONTUAÇÃO MULTIPLAYER
# ============================================================


def calcular_pontos(
    acertou,
    tempo_resposta,
    tempo_limite,
    sequencia=0
):
    """
    Calcula os pontos recebidos por uma resposta.

    Pontuação:
    - Errou: 0 pontos
    - Acertou: 500 pontos base
    - Velocidade: até +500 pontos
    - Sequência de acertos: até +200 pontos
    """

    if not acertou:
        return 0

    # -----------------------------
    # PONTOS BASE
    # -----------------------------

    pontos_base = 500


    # -----------------------------
    # BÔNUS DE VELOCIDADE
    # -----------------------------

    try:

        tempo_resposta = float(
            tempo_resposta
        )

        tempo_limite = float(
            tempo_limite
        )

    except (TypeError, ValueError):

        tempo_resposta = tempo_limite


    if tempo_limite <= 0:
        bonus_velocidade = 0

    else:

        proporcao = 1 - (
            tempo_resposta /
            tempo_limite
        )

        proporcao = max(
            0,
            min(1, proporcao)
        )

        bonus_velocidade = round(
            proporcao * 500
        )


    # -----------------------------
    # BÔNUS DE SEQUÊNCIA
    # -----------------------------

    sequencia = max(
        0,
        int(sequencia or 0)
    )

    bonus_sequencia = min(
        sequencia * 40,
        200
    )


    # -----------------------------
    # TOTAL
    # -----------------------------

    pontos = (
        pontos_base
        +
        bonus_velocidade
        +
        bonus_sequencia
    )

    return int(pontos)