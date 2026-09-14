import random


def embaralhar(
    correta,
    erradas
):

    alternativas = [
        str(correta)
    ] + [
        str(x)
        for x in erradas
    ]

    # Remove repetidas
    alternativas = list(
        dict.fromkeys(
            alternativas
        )
    )

    while len(alternativas) < 4:

        try:
            base = int(correta)

            nova = str(
                max(
                    0,
                    base
                    +
                    random.randint(
                        -10,
                        10
                    )
                )
            )

        except:

            nova = "Nenhuma"

        if nova not in alternativas:
            alternativas.append(
                nova
            )

    alternativas = alternativas[:4]

    random.shuffle(
        alternativas
    )

    return alternativas


def questao_numerica(
    pergunta,
    correta
):

    correta = int(
        correta
    )

    erradas = []

    while len(erradas) < 3:

        variacao = random.choice([
            -10, -5, -3, -2, -1,
            1, 2, 3, 5, 10
        ])

        valor = correta + variacao

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
        "pergunta": pergunta,
        "correta": str(correta),
        "alternativas": embaralhar(
            correta,
            erradas
        )
    }


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


def gerar_divisao():

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


def gerar_fracao():

    denominador = random.randint(
        2,
        10
    )

    numerador = random.randint(
        1,
        denominador - 1
    )

    if random.choice([
        True,
        False
    ]):

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


def gerar_tempo():

    horas = random.randint(
        1,
        8
    )

    return questao_numerica(
        (
            f"{horas} horas equivalem "
            f"a quantos minutos?"
        ),
        horas * 60
    )


def gerar_area():

    largura = random.randint(
        2,
        10
    )

    altura = random.randint(
        2,
        10
    )

    return questao_numerica(
        (
            f"Qual é a área de um retângulo "
            f"de {largura} × {altura}?"
        ),
        largura * altura
    )


def gerar_perimetro():

    largura = random.randint(
        2,
        10
    )

    altura = random.randint(
        2,
        10
    )

    return questao_numerica(
        (
            f"Qual é o perímetro de um "
            f"retângulo de {largura} × {altura}?"
        ),
        2 * (
            largura + altura
        )
    )


def gerar_angulo():

    angulo = random.choice([
        30,
        45,
        90,
        120,
        150
    ])

    if angulo < 90:
        correta = "Agudo"

    elif angulo == 90:
        correta = "Reto"

    else:
        correta = "Obtuso"

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
                f"{angulo}° é:"
            ),

        "correta": correta,

        "alternativas":
            alternativas
    }


def gerar_questao_multiplayer(
    assunto
):

    assunto = assunto.lower()

    if "adicao" in assunto:
        return gerar_adicao()

    if "subtracao" in assunto:
        return gerar_subtracao()

    if "multiplicacao" in assunto:
        return gerar_multiplicacao()

    if "divisao" in assunto:
        return gerar_divisao()

    if "fracao" in assunto:
        return gerar_fracao()

    if "tempo" in assunto:
        return gerar_tempo()

    if "area" in assunto:
        return gerar_area()

    if "perimetro" in assunto:
        return gerar_perimetro()

    if "angulo" in assunto:
        return gerar_angulo()

    # Misto
    geradores = [
        gerar_adicao,
        gerar_subtracao,
        gerar_multiplicacao,
        gerar_divisao
    ]

    return random.choice(
        geradores
    )()


def gerar_partida(
    assunto,
    quantidade
):

    return [
        gerar_questao_multiplayer(
            assunto
        )

        for _ in range(
            quantidade
        )
    ]