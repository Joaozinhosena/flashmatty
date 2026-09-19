# ============================================================
# SISTEMA DE PONTUAÇÃO MULTIPLAYER
# ============================================================


# ------------------------------------------------------------
# CONFIGURAÇÕES DE PONTUAÇÃO
# ------------------------------------------------------------

PONTOS_BASE = 500

BONUS_VELOCIDADE_MAXIMO = 500

PONTOS_POR_SEQUENCIA = 40

BONUS_SEQUENCIA_MAXIMO = 200


# Pontuação máxima possível em uma questão:
#
# 500 base
# + 500 velocidade
# + 200 sequência
#
# = 1200 pontos

PONTUACAO_MAXIMA = (
    PONTOS_BASE
    +
    BONUS_VELOCIDADE_MAXIMO
    +
    BONUS_SEQUENCIA_MAXIMO
)


# ============================================================
# NORMALIZAR VALORES
# ============================================================

def normalizar_numero(
    valor,
    padrao=0.0
):
    """
    Converte um valor para float.

    Caso não seja possível converter,
    retorna o valor padrão.
    """

    try:

        return float(
            valor
        )

    except (
        TypeError,
        ValueError
    ):

        return float(
            padrao
        )


def normalizar_inteiro(
    valor,
    padrao=0
):
    """
    Converte um valor para inteiro.

    Caso não seja possível converter,
    retorna o valor padrão.
    """

    try:

        return int(
            valor
        )

    except (
        TypeError,
        ValueError
    ):

        return int(
            padrao
        )


# ============================================================
# CALCULAR BÔNUS DE VELOCIDADE
# ============================================================

def calcular_bonus_velocidade(
    tempo_resposta,
    tempo_limite
):
    """
    Calcula até 500 pontos extras
    de acordo com a velocidade da resposta.

    Quanto mais rápido o jogador responder,
    maior será o bônus.
    """

    tempo_limite = normalizar_numero(
        tempo_limite,
        0
    )


    # Se o tempo limite for inválido,
    # não concede bônus.
    if tempo_limite <= 0:

        return 0


    tempo_resposta = normalizar_numero(
        tempo_resposta,
        tempo_limite
    )


    # Impede tempo negativo.
    tempo_resposta = max(
        0,
        tempo_resposta
    )


    # Se passou do limite,
    # considera o tempo máximo.
    tempo_resposta = min(
        tempo_resposta,
        tempo_limite
    )


    proporcao = (
        1
        -
        (
            tempo_resposta
            /
            tempo_limite
        )
    )


    proporcao = max(
        0,
        min(
            1,
            proporcao
        )
    )


    bonus = round(
        proporcao
        *
        BONUS_VELOCIDADE_MAXIMO
    )


    return int(
        bonus
    )


# ============================================================
# CALCULAR BÔNUS DE SEQUÊNCIA
# ============================================================

def calcular_bonus_sequencia(
    sequencia
):
    """
    Calcula bônus por sequência de acertos.

    Cada acerto consecutivo adiciona
    40 pontos, até o limite de 200.
    """

    sequencia = normalizar_inteiro(
        sequencia,
        0
    )


    sequencia = max(
        0,
        sequencia
    )


    bonus = (
        sequencia
        *
        PONTOS_POR_SEQUENCIA
    )


    bonus = min(
        bonus,
        BONUS_SEQUENCIA_MAXIMO
    )


    return int(
        bonus
    )


# ============================================================
# CALCULAR PONTUAÇÃO
# ============================================================

def calcular_pontos(
    acertou,
    tempo_resposta,
    tempo_limite,
    sequencia=0
):
    """
    Calcula a pontuação recebida
    por uma resposta no multiplayer.

    Regras:

    Erro:
        0 pontos

    Acerto:
        +500 pontos base

    Velocidade:
        até +500 pontos

    Sequência:
        +40 pontos por acerto consecutivo
        até o máximo de +200 pontos

    Pontuação máxima:
        1200 pontos por questão
    """


    # --------------------------------------------------------
    # RESPOSTA ERRADA
    # --------------------------------------------------------

    if not acertou:

        return 0


    # --------------------------------------------------------
    # BÔNUS DE VELOCIDADE
    # --------------------------------------------------------

    bonus_velocidade = (
        calcular_bonus_velocidade(
            tempo_resposta,
            tempo_limite
        )
    )


    # --------------------------------------------------------
    # BÔNUS DE SEQUÊNCIA
    # --------------------------------------------------------

    bonus_sequencia = (
        calcular_bonus_sequencia(
            sequencia
        )
    )


    # --------------------------------------------------------
    # TOTAL
    # --------------------------------------------------------

    pontos = (
        PONTOS_BASE
        +
        bonus_velocidade
        +
        bonus_sequencia
    )


    # Proteção adicional.
    pontos = max(
        0,
        min(
            pontos,
            PONTUACAO_MAXIMA
        )
    )


    return int(
        pontos
    )