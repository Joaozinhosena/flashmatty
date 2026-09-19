import random


# ============================================================
# MODOS DISPONÍVEIS
# ============================================================

MODOS = {

    "classico": {
        "nome": "Clássico",
        "icone": "🎮",
        "descricao": "Partida tradicional.",
        "multiplicador": 1.0,
        "penalidade_erro": 0
    },

    "relampago": {
        "nome": "Relâmpago",
        "icone": "⚡",
        "descricao":
            "Questões rápidas com bônus de pontuação.",
        "multiplicador": 1.25,
        "penalidade_erro": 0
    },

    "combo": {
        "nome": "Combo",
        "icone": "🔥",
        "descricao":
            "Sequências de acertos aumentam os pontos.",
        "multiplicador": 1.0,
        "penalidade_erro": 0
    },

    "dobro": {
        "nome": "Dobro ou Nada",
        "icone": "🎲",
        "descricao":
            "Acertos valem o dobro, mas erros retiram pontos.",
        "multiplicador": 2.0,
        "penalidade_erro": 250
    },

    "bomba": {
        "nome": "Bomba Matemática",
        "icone": "💣",
        "descricao":
            "Cada rodada pode valer 1x, 2x ou 3x pontos.",
        "multiplicador": 1.0,
        "penalidade_erro": 0
    }

}


# ============================================================
# NORMALIZAR MODO
# ============================================================

def normalizar_modo(modo):

    modo = str(
        modo or "classico"
    ).strip().lower()

    if modo not in MODOS:
        return "classico"

    return modo


# ============================================================
# INFORMAÇÕES DO MODO
# ============================================================

def obter_modo(modo):

    modo = normalizar_modo(
        modo
    )

    dados = dict(
        MODOS[modo]
    )

    dados["codigo"] = modo

    return dados


# ============================================================
# TEMPO DA QUESTÃO
# ============================================================

def ajustar_tempo(
    modo,
    tempo_original
):

    modo = normalizar_modo(
        modo
    )

    try:

        tempo_original = int(
            tempo_original
        )

    except (
        TypeError,
        ValueError
    ):

        tempo_original = 20


    tempo_original = max(
        5,
        tempo_original
    )


    # Relâmpago nunca passa de 10 segundos.
    if modo == "relampago":

        return min(
            tempo_original,
            10
        )


    return tempo_original


# ============================================================
# PREPARAR EFEITO DA RODADA
# ============================================================

def preparar_rodada(
    modo
):

    modo = normalizar_modo(
        modo
    )

    config = MODOS[
        modo
    ]


    efeito = {

        "modo":
            modo,

        "nome":
            config["nome"],

        "icone":
            config["icone"],

        "multiplicador":
            float(
                config.get(
                    "multiplicador",
                    1
                )
            ),

        "penalidade_erro":
            int(
                config.get(
                    "penalidade_erro",
                    0
                )
            ),

        "mensagem":
            config["descricao"]

    }


    # ========================================================
    # BOMBA MATEMÁTICA
    # ========================================================

    if modo == "bomba":

        sorteio = random.random()


        # 15% de chance de 3x
        if sorteio < 0.15:

            efeito[
                "multiplicador"
            ] = 3.0

            efeito[
                "mensagem"
            ] = (
                "💥 SUPER BOMBA! "
                "Esta questão vale 3x pontos!"
            )


        # 30% de chance de 2x
        elif sorteio < 0.45:

            efeito[
                "multiplicador"
            ] = 2.0

            efeito[
                "mensagem"
            ] = (
                "💣 BOMBA! "
                "Esta questão vale 2x pontos!"
            )


        else:

            efeito[
                "multiplicador"
            ] = 1.0

            efeito[
                "mensagem"
            ] = (
                "🎮 Rodada normal."
            )


    return efeito


# ============================================================
# MULTIPLICADOR DO COMBO
# ============================================================

def multiplicador_combo(
    sequencia
):

    try:

        sequencia = int(
            sequencia
        )

    except (
        TypeError,
        ValueError
    ):

        sequencia = 0


    sequencia = max(
        0,
        sequencia
    )


    # Primeiro acerto:
    # 1x
    #
    # Segundo:
    # 1.1x
    #
    # Terceiro:
    # 1.2x
    #
    # Até no máximo 1.5x.

    extra = max(
        0,
        sequencia - 1
    ) * 0.10


    return min(
        1.5,
        1.0 + extra
    )


# ============================================================
# APLICAR REGRA ESPECIAL À PONTUAÇÃO
# ============================================================

def aplicar_modo_pontuacao(
    modo,
    pontos_base,
    acertou,
    sequencia=0,
    efeito=None
):

    modo = normalizar_modo(
        modo
    )


    try:

        pontos_base = int(
            pontos_base
        )

    except (
        TypeError,
        ValueError
    ):

        pontos_base = 0


    # ========================================================
    # ERRO
    # ========================================================

    if not acertou:

        penalidade = int(
            MODOS[
                modo
            ].get(
                "penalidade_erro",
                0
            )
        )

        return -penalidade


    # ========================================================
    # ACERTO
    # ========================================================

    multiplicador = float(
        MODOS[
            modo
        ].get(
            "multiplicador",
            1
        )
    )


    # Bomba usa o multiplicador sorteado
    # especificamente para a rodada.
    if (
        efeito
        and
        modo == "bomba"
    ):

        multiplicador = float(
            efeito.get(
                "multiplicador",
                1
            )
        )


    # Combo aumenta conforme sequência.
    if modo == "combo":

        multiplicador *= (
            multiplicador_combo(
                sequencia
            )
        )


    pontos = round(
        pontos_base
        *
        multiplicador
    )


    return max(
        0,
        int(pontos)
    )