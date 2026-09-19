import random


# ============================================================
# FOTOS REAIS
# ============================================================
# Não precisa criar arquivos de imagem agora.
#
# Posteriormente você pode trocar:
#
# https://loremflickr.com/...
#
# por:
#
# /static/img/exercicios/bola.jpg
#
# sem alterar o restante do sistema.
# ============================================================

IMAGENS_REAIS = {

    "bola":
        "https://loremflickr.com/640/480/soccerball?lock=101",

    "caixa":
        "https://loremflickr.com/640/480/cardboardbox?lock=102",

    "lata":
        "https://loremflickr.com/640/480/tincan?lock=103",

    "cone":
        "https://loremflickr.com/640/480/trafficcone?lock=104",

    "roda":
        "https://loremflickr.com/640/480/wheel?lock=105",

    "janela":
        "https://loremflickr.com/640/480/squarewindow?lock=106",

    "placa_triangular":
        "https://loremflickr.com/640/480/triangleroadsign?lock=107",

    "livro":
        "https://loremflickr.com/640/480/book?lock=108",

    "regua":
        "https://loremflickr.com/640/480/ruler?lock=109",

    "balanca":
        "https://loremflickr.com/640/480/kitchenscale?lock=110",

    "relogio":
        "https://loremflickr.com/640/480/clock?lock=111",

    "dado":
        "https://loremflickr.com/640/480/dice?lock=112",

    "moeda":
        "https://loremflickr.com/640/480/coin?lock=113",

    "maca":
        "https://loremflickr.com/640/480/apple?lock=114",

    "banana":
        "https://loremflickr.com/640/480/banana?lock=115",
}


# ============================================================
# AUXILIARES
# ============================================================

def embaralhar(itens):

    itens = list(itens)

    random.shuffle(itens)

    return itens


def questao(
    pergunta,
    resposta,
    tipo_ui="numero",
    alternativas=None,
    visual=None,
    itens=None,
    esquerda=None,
    direita=None,
    instrucao=None
):

    dados = {

        "tipo_ui":
            tipo_ui,

        "pergunta":
            str(pergunta),

        "resposta":
            resposta
    }


    if alternativas is not None:

        dados[
            "alternativas"
        ] = alternativas


    if visual is not None:

        dados[
            "visual"
        ] = visual


    if itens is not None:

        dados[
            "itens"
        ] = itens


    if esquerda is not None:

        dados[
            "esquerda"
        ] = esquerda


    if direita is not None:

        dados[
            "direita"
        ] = direita


    if instrucao:

        dados[
            "instrucao"
        ] = instrucao


    return dados


# ============================================================
# ALTERNATIVAS NUMÉRICAS
# ============================================================

def alternativas_numericas(
    correta,
    quantidade=4
):

    correta = int(
        correta
    )

    valores = {
        correta
    }


    margem = max(
        3,
        min(
            100,
            abs(correta) // 5 + 2
        )
    )


    tentativas = 0


    while (
        len(valores) < quantidade
        and
        tentativas < 100
    ):

        tentativas += 1


        candidato = (
            correta
            +
            random.choice(
                (
                    -1,
                    1
                )
            )
            *
            random.randint(
                1,
                margem
            )
        )


        if candidato >= 0:

            valores.add(
                candidato
            )


    while len(valores) < quantidade:

        valores.add(
            max(
                0,
                correta
                +
                len(valores)
                +
                1
            )
        )


    return embaralhar(
        [
            {
                "id":
                    str(valor),

                "texto":
                    str(valor)
            }

            for valor
            in valores
        ]
    )


# ============================================================
# ALTERNATIVAS DE TEXTO
# ============================================================

def alternativas_texto(
    correta,
    erradas
):

    correta = str(
        correta
    )


    valores = [
        correta
    ]


    existentes = {
        correta.casefold()
    }


    for item in erradas:

        item = str(
            item
        )


        chave = (
            item.casefold()
        )


        if chave not in existentes:

            existentes.add(
                chave
            )

            valores.append(
                item
            )


    return embaralhar(
        [
            {
                "id":
                    valor,

                "texto":
                    valor
            }

            for valor
            in valores[:4]
        ]
    )


# ============================================================
# ESCOLHER TIPO DE INTERAÇÃO
# ============================================================

def escolher_interacao(
    interacoes,
    suportadas,
    padrao
):

    disponiveis = [

        interacao

        for interacao
        in (
            interacoes
            or []
        )

        if interacao
        in suportadas
    ]


    if disponiveis:

        return random.choice(
            disponiveis
        )


    return padrao


# ============================================================
# QUESTÃO NUMÉRICA DINÂMICA
# ============================================================

def numerica(
    pergunta,
    resposta,
    interacoes=None,
    visual=None,
    suportadas=(
        "numero",
        "multipla_escolha",
        "verdadeiro_falso"
    )
):

    modo = escolher_interacao(

        interacoes,

        suportadas,

        "multipla_escolha"
    )


    # --------------------------------------------------------
    # CAMPO
    # --------------------------------------------------------

    if modo == "numero":

        return questao(

            pergunta,

            str(
                resposta
            ),

            "numero",

            visual=visual
        )


    # --------------------------------------------------------
    # VERDADEIRO / FALSO
    # --------------------------------------------------------

    if modo == "verdadeiro_falso":

        correta = int(
            resposta
        )


        mostrar_correta = (
            random.choice(
                (
                    True,
                    False
                )
            )
        )


        if mostrar_correta:

            palpite = correta

        else:

            palpite = max(

                0,

                correta
                +
                random.choice(
                    (
                        -3,
                        -2,
                        -1,
                        1,
                        2,
                        3
                    )
                )
            )


        return questao(

            (
                f"{pergunta} "
                f"A resposta é {palpite}?"
            ),

            (
                "verdadeiro"
                if mostrar_correta
                else "falso"
            ),

            "verdadeiro_falso",

            alternativas=[
                {
                    "id":
                        "verdadeiro",

                    "texto":
                        "Verdadeiro"
                },

                {
                    "id":
                        "falso",

                    "texto":
                        "Falso"
                }
            ],

            visual=visual
        )


    # --------------------------------------------------------
    # CARDS
    # --------------------------------------------------------

    return questao(

        pergunta,

        str(
            resposta
        ),

        "multipla_escolha",

        alternativas=(
            alternativas_numericas(
                resposta
            )
        ),

        visual=visual
    )


