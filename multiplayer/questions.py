import random
import unicodedata


# =========================================================
# UTILITÁRIOS
# =========================================================

def normalizar_texto(texto):
    """
    Remove acentos e padroniza o texto.

    Exemplo:
    "Adição" -> "adicao"
    "Ângulo" -> "angulo"
    """

    texto = str(texto or "").strip().lower()

    texto = unicodedata.normalize(
        "NFKD",
        texto
    )

    texto = "".join(
        caractere
        for caractere in texto
        if not unicodedata.combining(caractere)
    )

    return texto


def embaralhar(
    correta,
    erradas
):
    """
    Recebe uma resposta correta e respostas erradas,
    remove duplicações e devolve 4 alternativas
    embaralhadas.
    """

    correta = str(correta)

    alternativas = [
        correta
    ]

    for alternativa in erradas:

        alternativa = str(
            alternativa
        )

        if (
            alternativa
            not in alternativas
        ):
            alternativas.append(
                alternativa
            )


    # Se for uma resposta numérica e ainda
    # faltarem alternativas, gera valores próximos.
    if len(alternativas) < 4:

        try:

            base = int(
                correta
            )

            tentativas = 0

            while (
                len(alternativas) < 4
                and
                tentativas < 100
            ):

                tentativas += 1

                variacao = random.choice([
                    -15,
                    -10,
                    -5,
                    -4,
                    -3,
                    -2,
                    -1,
                    1,
                    2,
                    3,
                    4,
                    5,
                    10,
                    15
                ])

                valor = (
                    base
                    +
                    variacao
                )

                if valor < 0:
                    continue

                valor = str(
                    valor
                )

                if (
                    valor
                    not in alternativas
                ):
                    alternativas.append(
                        valor
                    )

        except (
            TypeError,
            ValueError
        ):
            pass


    # Proteção extra para nunca ficar
    # preso tentando criar alternativas.
    contador = 1

    while len(alternativas) < 4:

        alternativa = (
            f"Alternativa {contador}"
        )

        contador += 1

        if (
            alternativa
            not in alternativas
        ):
            alternativas.append(
                alternativa
            )


    alternativas = (
        alternativas[:4]
    )

    random.shuffle(
        alternativas
    )

    return alternativas


def questao_numerica(
    pergunta,
    correta
):
    """
    Cria uma questão numérica com
    quatro alternativas.
    """

    correta = int(
        correta
    )

    erradas = []

    tentativas = 0

    while (
        len(erradas) < 3
        and
        tentativas < 100
    ):

        tentativas += 1

        variacao = random.choice([
            -15,
            -10,
            -5,
            -4,
            -3,
            -2,
            -1,
            1,
            2,
            3,
            4,
            5,
            10,
            15
        ])

        valor = (
            correta
            +
            variacao
        )

        if (
            valor >= 0
            and
            valor != correta
            and
            valor not in erradas
        ):

            erradas.append(
                valor
            )


    return {

        "pergunta":
            pergunta,

        "correta":
            str(correta),

        "alternativas":
            embaralhar(
                correta,
                erradas
            )

    }


# =========================================================
# ADIÇÃO
# =========================================================

def gerar_adicao():

    a = random.randint(
        5,
        80
    )

    b = random.randint(
        5,
        80
    )

    return questao_numerica(
        f"Quanto é {a} + {b}?",
        a + b
    )


# =========================================================
# SUBTRAÇÃO
# =========================================================

def gerar_subtracao():

    a = random.randint(
        20,
        100
    )

    b = random.randint(
        1,
        a
    )

    return questao_numerica(
        f"Quanto é {a} - {b}?",
        a - b
    )


# =========================================================
# MULTIPLICAÇÃO
# =========================================================

def gerar_multiplicacao():

    a = random.randint(
        2,
        12
    )

    b = random.randint(
        2,
        12
    )

    return questao_numerica(
        f"Quanto é {a} × {b}?",
        a * b
    )


# =========================================================
# DIVISÃO
# =========================================================

def gerar_divisao():
    """
    A divisão sempre gera
    resultado inteiro.
    """

    resposta = random.randint(
        2,
        12
    )

    divisor = random.randint(
        2,
        10
    )

    total = (
        resposta
        *
        divisor
    )

    return questao_numerica(
        f"Quanto é {total} ÷ {divisor}?",
        resposta
    )


# =========================================================
# FRAÇÕES
# =========================================================

def gerar_fracao():

    denominador = random.randint(
        2,
        12
    )

    numerador = random.randint(
        1,
        denominador - 1
    )


    tipo = random.choice([
        "numerador",
        "denominador"
    ])


    if tipo == "numerador":

        return questao_numerica(

            (
                f"Na fração "
                f"{numerador}/{denominador}, "
                f"qual é o numerador?"
            ),

            numerador
        )


    return questao_numerica(

        (
            f"Na fração "
            f"{numerador}/{denominador}, "
            f"qual é o denominador?"
        ),

        denominador
    )


