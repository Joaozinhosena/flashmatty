import random


def questao(pergunta, resposta):

    return {
        "pergunta": pergunta,
        "resposta": str(resposta)
    }


def gerar_questao(tipo):

    # ========================================================
    # ADIÇÃO
    # ========================================================

    if tipo == "adicao_visual":

        a = random.randint(1, 5)
        b = random.randint(1, 5)

        return questao(
            f"Você tem {a} estrelas e ganhou mais {b}. Quantas estrelas tem agora?",
            a + b
        )


    if tipo == "adicao":

        a = random.randint(5, 50)
        b = random.randint(1, 40)

        return questao(
            f"Quanto é {a} + {b}?",
            a + b
        )


    if tipo == "problema_adicao":

        a = random.randint(2, 30)
        b = random.randint(2, 30)

        return questao(
            f"Lucas tinha {a} figurinhas e ganhou {b}. Quantas figurinhas ele tem agora?",
            a + b
        )


    if tipo == "adicao_desafio":

        a = random.randint(20, 100)
        b = random.randint(20, 100)
        c = random.randint(1, 30)

        return questao(
            f"Resolva: {a} + {b} + {c}",
            a + b + c
        )


    # ========================================================
    # SUBTRAÇÃO
    # ========================================================

    if tipo == "subtracao_visual":

        a = random.randint(5, 15)
        b = random.randint(1, a)

        return questao(
            f"Havia {a} balões. {b} estouraram. Quantos sobraram?",
            a - b
        )


    if tipo == "subtracao":

        a = random.randint(10, 80)
        b = random.randint(1, a)

        return questao(
            f"Quanto é {a} - {b}?",
            a - b
        )


    if tipo == "problema_subtracao":

        a = random.randint(15, 60)
        b = random.randint(1, a)

        return questao(
            f"Uma caixa tinha {a} brinquedos. Foram retirados {b}. Quantos sobraram?",
            a - b
        )


    if tipo == "subtracao_desafio":

        a = random.randint(50, 150)
        b = random.randint(10, a)

        return questao(
            f"Resolva: {a} - {b}",
            a - b
        )


    # ========================================================
    # COMPOSIÇÃO
    # ========================================================

    if tipo == "composicao_visual":

        dezenas = random.randint(1, 9)
        unidades = random.randint(0, 9)

        return questao(
            f"{dezenas} dezenas e {unidades} unidades formam qual número?",
            dezenas * 10 + unidades
        )


    if tipo in (
        "composicao",
        "decomposicao"
    ):

        numero = random.randint(10, 99)

        dezenas = numero // 10

        return questao(
            f"Quantas dezenas existem em {numero}?",
            dezenas
        )


    if tipo == "composicao_desafio":

        c = random.randint(1, 9)
        d = random.randint(0, 9)
        u = random.randint(0, 9)

        numero = c * 100 + d * 10 + u

        return questao(
            f"{c} centenas, {d} dezenas e {u} unidades formam qual número?",
            numero
        )


    # ========================================================
    # MULTIPLICAÇÃO
    # ========================================================

    if tipo == "multiplicacao_visual":

        grupos = random.randint(2, 5)
        itens = random.randint(2, 5)

        return questao(
            f"Existem {grupos} grupos com {itens} objetos em cada grupo. Quantos objetos existem?",
            grupos * itens
        )


    if tipo == "multiplicacao":

        a = random.randint(2, 10)
        b = random.randint(2, 10)

        return questao(
            f"Quanto é {a} × {b}?",
            a * b
        )


    if tipo == "multiplicacao_avancada":

        a = random.randint(10, 30)
        b = random.randint(2, 9)

        return questao(
            f"Quanto é {a} × {b}?",
            a * b
        )


    if tipo == "problema_multiplicacao":

        caixas = random.randint(2, 8)
        objetos = random.randint(2, 10)

        return questao(
            f"Há {caixas} caixas com {objetos} objetos em cada. Quantos objetos existem?",
            caixas * objetos
        )


    if tipo == "multiplicacao_desafio":

        a = random.randint(10, 50)
        b = random.randint(2, 12)

        return questao(
            f"Desafio: {a} × {b}",
            a * b
        )


    # ========================================================
    # DIVISÃO
    # ========================================================

    if tipo == "divisao_visual":

        grupos = random.randint(2, 6)
        quantidade = random.randint(2, 8)

        total = grupos * quantidade

        return questao(
            f"{total} doces serão divididos igualmente entre {grupos} crianças. Quantos cada criança recebe?",
            quantidade
        )


    if tipo == "divisao":

        resposta = random.randint(2, 12)
        divisor = random.randint(2, 10)

        total = resposta * divisor

        return questao(
            f"Quanto é {total} ÷ {divisor}?",
            resposta
        )


    if tipo == "problema_divisao":

        pessoas = random.randint(2, 8)
        quantidade = random.randint(2, 10)

        total = pessoas * quantidade

        return questao(
            f"{total} objetos foram divididos igualmente entre {pessoas} pessoas. Quantos cada uma recebeu?",
            quantidade
        )


    if tipo == "divisao_desafio":

        divisor = random.randint(2, 12)
        resposta = random.randint(5, 20)

        total = divisor * resposta

        return questao(
            f"Desafio: {total} ÷ {divisor}",
            resposta
        )


    # ========================================================
    # DOBRO / METADE
    # ========================================================

    if tipo == "dobro":

        n = random.randint(1, 30)

        return questao(
            f"Qual é o dobro de {n}?",
            n * 2
        )


    if tipo == "metade":

        n = random.randint(1, 20) * 2

        return questao(
            f"Qual é a metade de {n}?",
            n // 2
        )


    if tipo == "triplo":

        n = random.randint(1, 20)

        return questao(
            f"Qual é o triplo de {n}?",
            n * 3
        )


    if tipo == "terca":

        resposta = random.randint(1, 20)

        n = resposta * 3

        return questao(
            f"Qual é a terça parte de {n}?",
            resposta
        )


    if tipo == "dobro_metade_desafio":

        n = random.randint(2, 20)

        return questao(
            f"Qual é o dobro do triplo de {n}?",
            n * 6
        )


    # ========================================================
    # COMPARAÇÃO
    # ========================================================

    if tipo == "comparacao":

        a = random.randint(1, 100)
        b = random.randint(1, 100)

        while b == a:
            b = random.randint(1, 100)

        return questao(
            f"Qual número é maior: {a} ou {b}?",
            max(a, b)
        )


    # ========================================================
    # EQUIVALÊNCIA
    # ========================================================

    if tipo == "equivalencia":

        resultado = random.randint(5, 20)

        a = random.randint(1, resultado - 1)

        b = resultado - a

        c = random.randint(1, resultado - 1)

        return questao(
            f"{a} + {b} possui o mesmo resultado que {c} + quanto?",
            resultado - c
        )


    # ========================================================
    # DECIMAIS
    # ========================================================

    if tipo == "decimal":

        inteiro = random.randint(1, 20)

        return questao(
            f"Qual é a parte inteira do número {inteiro},5?",
            inteiro
        )


    # ========================================================
    # FIGURAS
    # ========================================================

    if tipo in (
        "figuras_nome",
        "figuras_lados",
        "figuras_planas"
    ):

        figura = random.choice([
            ("triângulo", 3),
            ("quadrado", 4),
            ("retângulo", 4)
        ])

        return questao(
            f"Quantos lados possui um {figura[0]}?",
            figura[1]
        )


    if tipo == "figuras_desafio":

        return questao(
            "Qual figura plana possui 3 lados?",
            "triângulo"
        )


    if tipo == "lados_vertices":

        figura = random.choice([
            ("triângulo", 3),
            ("quadrado", 4),
            ("pentágono", 5)
        ])

        return questao(
            f"Quantos vértices possui um {figura[0]}?",
            figura[1]
        )


    if tipo == "solidos":

        perguntas = [
            (
                "Uma bola lembra qual sólido geométrico?",
                "esfera"
            ),
            (
                "Quantas faces possui um cubo?",
                6
            )
        ]

        pergunta, resposta = random.choice(
            perguntas
        )

        return questao(
            pergunta,
            resposta
        )


    # ========================================================
    # CALENDÁRIO
    # ========================================================

    if tipo in (
        "calendario_basico",
        "calendario",
        "calendario_desafio"
    ):

        perguntas = [
            (
                "Quantos dias possui uma semana?",
                7
            ),
            (
                "Quantos meses possui um ano?",
                12
            ),
            (
                "Quantas horas possui um dia?",
                24
            )
        ]

        p, r = random.choice(perguntas)

        return questao(p, r)


    # ========================================================
    # TEMPO
    # ========================================================

    if tipo == "tempo":

        horas = random.randint(1, 8)

        return questao(
            f"{horas} horas correspondem a quantos minutos?",
            horas * 60
        )


    # ========================================================
    # DINHEIRO
    # ========================================================

    if tipo in (
        "dinheiro_basico",
        "dinheiro"
    ):

        a = random.randint(1, 20)
        b = random.randint(1, 20)

        return questao(
            f"Você possui R$ {a} e ganhou R$ {b}. Quantos reais possui agora?",
            a + b
        )


    if tipo in (
        "problema_dinheiro",
        "dinheiro_desafio"
    ):

        dinheiro = random.randint(20, 100)
        gasto = random.randint(1, dinheiro)

        return questao(
            f"Você tinha R$ {dinheiro} e gastou R$ {gasto}. Quanto sobrou?",
            dinheiro - gasto
        )


    # ========================================================
    # PROBABILIDADE
    # ========================================================

    if tipo in (
        "probabilidade_basica",
        "probabilidade"
    ):

        return questao(
            "Uma moeda possui quantos resultados possíveis ao ser lançada?",
            2
        )


    if tipo == "probabilidade_desafio":

        return questao(
            "Um dado comum possui quantos resultados possíveis?",
            6
        )


    # ========================================================
    # GRÁFICOS
    # ========================================================

    if tipo in (
        "grafico_basico",
        "grafico",
        "grafico_desafio"
    ):

        a = random.randint(1, 20)
        b = random.randint(1, 20)

        while a == b:
            b = random.randint(1, 20)

        return questao(
            f"Em um gráfico, Azul possui {a} votos e Verde possui {b}. Qual possui mais votos? Digite Azul ou Verde.",
            "Azul" if a > b else "Verde"
        )


    # ========================================================
    # COMPRIMENTO
    # ========================================================

    if tipo == "comprimento":

        metros = random.randint(1, 20)

        return questao(
            f"{metros} metros correspondem a quantos centímetros?",
            metros * 100
        )


    # ========================================================
    # MASSA
    # ========================================================

    if tipo == "massa":

        kg = random.randint(1, 10)

        return questao(
            f"{kg} kg correspondem a quantos gramas?",
            kg * 1000
        )


    # ========================================================
    # MILHAR
    # ========================================================

    if tipo == "milhar":

        milhares = random.randint(1, 9)

        return questao(
            f"{milhares} unidades de milhar representam qual número?",
            milhares * 1000
        )


    # ========================================================
    # DECOMPOSIÇÃO 4 ORDENS
    # ========================================================

    if tipo == "decomposicao4":

        numero = random.randint(1000, 9999)

        milhares = numero // 1000

        return questao(
            f"Quantas unidades de milhar existem em {numero}?",
            milhares
        )


    # ========================================================
    # QUATRO OPERAÇÕES
    # ========================================================

    if tipo == "quatro_operacoes":

        operacao = random.choice([
            "+",
            "-",
            "×",
            "÷"
        ])

        if operacao == "+":

            a = random.randint(10, 100)
            b = random.randint(10, 100)

            resposta = a + b

        elif operacao == "-":

            a = random.randint(20, 100)
            b = random.randint(1, a)

            resposta = a - b

        elif operacao == "×":

            a = random.randint(2, 12)
            b = random.randint(2, 12)

            resposta = a * b

        else:

            resposta = random.randint(2, 12)
            b = random.randint(2, 10)

            a = resposta * b

        return questao(
            f"Resolva: {a} {operacao} {b}",
            resposta
        )


    # ========================================================
    # FRAÇÃO
    # ========================================================

    if tipo in (
        "fracao_basica",
        "fracao"
    ):

        denominador = random.randint(2, 10)
        numerador = random.randint(
            1,
            denominador - 1
        )

        escolha = random.choice([
            "numerador",
            "denominador"
        ])

        if escolha == "numerador":

            return questao(
                f"Na fração {numerador}/{denominador}, qual é o numerador?",
                numerador
            )

        return questao(
            f"Na fração {numerador}/{denominador}, qual é o denominador?",
            denominador
        )


    if tipo == "fracao_desafio":

        denominador = random.randint(2, 10)

        return questao(
            f"Uma pizza foi dividida em {denominador} partes iguais. Uma parte representa 1 sobre quanto?",
            denominador
        )


    # ========================================================
    # POLÍGONOS
    # ========================================================

    if tipo == "poligonos":

        poligono = random.choice([
            ("triângulo", 3),
            ("quadrilátero", 4),
            ("pentágono", 5),
            ("hexágono", 6)
        ])

        return questao(
            f"Quantos lados possui um {poligono[0]}?",
            poligono[1]
        )


    # ========================================================
    # TEMPERATURA
    # ========================================================

    if tipo == "temperatura":

        temperatura = random.randint(
            10,
            40
        )

        aumento = random.randint(
            1,
            10
        )

        return questao(
            f"A temperatura era {temperatura} °C e aumentou {aumento} graus. Qual é a nova temperatura?",
            temperatura + aumento
        )


    # ========================================================
    # ÂNGULOS
    # ========================================================

    if tipo == "angulos":

        angulo = random.choice([
            30,
            45,
            90,
            120,
            150
        ])

        if angulo < 90:

            resposta = "agudo"

        elif angulo == 90:

            resposta = "reto"

        else:

            resposta = "obtuso"

        return questao(
            f"Um ângulo de {angulo}° é agudo, reto ou obtuso?",
            resposta
        )


    # ========================================================
    # PERÍMETRO / ÁREA
    # ========================================================

    if tipo == "perimetro":

        largura = random.randint(2, 10)
        altura = random.randint(2, 10)

        return questao(
            f"Um retângulo mede {largura} por {altura}. Qual é o perímetro?",
            2 * (largura + altura)
        )


    if tipo == "area":

        largura = random.randint(2, 10)
        altura = random.randint(2, 10)

        return questao(
            f"Um retângulo mede {largura} por {altura}. Qual é a área?",
            largura * altura
        )


    if tipo == "perimetro_area":

        return gerar_questao(
            random.choice([
                "perimetro",
                "area"
            ])
        )


    # ========================================================
    # PROPORÇÃO
    # ========================================================

    if tipo == "proporcao":

        quantidade = random.randint(
            2,
            6
        )

        preco = random.randint(
            2,
            10
        )

        nova_quantidade = quantidade * 2

        return questao(
            f"{quantidade} itens custam R$ {quantidade * preco}. Quanto custam {nova_quantidade} itens?",
            nova_quantidade * preco
        )


    # ========================================================
    # PLANO CARTESIANO
    # ========================================================

    if tipo == "plano_cartesiano":

        x = random.randint(
            0,
            10
        )

        y = random.randint(
            0,
            10
        )

        return questao(
            f"No ponto ({x}, {y}), qual é a coordenada X?",
            x
        )


    # ========================================================
    # POLIEDROS
    # ========================================================

    if tipo == "poliedros":

        return questao(
            "Quantas faces possui um cubo?",
            6
        )


    # ========================================================
    # CONVERSÃO
    # ========================================================

    if tipo == "conversao":

        metros = random.randint(
            1,
            20
        )

        return questao(
            f"{metros} metros equivalem a quantos centímetros?",
            metros * 100
        )


    # ========================================================
    # VOLUME
    # ========================================================

    if tipo == "volume":

        a = random.randint(2, 6)
        b = random.randint(2, 6)
        c = random.randint(2, 6)

        return questao(
            f"Um bloco mede {a} × {b} × {c}. Qual é seu volume?",
            a * b * c
        )


    # ========================================================
    # FALLBACK
    # ========================================================

    a = random.randint(1, 10)
    b = random.randint(1, 10)

    return questao(
        f"Quanto é {a} + {b}?",
        a + b
    )