# ============================================================
# QUESTÃO DE TEXTO
# ============================================================

def textual(
    pergunta,
    resposta,
    erradas,
    interacoes=None,
    visual=None
):

    modo = escolher_interacao(

        interacoes,

        (
            "multipla_escolha",
            "numero"
        ),

        "multipla_escolha"
    )


    if modo == "numero":

        return questao(

            pergunta,

            str(
                resposta
            ),

            "numero",

            visual=visual
        )


    return questao(

        pergunta,

        str(
            resposta
        ),

        "multipla_escolha",

        alternativas=(
            alternativas_texto(
                resposta,
                erradas
            )
        ),

        visual=visual
    )


# ============================================================
# ESCOLHA COM FOTOS
# ============================================================

def imagem_escolha(
    pergunta,
    correta,
    opcoes
):

    alternativas = []


    for item in opcoes:

        alternativas.append(
            {
                "id":
                    item["id"],

                "texto":
                    item.get(
                        "texto",
                        ""
                    ),

                "imagem":
                    item["imagem"],

                "fallback":
                    item.get(
                        "fallback",
                        "🖼️"
                    )
            }
        )


    return questao(

        pergunta,

        correta,

        "imagem_escolha",

        alternativas=(
            embaralhar(
                alternativas
            )
        )
    )


# ============================================================
# ASSOCIAÇÃO DE OPERAÇÕES
# ============================================================

def associacao_operacoes():

    resultados = random.sample(

        range(
            5,
            21
        ),

        3
    )


    esquerda = []

    direita = []

    resposta = {}


    for indice, resultado in enumerate(
        resultados,
        start=1
    ):

        a = random.randint(
            1,
            resultado - 1
        )

        b = (
            resultado -
            a
        )


        id_esquerda = (
            f"e{indice}"
        )

        id_direita = (
            f"r{resultado}"
        )


        esquerda.append(
            {
                "id":
                    id_esquerda,

                "texto":
                    f"{a} + {b}"
            }
        )


        direita.append(
            {
                "id":
                    id_direita,

                "texto":
                    str(resultado)
            }
        )


        resposta[
            id_esquerda
        ] = id_direita


    return questao(

        "Associe cada operação ao resultado correto.",

        resposta,

        "associacao",

        esquerda=esquerda,

        direita=(
            embaralhar(
                direita
            )
        )
    )


# ============================================================
# ASSOCIAÇÃO DE FORMAS
# ============================================================

def associacao_formas():

    esquerda = [

        {
            "id":
                "tri",

            "texto":
                "△"
        },

        {
            "id":
                "qua",

            "texto":
                "□"
        },

        {
            "id":
                "cir",

            "texto":
                "○"
        }
    ]


    direita = [

        {
            "id":
                "triangulo",

            "texto":
                "Triângulo"
        },

        {
            "id":
                "quadrado",

            "texto":
                "Quadrado"
        },

        {
            "id":
                "circulo",

            "texto":
                "Círculo"
        }
    ]


    return questao(

        "Associe cada figura ao nome correto.",

        {
            "tri":
                "triangulo",

            "qua":
                "quadrado",

            "cir":
                "circulo"
        },

        "associacao",

        esquerda=esquerda,

        direita=(
            embaralhar(
                direita
            )
        )
    )


# ============================================================
# ORDENAÇÃO
# ============================================================

def ordenacao_numeros(
    limite=100
):

    valores = random.sample(

        range(
            1,
            limite + 1
        ),

        4
    )


    return questao(

        "Coloque os números do menor para o maior.",

        [
            str(valor)

            for valor
            in sorted(
                valores
            )
        ],

        "ordenacao",

        itens=(
            embaralhar(
                [
                    {
                        "id":
                            str(valor),

                        "texto":
                            str(valor)
                    }

                    for valor
                    in valores
                ]
            )
        )
    )


# ============================================================
# GERADOR PRINCIPAL
# ============================================================