# =========================================================
# TEMPO
# =========================================================

def gerar_tempo():

    tipo = random.choice([
        "hora_minuto",
        "minuto_hora"
    ])


    if tipo == "hora_minuto":

        horas = random.randint(
            1,
            8
        )

        return questao_numerica(

            (
                f"{horas} "
                f"{'hora' if horas == 1 else 'horas'} "
                f"equivale a quantos minutos?"
            ),

            horas * 60
        )


    horas = random.randint(
        1,
        8
    )

    minutos = (
        horas
        *
        60
    )

    return questao_numerica(

        (
            f"{minutos} minutos "
            f"equivalem a quantas horas?"
        ),

        horas
    )


# =========================================================
# ÁREA
# =========================================================

def gerar_area():

    largura = random.randint(
        2,
        12
    )

    altura = random.randint(
        2,
        12
    )

    return questao_numerica(

        (
            f"Qual é a área de um retângulo "
            f"com {largura} unidades de largura "
            f"e {altura} unidades de altura?"
        ),

        largura * altura
    )


# =========================================================
# PERÍMETRO
# =========================================================

def gerar_perimetro():

    largura = random.randint(
        2,
        12
    )

    altura = random.randint(
        2,
        12
    )

    return questao_numerica(

        (
            f"Qual é o perímetro de um retângulo "
            f"com lados de {largura} e {altura} unidades?"
        ),

        2 * (
            largura
            +
            altura
        )
    )


# =========================================================
# ÂNGULOS
# =========================================================

def gerar_angulo():

    angulo = random.choice([
        30,
        45,
        60,
        90,
        120,
        135,
        150,
        180
    ])


    if angulo < 90:

        correta = (
            "Agudo"
        )


    elif angulo == 90:

        correta = (
            "Reto"
        )


    elif angulo < 180:

        correta = (
            "Obtuso"
        )


    else:

        correta = (
            "Raso"
        )


    alternativas = [
        "Agudo",
        "Reto",
        "Obtuso",
        "Raso"
    ]


    random.shuffle(
        alternativas
    )


    return {

        "pergunta":
            (
                f"Um ângulo de "
                f"{angulo}° é classificado como:"
            ),

        "correta":
            correta,

        "alternativas":
            alternativas

    }


# =========================================================
# GERADORES DISPONÍVEIS
# =========================================================

GERADORES = {

    "adicao":
        gerar_adicao,

    "subtracao":
        gerar_subtracao,

    "multiplicacao":
        gerar_multiplicacao,

    "divisao":
        gerar_divisao,

    "fracao":
        gerar_fracao,

    "tempo":
        gerar_tempo,

    "area":
        gerar_area,

    "perimetro":
        gerar_perimetro,

    "angulo":
        gerar_angulo

}


# =========================================================
# GERAR UMA QUESTÃO
# =========================================================

def gerar_questao_multiplayer(
    assunto
):

    assunto = normalizar_texto(
        assunto
    )


    # Se o assunto existir,
    # usa diretamente seu gerador.
    if (
        assunto in GERADORES
    ):

        return GERADORES[
            assunto
        ]()


    # ==========================================
    # MATEMÁTICA MISTA
    # ==========================================

    gerador = random.choice(
        list(
            GERADORES.values()
        )
    )

    return gerador()


# =========================================================
# GERAR PARTIDA COMPLETA
# =========================================================

def gerar_partida(
    assunto,
    quantidade
):
    """
    Gera as questões da partida tentando
    evitar perguntas repetidas.
    """

    try:

        quantidade = int(
            quantidade
        )

    except (
        TypeError,
        ValueError
    ):

        quantidade = 10


    # Evita valores absurdos enviados
    # manualmente pelo navegador.
    quantidade = max(
        1,
        min(
            quantidade,
            50
        )
    )


    partida = []

    perguntas_usadas = set()

    tentativas = 0

    limite_tentativas = (
        quantidade
        *
        20
    )


    while (
        len(partida) < quantidade
        and
        tentativas < limite_tentativas
    ):

        tentativas += 1

        questao = (
            gerar_questao_multiplayer(
                assunto
            )
        )

        pergunta = (
            questao[
                "pergunta"
            ]
        )


        # Evita a mesma pergunta
        # aparecer duas vezes.
        if (
            pergunta
            in perguntas_usadas
        ):
            continue


        perguntas_usadas.add(
            pergunta
        )

        partida.append(
            questao
        )


    # Proteção caso não seja possível
    # gerar perguntas únicas suficientes.
    while (
        len(partida)
        <
        quantidade
    ):

        partida.append(

            gerar_questao_multiplayer(
                assunto
            )

        )


    return partida