def gerar_questao(
    tipo,
    interacoes=None
):

    # ========================================================
    # ADIÇÃO VISUAL
    # ========================================================

    if tipo == "adicao_visual":

        a = random.randint(
            1,
            5
        )

        b = random.randint(
            1,
            5
        )


        return numerica(

            (
                f"Você tinha {a} estrelas "
                f"e ganhou mais {b}. "
                f"Quantas estrelas tem agora?"
            ),

            a + b,

            interacoes,

            {
                "tipo":
                    "grupos",

                "icone":
                    "⭐",

                "grupos":
                    [
                        a,
                        b
                    ]
            },

            (
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # ADIÇÃO
    # ========================================================

    if tipo == "adicao":

        a = random.randint(
            5,
            50
        )

        b = random.randint(
            1,
            40
        )


        return numerica(

            f"Quanto é {a} + {b}?",

            a + b,

            interacoes
        )


    # ========================================================
    # PROBLEMA DE ADIÇÃO
    # ========================================================

    if tipo == "problema_adicao":

        a = random.randint(
            2,
            30
        )

        b = random.randint(
            2,
            30
        )


        return numerica(

            (
                f"Lucas tinha {a} figurinhas "
                f"e ganhou {b}. "
                f"Quantas figurinhas ele tem agora?"
            ),

            a + b,

            interacoes,

            {
                "tipo":
                    "grupos",

                "icone":
                    "🟦",

                "grupos":
                    [
                        a,
                        b
                    ]
            },

            (
                "numero",
                "multipla_escolha"
            )
        )


    if tipo == "adicao_desafio":

        a = random.randint(
            20,
            100
        )

        b = random.randint(
            20,
            100
        )

        c = random.randint(
            1,
            30
        )


        return numerica(

            f"Resolva: {a} + {b} + {c}",

            a + b + c,

            interacoes,

            suportadas=(
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # SUBTRAÇÃO VISUAL
    # ========================================================

    if tipo == "subtracao_visual":

        a = random.randint(
            5,
            15
        )

        b = random.randint(
            1,
            a
        )


        return numerica(

            (
                f"Havia {a} balões. "
                f"{b} estouraram. "
                f"Quantos sobraram?"
            ),

            a - b,

            interacoes,

            {
                "tipo":
                    "subtracao_objetos",

                "icone":
                    "🎈",

                "total":
                    a,

                "retirados":
                    b
            },

            (
                "numero",
                "multipla_escolha"
            )
        )


    if tipo == "subtracao":

        a = random.randint(
            10,
            80
        )

        b = random.randint(
            1,
            a
        )


        return numerica(

            f"Quanto é {a} - {b}?",

            a - b,

            interacoes
        )


    if tipo == "problema_subtracao":

        a = random.randint(
            15,
            60
        )

        b = random.randint(
            1,
            a
        )


        return numerica(

            (
                f"Uma caixa tinha {a} brinquedos. "
                f"Foram retirados {b}. "
                f"Quantos sobraram?"
            ),

            a - b,

            interacoes,

            suportadas=(
                "numero",
                "multipla_escolha"
            )
        )


    if tipo == "subtracao_desafio":

        a = random.randint(
            50,
            150
        )

        b = random.randint(
            10,
            a
        )


        return numerica(

            f"Resolva: {a} - {b}",

            a - b,

            interacoes,

            suportadas=(
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # COMPOSIÇÃO
    # ========================================================

    if tipo == "composicao_visual":

        dezenas = random.randint(
            1,
            9
        )

        unidades = random.randint(
            0,
            9
        )


        return numerica(

            (
                f"{dezenas} dezenas e "
                f"{unidades} unidades "
                f"formam qual número?"
            ),

            (
                dezenas * 10
                +
                unidades
            ),

            interacoes,

            {
                "tipo":
                    "material_dourado",

                "dezenas":
                    dezenas,

                "unidades":
                    unidades
            },

            (
                "numero",
                "multipla_escolha"
            )
        )


    if tipo in (
        "composicao",
        "decomposicao"
    ):

        valor = random.randint(
            10,
            99
        )


        return numerica(

            (
                f"Quantas dezenas "
                f"existem em {valor}?"
            ),

            valor // 10,

            interacoes,

            {
                "tipo":
                    "material_dourado",

                "dezenas":
                    valor // 10,

                "unidades":
                    valor % 10
            },

            (
                "numero",
                "multipla_escolha"
            )
        )


    if tipo == "composicao_desafio":

        centenas = random.randint(
            1,
            9
        )

        dezenas = random.randint(
            0,
            9
        )

        unidades = random.randint(
            0,
            9
        )


        return numerica(

            (
                f"{centenas} centenas, "
                f"{dezenas} dezenas e "
                f"{unidades} unidades "
                f"formam qual número?"
            ),

            (
                centenas * 100
                +
                dezenas * 10
                +
                unidades
            ),

            interacoes,

            suportadas=(
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # MULTIPLICAÇÃO
    # ========================================================

    if tipo == "multiplicacao_visual":

        grupos = random.randint(
            2,
            5
        )

        itens = random.randint(
            2,
            5
        )


        return numerica(

            "Observe os grupos. Quantos objetos existem ao todo?",

            grupos * itens,

            interacoes,

            {
                "tipo":
                    "multiplicacao_grupos",

                "icone":
                    random.choice(
                        (
                            "🍎",
                            "⭐",
                            "⚽",
                            "🟣"
                        )
                    ),

                "grupos":
                    grupos,

                "itens":
                    itens
            },

            (
                "numero",
                "multipla_escolha"
            )
        )


    if tipo == "multiplicacao":

        a = random.randint(
            2,
            10
        )

        b = random.randint(
            2,
            10
        )


        return numerica(

            f"Quanto é {a} × {b}?",

            a * b,

            interacoes
        )


    if tipo == "multiplicacao_avancada":

        a = random.randint(
            10,
            30
        )

        b = random.randint(
            2,
            9
        )


        return numerica(

            f"Quanto é {a} × {b}?",

            a * b,

            interacoes,

            suportadas=(
                "numero",
                "multipla_escolha"
            )
        )


    if tipo == "problema_multiplicacao":

        caixas = random.randint(
            2,
            8
        )

        objetos = random.randint(
            2,
            10
        )


        return numerica(

            (
                f"Há {caixas} caixas "
                f"com {objetos} objetos em cada. "
                f"Quantos objetos existem?"
            ),

            caixas * objetos,

            interacoes,

            {
                "tipo":
                    "multiplicacao_grupos",

                "icone":
                    "🔵",

                "grupos":
                    caixas,

                "itens":
                    objetos
            },

            (
                "numero",
                "multipla_escolha"
            )
        )


    if tipo == "multiplicacao_desafio":

        a = random.randint(
            10,
            50
        )

        b = random.randint(
            2,
            12
        )


        return numerica(

            f"Desafio: {a} × {b}",

            a * b,

            interacoes,

            suportadas=(
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # DIVISÃO
    # ========================================================

    if tipo == "divisao_visual":

        grupos = random.randint(
            2,
            6
        )

        por_grupo = random.randint(
            2,
            8
        )

        total = (
            grupos *
            por_grupo
        )


        return numerica(

            (
                f"{total} doces serão divididos "
                f"igualmente entre {grupos} crianças. "
                f"Quantos cada criança recebe?"
            ),

            por_grupo,

            interacoes,

            {
                "tipo":
                    "divisao",

                "icone":
                    "🍬",

                "total":
                    total,

                "grupos":
                    grupos
            },

            (
                "numero",
                "multipla_escolha"
            )
        )


    if tipo == "divisao":

        resposta = random.randint(
            2,
            12
        )

        divisor = random.randint(
            2,
            10
        )


        return numerica(

            (
                f"Quanto é "
                f"{resposta * divisor} ÷ {divisor}?"
            ),

            resposta,

            interacoes
        )


    if tipo == "problema_divisao":

        pessoas = random.randint(
            2,
            8
        )

        quantidade = random.randint(
            2,
            10
        )


        return numerica(

            (
                f"{pessoas * quantidade} objetos "
                f"foram divididos igualmente "
                f"entre {pessoas} pessoas. "
                f"Quantos cada uma recebeu?"
            ),

            quantidade,

            interacoes,

            suportadas=(
                "numero",
                "multipla_escolha"
            )
        )


    if tipo == "divisao_desafio":

        divisor = random.randint(
            2,
            12
        )

        resposta = random.randint(
            5,
            20
        )


        return numerica(

            (
                f"Desafio: "
                f"{divisor * resposta} ÷ {divisor}"
            ),

            resposta,

            interacoes,

            suportadas=(
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # DOBRO / METADE / TRIPLO
    # ========================================================

    if tipo == "dobro":

        valor = random.randint(
            1,
            30
        )


        return numerica(

            f"Qual é o dobro de {valor}?",

            valor * 2,

            interacoes,

            suportadas=(
                "numero",
                "multipla_escolha"
            )
        )


    if tipo == "metade":

        valor = (
            random.randint(
                1,
                20
            )
            *
            2
        )


        return numerica(

            f"Qual é a metade de {valor}?",

            valor // 2,

            interacoes,

            suportadas=(
                "numero",
                "multipla_escolha"
            )
        )


    if tipo == "triplo":

        valor = random.randint(
            1,
            20
        )


        return numerica(

            f"Qual é o triplo de {valor}?",

            valor * 3,

            interacoes,

            suportadas=(
                "numero",
                "multipla_escolha"
            )
        )


    if tipo == "terca":

        resposta = random.randint(
            1,
            20
        )


        return numerica(

            (
                f"Qual é a terça parte "
                f"de {resposta * 3}?"
            ),

            resposta,

            interacoes,

            suportadas=(
                "numero",
                "multipla_escolha"
            )
        )


    if tipo == "dobro_metade_desafio":

        valor = random.randint(
            2,
            20
        )


        return numerica(

            (
                f"Qual é o dobro do "
                f"triplo de {valor}?"
            ),

            valor * 6,

            interacoes,

            suportadas=(
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # COMPARAÇÃO
    # ========================================================

    if tipo == "comparacao":

        modo = escolher_interacao(

            interacoes,

            (
                "multipla_escolha",
                "ordenacao"
            ),

            "multipla_escolha"
        )


        if modo == "ordenacao":

            return ordenacao_numeros(
                100
            )


        a, b = random.sample(

            range(
                1,
                101
            ),

            2
        )


        return questao(

            "Selecione o maior número.",

            str(
                max(
                    a,
                    b
                )
            ),

            "multipla_escolha",

            alternativas=(
                embaralhar(
                    [
                        {
                            "id":
                                str(a),

                            "texto":
                                str(a)
                        },

                        {
                            "id":
                                str(b),

                            "texto":
                                str(b)
                        }
                    ]
                )
            )
        )


    # ========================================================
    # EQUIVALÊNCIA
    # ========================================================

    if tipo == "equivalencia":

        modo = escolher_interacao(

            interacoes,

            (
                "multipla_escolha",
                "associacao"
            ),

            "multipla_escolha"
        )


        if modo == "associacao":

            return associacao_operacoes()


        resultado = random.randint(
            5,
            20
        )

        a = random.randint(
            1,
            resultado - 1
        )

        b = (
            resultado -
            a
        )

        c = random.randint(
            1,
            resultado - 1
        )


        return numerica(

            (
                f"{a} + {b} possui o mesmo "
                f"resultado que {c} + quanto?"
            ),

            resultado - c,

            interacoes,

            suportadas=(
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # DECIMAL
    # ========================================================

    if tipo == "decimal":

        inteiro = random.randint(
            1,
            20
        )


        return numerica(

            (
                f"Qual é a parte inteira "
                f"do número {inteiro},5?"
            ),

            inteiro,

            interacoes,

            suportadas=(
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # FIGURAS - FOTOS REAIS
    # ========================================================

    if tipo == "figuras_nome":

        modo = escolher_interacao(

            interacoes,

            (
                "multipla_escolha",
                "imagem_escolha",
                "associacao"
            ),

            "multipla_escolha"
        )


        if modo == "associacao":

            return associacao_formas()


        if modo == "imagem_escolha":

            alvo = random.choice(
                (
                    "triângulo",
                    "quadrado",
                    "círculo",
                    "retângulo"
                )
            )


            return imagem_escolha(

                (
                    f"Qual foto lembra "
                    f"mais um {alvo}?"
                ),

                alvo,

                [
                    {
                        "id":
                            "triângulo",

                        "texto":
                            "Triângulo",

                        "imagem":
                            IMAGENS_REAIS[
                                "placa_triangular"
                            ],

                        "fallback":
                            "🔺"
                    },

                    {
                        "id":
                            "quadrado",

                        "texto":
                            "Quadrado",

                        "imagem":
                            IMAGENS_REAIS[
                                "janela"
                            ],

                        "fallback":
                            "◼️"
                    },

                    {
                        "id":
                            "círculo",

                        "texto":
                            "Círculo",

                        "imagem":
                            IMAGENS_REAIS[
                                "roda"
                            ],

                        "fallback":
                            "⭕"
                    },

                    {
                        "id":
                            "retângulo",

                        "texto":
                            "Retângulo",

                        "imagem":
                            IMAGENS_REAIS[
                                "livro"
                            ],

                        "fallback":
                            "▭"
                    }
                ]
            )


        nome, forma = random.choice(
            (
                (
                    "triângulo",
                    "triangulo"
                ),

                (
                    "quadrado",
                    "quadrado"
                ),

                (
                    "retângulo",
                    "retangulo"
                ),

                (
                    "pentágono",
                    "pentagono"
                )
            )
        )


        return textual(

            "Qual é o nome desta figura?",

            nome,

            (
                "triângulo",
                "quadrado",
                "retângulo",
                "pentágono"
            ),

            interacoes,

            {
                "tipo":
                    "forma",

                "forma":
                    forma
            }
        )


    if tipo in (
        "figuras_lados",
        "figuras_planas"
    ):

        nome, lados, forma = random.choice(
            (
                (
                    "triângulo",
                    3,
                    "triangulo"
                ),

                (
                    "quadrado",
                    4,
                    "quadrado"
                ),

                (
                    "retângulo",
                    4,
                    "retangulo"
                ),

                (
                    "pentágono",
                    5,
                    "pentagono"
                )
            )
        )


        return numerica(

            (
                f"Quantos lados possui "
                f"este {nome}?"
            ),

            lados,

            interacoes,

            {
                "tipo":
                    "forma",

                "forma":
                    forma
            },

            (
                "numero",
                "multipla_escolha"
            )
        )


    if tipo == "figuras_desafio":

        return textual(

            "Qual figura plana possui 3 lados?",

            "triângulo",

            (
                "quadrado",
                "retângulo",
                "círculo"
            ),

            interacoes
        )


    if tipo == "lados_vertices":

        nome, vertices, forma = random.choice(
            (
                (
                    "triângulo",
                    3,
                    "triangulo"
                ),

                (
                    "quadrado",
                    4,
                    "quadrado"
                ),

                (
                    "pentágono",
                    5,
                    "pentagono"
                )
            )
        )


        return numerica(

            (
                f"Quantos vértices possui "
                f"este {nome}?"
            ),

            vertices,

            interacoes,

            {
                "tipo":
                    "forma",

                "forma":
                    forma
            },

            (
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # SÓLIDOS - FOTOS REAIS
    # ========================================================

    if tipo == "solidos":

        modo = escolher_interacao(

            interacoes,

            (
                "imagem_escolha",
                "multipla_escolha"
            ),

            "imagem_escolha"
        )


        if modo == "imagem_escolha":

            alvo = random.choice(
                (
                    "esfera",
                    "cubo",
                    "cilindro",
                    "cone"
                )
            )


            return imagem_escolha(

                (
                    f"Qual foto representa "
                    f"melhor um {alvo}?"
                ),

                alvo,

                [
                    {
                        "id":
                            "esfera",

                        "texto":
                            "Esfera",

                        "imagem":
                            IMAGENS_REAIS[
                                "bola"
                            ],

                        "fallback":
                            "⚽"
                    },

                    {
                        "id":
                            "cubo",

                        "texto":
                            "Cubo",

                        "imagem":
                            IMAGENS_REAIS[
                                "caixa"
                            ],

                        "fallback":
                            "📦"
                    },

                    {
                        "id":
                            "cilindro",

                        "texto":
                            "Cilindro",

                        "imagem":
                            IMAGENS_REAIS[
                                "lata"
                            ],

                        "fallback":
                            "🥫"
                    },

                    {
                        "id":
                            "cone",

                        "texto":
                            "Cone",

                        "imagem":
                            IMAGENS_REAIS[
                                "cone"
                            ],

                        "fallback":
                            "🔺"
                    }
                ]
            )


        objeto, resposta, forma = (
            random.choice(
                (
                    (
                        "bola",
                        "esfera",
                        "esfera"
                    ),

                    (
                        "caixa",
                        "cubo",
                        "cubo"
                    ),

                    (
                        "lata",
                        "cilindro",
                        "cilindro"
                    )
                )
            )
        )


        return textual(

            (
                f"Um objeto como {objeto} "
                f"lembra qual sólido geométrico?"
            ),

            resposta,

            (
                "cubo",
                "esfera",
                "cilindro",
                "cone"
            ),

            interacoes,

            {
                "tipo":
                    "solido",

                "forma":
                    forma
            }
        )


    # ========================================================
    # CALENDÁRIO
    # ========================================================

    if tipo in (
        "calendario_basico",
        "calendario",
        "calendario_desafio"
    ):

        pergunta, resposta = random.choice(
            (
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
            )
        )


        return numerica(

            pergunta,

            resposta,

            interacoes,

            suportadas=(
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # RELÓGIO
    # ========================================================

    if tipo == "tempo":

        if random.random() < 0.55:

            hora = random.randint(
                1,
                12
            )

            minuto = random.choice(
                (
                    0,
                    15,
                    30,
                    45
                )
            )


            correta = (
                f"{hora:02d}:"
                f"{minuto:02d}"
            )


            erradas = set()


            while len(erradas) < 3:

                h = random.randint(
                    1,
                    12
                )

                m = random.choice(
                    (
                        0,
                        15,
                        30,
                        45
                    )
                )


                candidato = (
                    f"{h:02d}:"
                    f"{m:02d}"
                )


                if candidato != correta:

                    erradas.add(
                        candidato
                    )


            return textual(

                "Que horas o relógio está marcando?",

                correta,

                list(
                    erradas
                ),

                interacoes,

                {
                    "tipo":
                        "relogio",

                    "hora":
                        hora,

                    "minuto":
                        minuto
                }
            )


        horas = random.randint(
            1,
            8
        )


        return numerica(

            (
                f"{horas} horas correspondem "
                f"a quantos minutos?"
            ),

            horas * 60,

            interacoes,

            suportadas=(
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # DINHEIRO
    # ========================================================

    if tipo in (
        "dinheiro_basico",
        "dinheiro"
    ):

        valores = random.choices(

            (
                1,
                2,
                5,
                10
            ),

            k=random.randint(
                2,
                4
            )
        )


        return numerica(

            "Quanto dinheiro há ao todo?",

            sum(
                valores
            ),

            interacoes,

            {
                "tipo":
                    "dinheiro",

                "valores":
                    valores
            },

            (
                "numero",
                "multipla_escolha"
            )
        )


    if tipo in (
        "problema_dinheiro",
        "dinheiro_desafio"
    ):

        dinheiro = random.randint(
            20,
            100
        )

        gasto = random.randint(
            1,
            dinheiro
        )


        return numerica(

            (
                f"Você tinha R$ {dinheiro} "
                f"e gastou R$ {gasto}. "
                f"Quanto sobrou?"
            ),

            dinheiro - gasto,

            interacoes,

            suportadas=(
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # PROBABILIDADE - FOTOS
    # ========================================================

    if tipo in (
        "probabilidade_basica",
        "probabilidade"
    ):

        modo = escolher_interacao(

            interacoes,

            (
                "imagem_escolha",
                "multipla_escolha"
            ),

            "multipla_escolha"
        )


        if modo == "imagem_escolha":

            return imagem_escolha(

                (
                    "Qual foto mostra um objeto "
                    "que, ao ser lançado, possui "
                    "dois resultados principais: "
                    "cara ou coroa?"
                ),

                "moeda",

                [
                    {
                        "id":
                            "moeda",

                        "texto":
                            "Moeda",

                        "imagem":
                            IMAGENS_REAIS[
                                "moeda"
                            ],

                        "fallback":
                            "🪙"
                    },

                    {
                        "id":
                            "dado",

                        "texto":
                            "Dado",

                        "imagem":
                            IMAGENS_REAIS[
                                "dado"
                            ],

                        "fallback":
                            "🎲"
                    },

                    {
                        "id":
                            "bola",

                        "texto":
                            "Bola",

                        "imagem":
                            IMAGENS_REAIS[
                                "bola"
                            ],

                        "fallback":
                            "⚽"
                    },

                    {
                        "id":
                            "relogio",

                        "texto":
                            "Relógio",

                        "imagem":
                            IMAGENS_REAIS[
                                "relogio"
                            ],

                        "fallback":
                            "🕒"
                    }
                ]
            )


        return numerica(

            (
                "Uma moeda possui quantos "
                "resultados possíveis ao ser lançada?"
            ),

            2,

            interacoes,

            {
                "tipo":
                    "moeda"
            },

            (
                "numero",
                "multipla_escolha"
            )
        )


    if tipo == "probabilidade_desafio":

        return numerica(

            (
                "Um dado comum possui quantos "
                "resultados possíveis?"
            ),

            6,

            interacoes,

            {
                "tipo":
                    "dado"
            },

            (
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # GRÁFICOS
    # ========================================================

    if tipo in (
        "grafico_basico",
        "grafico",
        "grafico_desafio"
    ):

        dados = {

            "Maçã":
                random.randint(
                    2,
                    10
                ),

            "Banana":
                random.randint(
                    2,
                    10
                ),

            "Uva":
                random.randint(
                    2,
                    10
                ),

            "Laranja":
                random.randint(
                    2,
                    10
                )
        }


        maior = max(
            dados.values()
        )


        if (
            list(
                dados.values()
            ).count(
                maior
            )
            >
            1
        ):

            chave = random.choice(
                list(
                    dados.keys()
                )
            )

            dados[chave] = (
                maior +
                2
            )


        resposta = max(

            dados,

            key=dados.get
        )


        return textual(

            (
                "Observe o gráfico. "
                "Qual fruta teve a maior quantidade?"
            ),

            resposta,

            [
                nome

                for nome
                in dados

                if nome != resposta
            ],

            interacoes,

            {
                "tipo":
                    "grafico_barras",

                "dados":
                    dados
            }
        )


    # ========================================================
    # COMPRIMENTO - FOTO REAL
    # ========================================================

    if tipo == "comprimento":

        modo = escolher_interacao(

            interacoes,

            (
                "imagem_escolha",
                "multipla_escolha",
                "numero"
            ),

            "multipla_escolha"
        )


        if modo == "imagem_escolha":

            return imagem_escolha(

                "Qual objeto é apropriado para medir comprimento?",

                "regua",

                [
                    {
                        "id":
                            "regua",

                        "texto":
                            "Régua",

                        "imagem":
                            IMAGENS_REAIS[
                                "regua"
                            ],

                        "fallback":
                            "📏"
                    },

                    {
                        "id":
                            "balanca",

                        "texto":
                            "Balança",

                        "imagem":
                            IMAGENS_REAIS[
                                "balanca"
                            ],

                        "fallback":
                            "⚖️"
                    },

                    {
                        "id":
                            "relogio",

                        "texto":
                            "Relógio",

                        "imagem":
                            IMAGENS_REAIS[
                                "relogio"
                            ],

                        "fallback":
                            "🕒"
                    },

                    {
                        "id":
                            "bola",

                        "texto":
                            "Bola",

                        "imagem":
                            IMAGENS_REAIS[
                                "bola"
                            ],

                        "fallback":
                            "⚽"
                    }
                ]
            )


        metros = random.randint(
            1,
            20
        )


        return numerica(

            (
                f"{metros} metros correspondem "
                f"a quantos centímetros?"
            ),

            metros * 100,

            [
                modo
            ],

            {
                "tipo":
                    "regua",

                "metros":
                    metros
            },

            (
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # MASSA - FOTO REAL
    # ========================================================

    if tipo == "massa":

        modo = escolher_interacao(

            interacoes,

            (
                "imagem_escolha",
                "multipla_escolha",
                "numero"
            ),

            "multipla_escolha"
        )


        if modo == "imagem_escolha":

            return imagem_escolha(

                "Qual objeto usamos para medir massa?",

                "balanca",

                [
                    {
                        "id":
                            "balanca",

                        "texto":
                            "Balança",

                        "imagem":
                            IMAGENS_REAIS[
                                "balanca"
                            ],

                        "fallback":
                            "⚖️"
                    },

                    {
                        "id":
                            "regua",

                        "texto":
                            "Régua",

                        "imagem":
                            IMAGENS_REAIS[
                                "regua"
                            ],

                        "fallback":
                            "📏"
                    },

                    {
                        "id":
                            "relogio",

                        "texto":
                            "Relógio",

                        "imagem":
                            IMAGENS_REAIS[
                                "relogio"
                            ],

                        "fallback":
                            "🕒"
                    },

                    {
                        "id":
                            "bola",

                        "texto":
                            "Bola",

                        "imagem":
                            IMAGENS_REAIS[
                                "bola"
                            ],

                        "fallback":
                            "⚽"
                    }
                ]
            )


        kg = random.randint(
            1,
            10
        )


        return numerica(

            (
                f"{kg} kg correspondem "
                f"a quantos gramas?"
            ),

            kg * 1000,

            [
                modo
            ],

            {
                "tipo":
                    "balanca",

                "kg":
                    kg
            },

            (
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # MILHAR
    # ========================================================

    if tipo == "milhar":

        milhares = random.randint(
            1,
            9
        )


        return numerica(

            (
                f"{milhares} unidades de milhar "
                f"representam qual número?"
            ),

            milhares * 1000,

            interacoes,

            suportadas=(
                "numero",
                "multipla_escolha"
            )
        )


    if tipo == "decomposicao4":

        valor = random.randint(
            1000,
            9999
        )


        return numerica(

            (
                f"Quantas unidades de milhar "
                f"existem em {valor}?"
            ),

            valor // 1000,

            interacoes,

            suportadas=(
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # QUATRO OPERAÇÕES
    # ========================================================

    if tipo == "quatro_operacoes":

        operacao = random.choice(
            (
                "+",
                "-",
                "×",
                "÷"
            )
        )


        if operacao == "+":

            a = random.randint(
                10,
                100
            )

            b = random.randint(
                10,
                100
            )

            resposta = (
                a + b
            )


        elif operacao == "-":

            a = random.randint(
                20,
                100
            )

            b = random.randint(
                1,
                a
            )

            resposta = (
                a - b
            )


        elif operacao == "×":

            a = random.randint(
                2,
                12
            )

            b = random.randint(
                2,
                12
            )

            resposta = (
                a * b
            )


        else:

            resposta = random.randint(
                2,
                12
            )

            b = random.randint(
                2,
                10
            )

            a = (
                resposta *
                b
            )


        return numerica(

            (
                f"Resolva: "
                f"{a} {operacao} {b}"
            ),

            resposta,

            interacoes,

            suportadas=(
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # FRAÇÕES VISUAIS
    # ========================================================

    if tipo in (
        "fracao_basica",
        "fracao"
    ):

        denominador = random.randint(
            2,
            8
        )

        numerador = random.randint(
            1,
            denominador - 1
        )


        correta = (
            f"{numerador}/"
            f"{denominador}"
        )


        erradas = set()


        while len(erradas) < 3:

            numero = random.randint(
                1,
                7
            )

            divisor = random.randint(
                2,
                8
            )


            candidato = (
                f"{numero}/"
                f"{divisor}"
            )


            if candidato != correta:

                erradas.add(
                    candidato
                )


        return textual(

            "Qual fração está representada na imagem?",

            correta,

            list(
                erradas
            ),

            interacoes,

            {
                "tipo":
                    "fracao",

                "numerador":
                    numerador,

                "denominador":
                    denominador
            }
        )


    if tipo == "fracao_desafio":

        denominador = random.randint(
            2,
            10
        )


        return numerica(

            (
                f"Uma pizza foi dividida em "
                f"{denominador} partes iguais. "
                f"Uma parte representa 1 sobre quanto?"
            ),

            denominador,

            interacoes,

            {
                "tipo":
                    "fracao",

                "numerador":
                    1,

                "denominador":
                    denominador
            },

            (
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # POLÍGONOS
    # ========================================================

    if tipo == "poligonos":

        nome, lados, forma = (
            random.choice(
                (
                    (
                        "triângulo",
                        3,
                        "triangulo"
                    ),

                    (
                        "quadrilátero",
                        4,
                        "quadrado"
                    ),

                    (
                        "pentágono",
                        5,
                        "pentagono"
                    ),

                    (
                        "hexágono",
                        6,
                        "hexagono"
                    )
                )
            )
        )


        return numerica(

            (
                f"Quantos lados possui "
                f"este {nome}?"
            ),

            lados,

            interacoes,

            {
                "tipo":
                    "forma",

                "forma":
                    forma
            },

            (
                "numero",
                "multipla_escolha"
            )
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


        return numerica(

            (
                f"A temperatura era "
                f"{temperatura} °C e aumentou "
                f"{aumento} graus. "
                f"Qual é a nova temperatura?"
            ),

            temperatura + aumento,

            interacoes,

            {
                "tipo":
                    "termometro",

                "valor":
                    temperatura
            },

            (
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # ÂNGULOS
    # ========================================================

    if tipo == "angulos":

        angulo = random.choice(
            (
                30,
                45,
                90,
                120,
                150
            )
        )


        if angulo < 90:

            resposta = (
                "agudo"
            )

        elif angulo == 90:

            resposta = (
                "reto"
            )

        else:

            resposta = (
                "obtuso"
            )


        return textual(

            (
                f"Observe o ângulo de {angulo}°. "
                f"Como ele é classificado?"
            ),

            resposta,

            (
                "agudo",
                "reto",
                "obtuso"
            ),

            interacoes,

            {
                "tipo":
                    "angulo",

                "graus":
                    angulo
            }
        )


    # ========================================================
    # PERÍMETRO
    # ========================================================

    if tipo == "perimetro":

        largura = random.randint(
            2,
            10
        )

        altura = random.randint(
            2,
            10
        )


        return numerica(

            "Qual é o perímetro do retângulo?",

            (
                2 *
                (
                    largura +
                    altura
                )
            ),

            interacoes,

            {
                "tipo":
                    "retangulo_medidas",

                "largura":
                    largura,

                "altura":
                    altura
            },

            (
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # ÁREA
    # ========================================================

    if tipo == "area":

        largura = random.randint(
            2,
            10
        )

        altura = random.randint(
            2,
            10
        )


        return numerica(

            "Qual é a área do retângulo?",

            largura *
            altura,

            interacoes,

            {
                "tipo":
                    "retangulo_medidas",

                "largura":
                    largura,

                "altura":
                    altura,

                "grade":
                    True
            },

            (
                "numero",
                "multipla_escolha"
            )
        )


    if tipo == "perimetro_area":

        return gerar_questao(

            random.choice(
                (
                    "perimetro",
                    "area"
                )
            ),

            interacoes
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

        nova_quantidade = (
            quantidade *
            2
        )


        return numerica(

            (
                f"{quantidade} itens custam "
                f"R$ {quantidade * preco}. "
                f"Quanto custam "
                f"{nova_quantidade} itens?"
            ),

            nova_quantidade *
            preco,

            interacoes,

            suportadas=(
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # PLANO CARTESIANO
    # ========================================================

    if tipo == "plano_cartesiano":

        x = random.randint(
            0,
            8
        )

        y = random.randint(
            0,
            8
        )


        return numerica(

            (
                "Observe o ponto no plano cartesiano. "
                "Qual é a coordenada X?"
            ),

            x,

            interacoes,

            {
                "tipo":
                    "plano_cartesiano",

                "x":
                    x,

                "y":
                    y
            },

            (
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # POLIEDROS
    # ========================================================

    if tipo == "poliedros":

        return numerica(

            "Quantas faces possui um cubo?",

            6,

            interacoes,

            {
                "tipo":
                    "solido",

                "forma":
                    "cubo"
            },

            (
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # CONVERSÃO
    # ========================================================

    if tipo == "conversao":

        metros = random.randint(
            1,
            20
        )


        return numerica(

            (
                f"{metros} metros equivalem "
                f"a quantos centímetros?"
            ),

            metros * 100,

            interacoes,

            suportadas=(
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # VOLUME
    # ========================================================

    if tipo == "volume":

        a = random.randint(
            2,
            6
        )

        b = random.randint(
            2,
            6
        )

        c = random.randint(
            2,
            6
        )


        return numerica(

            (
                f"Um bloco mede "
                f"{a} × {b} × {c}. "
                f"Qual é seu volume?"
            ),

            a * b * c,

            interacoes,

            {
                "tipo":
                    "bloco",

                "a":
                    a,

                "b":
                    b,

                "c":
                    c
            },

            (
                "numero",
                "multipla_escolha"
            )
        )


    # ========================================================
    # TIPOS ESPECIAIS
    # ========================================================

    if tipo == "associacao_formas":

        return associacao_formas()


    if tipo == "ordenacao_numeros":

        return ordenacao_numeros()


    # ========================================================
    # FALLBACK
    # ========================================================

    a = random.randint(
        1,
        10
    )

    b = random.randint(
        1,
        10
    )


    return numerica(

        f"Quanto é {a} + {b}?",

        a + b,

        interacoes
    )