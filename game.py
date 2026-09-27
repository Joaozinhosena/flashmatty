import random


IMAGENS_REAIS = {

    "bola":
        "https://png.pngtree.com/png-vector/20190912/ourmid/pngtree-modren-ball-icon-vector-png-image_1726872.jpg",

    "caixa":
        "https://png.pngtree.com/png-clipart/20220606/ourmid/pngtree-cardboard-box-png-image_4918390.png",

    "lata":
        "https://cdn-icons-png.flaticon.com/512/5198/5198836.png",

    "cone":
        "https://png.pngtree.com/png-vector/20220613/ourmid/pngtree-traffic-cone-vector-png-image_5044131.png",

    "roda":
        "https://png.pngtree.com/png-vector/20250426/ourlarge/pngtree-cartoon-car-tire-graphic-png-image_16123609.png",

    "janela":
        "https://i.pinimg.com/originals/e2/22/69/e22269c79f6880c7fcf60728654d8006.jpg",

    "placa_triangular":
        "https://static.vecteezy.com/ti/vetor-gratis/p1/26734851-triangular-cuidado-placa-atencao-placa-perigo-exclamacao-icone-vetor.jpg",

    "livro":
        "https://png.pngtree.com/png-vector/20260123/ourmid/pngtree-open-book-icon-in-flat-design-style-vector-png-image_18609114.webp",

    "regua":
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS73gqzT4KRSZiv9x0soACoBgs8jCtGZPmPVvdJKGGwwQ&s=10",

    "balanca":
        "https://png.pngtree.com/png-clipart/20240730/original/pngtree-justice-scales-icon-illustration-vector-png-image_15666527.png",

    "relogio":
        "https://png.pngtree.com/png-clipart/20190614/original/pngtree-vector-clock-icon-png-image_3773633.jpg",

    "dado":
        "https://img.magnific.com/vetores-gratis/dados-estilo-desenho-animado_78370-2824.jpg",

    "moeda":
        "https://static.vecteezy.com/ti/vetor-gratis/t1/9645364-coin-icon-logo-vector-illustration-money-stacked-coins-symbol-template-for-graphic-and-web-design-collection-gratis-vetor.jpg",

    "maca":
        "https://png.pngtree.com/element_our/png/20181227/apple-vector-icon-png_293587.jpg",

    "banana":
        "https://www.flaticon.com/br/icone-gratis/banana_6482627",
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
# MOTOR PEDAGÓGICO AVANÇADO
# ============================================================
#
# Esta camada mantém 100% de compatibilidade com o restante do
# projeto. Ela intercepta os tipos mais importantes e cria
# questões com:
# - mais raciocínio;
# - problemas em duas ou três etapas;
# - incógnitas em posições diferentes;
# - distratores baseados em erros comuns;
# - comparação entre estratégias/expressões;
# - contexto realista;
# - níveis "normal" e "desafio" realmente diferentes.
#
# Se um tipo não estiver tratado aqui, o gerador antigo continua
# funcionando normalmente.
# ============================================================


def _nivel_tipo(tipo):
    tipo = str(tipo or "").casefold()

    if (
        "desafio" in tipo
        or "avancada" in tipo
        or tipo in {
            "quatro_operacoes",
            "proporcao",
            "plano_cartesiano",
            "volume",
            "perimetro_area",
            "equivalencia"
        }
    ):
        return 3

    if (
        "visual" in tipo
        or "basico" in tipo
        or "basica" in tipo
    ):
        return 1

    return 2


def _alternativas_por_erros(
    correta,
    erros=None,
    quantidade=4,
    permitir_negativos=False
):
    correta = int(correta)

    candidatos = []

    for valor in (erros or []):
        try:
            valor = int(valor)
        except (
            TypeError,
            ValueError
        ):
            continue

        if (
            valor != correta
            and (
                permitir_negativos
                or valor >= 0
            )
            and valor not in candidatos
        ):
            candidatos.append(valor)

    # Distratores próximos, mas não puramente aleatórios.
    passos = [
        1,
        -1,
        2,
        -2,
        5,
        -5,
        10,
        -10
    ]

    if abs(correta) >= 50:
        passos += [
            20,
            -20
        ]

    if abs(correta) >= 100:
        passos += [
            50,
            -50
        ]

    random.shuffle(passos)

    for passo in passos:
        candidato = correta + passo

        if (
            candidato != correta
            and (
                permitir_negativos
                or candidato >= 0
            )
            and candidato not in candidatos
        ):
            candidatos.append(
                candidato
            )

        if len(candidatos) >= quantidade - 1:
            break

    while len(candidatos) < quantidade - 1:
        margem = max(
            3,
            abs(correta) // 4
        )

        candidato = (
            correta
            +
            random.choice(
                (-1, 1)
            )
            *
            random.randint(
                1,
                margem
            )
        )

        if (
            candidato != correta
            and (
                permitir_negativos
                or candidato >= 0
            )
            and candidato not in candidatos
        ):
            candidatos.append(
                candidato
            )

    valores = [
        correta,
        *candidatos[: quantidade - 1]
    ]

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


# Substitui o gerador simples de alternativas por um que recebe
# distratores pedagogicamente mais plausíveis.
def alternativas_numericas(
    correta,
    quantidade=4,
    erros=None
):
    return _alternativas_por_erros(
        correta,
        erros=erros,
        quantidade=quantidade
    )


def numerica_avancada(
    pergunta,
    resposta,
    interacoes=None,
    visual=None,
    erros=None,
    explicacao=None,
    dificuldade=2,
    habilidade=None,
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

    resposta_int = int(
        resposta
    )

    if modo == "numero":
        dados = questao(
            pergunta,
            str(resposta_int),
            "numero",
            visual=visual
        )

    elif modo == "verdadeiro_falso":
        mostrar_correta = random.random() < 0.5

        if mostrar_correta:
            palpite = resposta_int
        else:
            opcoes_erradas = [
                item["id"]
                for item
                in _alternativas_por_erros(
                    resposta_int,
                    erros=erros,
                    quantidade=4,
                    permitir_negativos=True
                )
                if item["id"] != str(resposta_int)
            ]

            palpite = int(
                random.choice(
                    opcoes_erradas
                )
            )

        dados = questao(
            (
                f"{pergunta} "
                f"Um aluno afirmou que o resultado é {palpite}. "
                f"Essa afirmação está correta?"
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

    else:
        dados = questao(
            pergunta,
            str(resposta_int),
            "multipla_escolha",
            alternativas=(
                _alternativas_por_erros(
                    resposta_int,
                    erros=erros
                )
            ),
            visual=visual
        )

    dados["dificuldade"] = int(
        dificuldade
    )

    if habilidade:
        dados["habilidade"] = str(
            habilidade
        )

    if explicacao:
        dados["explicacao"] = str(
            explicacao
        )

    return dados


def textual_avancada(
    pergunta,
    resposta,
    erradas,
    interacoes=None,
    visual=None,
    explicacao=None,
    dificuldade=2,
    habilidade=None
):
    # Para respostas textuais, não usamos "numero".
    # Isso evita pedir palavras em um campo numérico.
    modo = escolher_interacao(
        interacoes,
        (
            "multipla_escolha",
            "verdadeiro_falso"
        ),
        "multipla_escolha"
    )

    resposta = str(
        resposta
    )

    erradas = [
        str(item)
        for item
        in erradas
        if str(item).casefold()
        != resposta.casefold()
    ]

    if modo == "verdadeiro_falso":
        mostrar_correta = (
            random.random() < 0.5
        )

        apresentada = (
            resposta
            if mostrar_correta
            else random.choice(
                erradas
            )
        )

        dados = questao(
            (
                f"{pergunta} "
                f"Um aluno respondeu “{apresentada}”. "
                f"A resposta dele está correta?"
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

    else:
        dados = questao(
            pergunta,
            resposta,
            "multipla_escolha",
            alternativas=(
                alternativas_texto(
                    resposta,
                    erradas
                )
            ),
            visual=visual
        )

    dados["dificuldade"] = int(
        dificuldade
    )

    if habilidade:
        dados["habilidade"] = str(
            habilidade
        )

    if explicacao:
        dados["explicacao"] = str(
            explicacao
        )

    return dados


def _dia_semana(
    indice
):
    dias = [
        "segunda-feira",
        "terça-feira",
        "quarta-feira",
        "quinta-feira",
        "sexta-feira",
        "sábado",
        "domingo"
    ]

    return dias[
        indice % 7
    ]


# ============================================================
# MOTOR DE PROGRESSÃO POR ANO / ETAPA
# ============================================================


def _nivel_progressivo(nivel=None, ano=None, tipo=None):
    """Resolve um nível global entre 1 e 7."""
    if nivel is not None:
        try:
            return max(1, min(7, int(nivel)))
        except (TypeError, ValueError):
            pass

    if ano is not None:
        try:
            ano_int = max(1, min(5, int(ano)))
            return ano_int
        except (TypeError, ValueError):
            pass

    return max(1, min(7, int(_nivel_tipo(tipo))))


def _faixa_numerica(nivel):
    return {
        1: 10,
        2: 50,
        3: 120,
        4: 500,
        5: 1500,
        6: 10000,
        7: 100000,
    }.get(int(nivel), 120)


def _anexar_progressao(
    dados,
    nivel,
    ano=None,
    complexidade=None,
    operacoes=None,
    desafio=False,
):
    dados["nivel"] = int(nivel)

    if ano is not None:
        try:
            dados["ano_escolar"] = int(ano)
        except (TypeError, ValueError):
            pass

    if complexidade:
        dados["complexidade"] = str(complexidade)

    if operacoes is not None:
        try:
            dados["operacoes_estimadas"] = int(operacoes)
        except (TypeError, ValueError):
            pass

    dados["desafio"] = bool(desafio)
    return dados


def _qnum(
    pergunta,
    resposta,
    interacoes,
    nivel,
    ano=None,
    complexidade=None,
    operacoes=None,
    desafio=False,
    visual=None,
    erros=None,
    explicacao=None,
    habilidade=None,
    suportadas=("numero", "multipla_escolha", "verdadeiro_falso"),
):
    dados = numerica_avancada(
        pergunta,
        resposta,
        interacoes=interacoes,
        visual=visual,
        erros=erros,
        explicacao=explicacao,
        dificuldade=nivel,
        habilidade=habilidade,
        suportadas=suportadas,
    )

    return _anexar_progressao(
        dados,
        nivel,
        ano,
        complexidade,
        operacoes,
        desafio,
    )


def _qtext(
    pergunta,
    resposta,
    erradas,
    interacoes,
    nivel,
    ano=None,
    complexidade=None,
    operacoes=None,
    desafio=False,
    visual=None,
    explicacao=None,
    habilidade=None,
):
    dados = textual_avancada(
        pergunta,
        resposta,
        erradas,
        interacoes=interacoes,
        visual=visual,
        explicacao=explicacao,
        dificuldade=nivel,
        habilidade=habilidade,
    )

    return _anexar_progressao(
        dados,
        nivel,
        ano,
        complexidade,
        operacoes,
        desafio,
    )


def _decimal_pt(valor):
    return f"{valor:.1f}".replace(".", ",")


def gerar_questao_progressiva(
    tipo,
    interacoes=None,
    nivel=None,
    ano=None,
    complexidade=None,
    operacoes=None,
    desafio=False,
):
    """
    Gera questões cuja exigência cresce de acordo com o currículo.

    Nível 1-2: reconhecimento e cálculo simples.
    Nível 3-4: incógnitas, contexto e duas etapas.
    Nível 5-7: composição de operações, interpretação e dados extras.
    """

    nivel = _nivel_progressivo(nivel, ano, tipo)
    complexidade = complexidade or "pratica"
    operacoes = int(operacoes or (3 if desafio else (2 if nivel >= 4 else 1)))
    limite = _faixa_numerica(nivel)

    # --------------------------------------------------------
    # ADIÇÃO
    # --------------------------------------------------------
    if tipo == "adicao_visual":
        a = random.randint(2, 5 if nivel <= 1 else 9)
        b = random.randint(1, 5 if nivel <= 1 else 9)
        correta = a + b
        return _qnum(
            f"Observe os dois grupos. Quantos objetos há ao todo?",
            correta,
            interacoes,
            nivel,
            ano,
            complexidade,
            operacoes,
            desafio,
            visual={"tipo": "grupos", "icone": "⭐", "grupos": [a, b]},
            erros=[abs(a - b), correta - 1, correta + 1],
            explicacao=f"Somamos os grupos: {a} + {b} = {correta}.",
            habilidade="adição por composição de grupos",
            suportadas=("numero", "multipla_escolha", "verdadeiro_falso"),
        )

    if tipo in ("adicao", "adicao_desafio"):
        if nivel <= 2 and not desafio:
            a = random.randint(8, max(12, limite))
            b = random.randint(5, max(10, limite // 2))
            correta = a + b
            return _qnum(
                f"Calcule {a} + {b}.",
                correta,
                interacoes,
                nivel,
                ano,
                complexidade,
                operacoes,
                desafio,
                erros=[correta - 10, correta + 10, abs(a - b)],
                explicacao=f"{a} + {b} = {correta}.",
                habilidade="adição",
            )

        if nivel <= 3 and not desafio:
            total = random.randint(max(40, limite // 2), max(80, limite))
            parcela = random.randint(10, total - 10)
            faltante = total - parcela
            return _qnum(
                f"Descubra o número que falta: {parcela} + □ = {total}.",
                faltante,
                interacoes,
                nivel,
                ano,
                complexidade,
                operacoes,
                desafio,
                erros=[total + parcela, parcela, faltante + 10],
                explicacao=f"O valor faltante é {total} - {parcela} = {faltante}.",
                habilidade="relação inversa entre adição e subtração",
            )

        a = random.randint(max(40, limite // 8), max(80, limite // 2))
        b = random.randint(max(20, limite // 12), max(40, limite // 3))
        c = random.randint(5, max(10, min(a + b - 1, limite // 5)))
        correta = a + b - c
        return _qnum(
            (
                f"Uma coleção tinha {a} itens. Recebeu mais {b} e depois "
                f"{c} itens foram retirados. Quantos itens ficaram?"
            ),
            correta,
            interacoes,
            nivel,
            ano,
            complexidade,
            max(2, operacoes),
            desafio,
            erros=[a + b + c, a + b, abs(a - b) + c],
            explicacao=f"Primeiro: {a} + {b} = {a+b}. Depois: {a+b} - {c} = {correta}.",
            habilidade="problema aditivo em duas etapas",
        )

    if tipo == "problema_adicao":
        a = random.randint(8, max(20, limite // 2))
        b = random.randint(5, max(15, limite // 3))
        if nivel <= 2:
            correta = a + b
            pergunta = f"Lia tinha {a} figurinhas e ganhou {b}. Quantas figurinhas ela tem agora?"
            explicacao = f"Juntamos as quantidades: {a} + {b} = {correta}."
            erros = [abs(a - b), correta - 1, correta + 1]
        else:
            c = random.randint(3, max(6, min(30, limite // 8)))
            correta = a + b + c
            pergunta = (
                f"Lia tinha {a} figurinhas, ganhou {b} pela manhã e mais {c} à tarde. "
                f"Quantas figurinhas ela passou a ter?"
            )
            explicacao = f"Somamos as três quantidades: {a} + {b} + {c} = {correta}."
            erros = [a + b, a + c, b + c]
        return _qnum(
            pergunta,
            correta,
            interacoes,
            nivel,
            ano,
            complexidade,
            max(1, operacoes),
            desafio,
            erros=erros,
            explicacao=explicacao,
            habilidade="resolução de problema de adição",
        )

    # --------------------------------------------------------
    # SUBTRAÇÃO
    # --------------------------------------------------------
    if tipo == "subtracao_visual":
        total = random.randint(6, 12 if nivel <= 1 else 20)
        retirados = random.randint(1, total - 1)
        correta = total - retirados
        return _qnum(
            f"Havia {total} balões e {retirados} estouraram. Quantos sobraram?",
            correta,
            interacoes,
            nivel,
            ano,
            complexidade,
            operacoes,
            desafio,
            visual={"tipo": "subtracao_objetos", "icone": "🎈", "total": total, "retirados": retirados},
            erros=[total + retirados, retirados, correta + 1],
            explicacao=f"Retiramos {retirados} de {total}: {total} - {retirados} = {correta}.",
            habilidade="subtração por retirada",
        )

    if tipo in ("subtracao", "subtracao_desafio"):
        if nivel <= 2 and not desafio:
            a = random.randint(20, max(30, limite))
            b = random.randint(5, a - 1)
            correta = a - b
            return _qnum(
                f"Calcule {a} - {b}.",
                correta,
                interacoes,
                nivel,
                ano,
                complexidade,
                operacoes,
                desafio,
                erros=[a + b, b - 1, correta + 10],
                explicacao=f"{a} - {b} = {correta}.",
                habilidade="subtração",
            )

        if nivel <= 3 and not desafio:
            total = random.randint(60, max(100, limite))
            restante = random.randint(10, total - 10)
            retirado = total - restante
            return _qnum(
                f"De {total} unidades, algumas foram retiradas e restaram {restante}. Quantas foram retiradas?",
                retirado,
                interacoes,
                nivel,
                ano,
                complexidade,
                operacoes,
                desafio,
                erros=[total + restante, restante, retirado + 10],
                explicacao=f"Quantidade retirada = {total} - {restante} = {retirado}.",
                habilidade="subtração com termo desconhecido",
            )

        inicial = random.randint(max(100, limite // 3), max(180, limite))
        saida1 = random.randint(10, max(20, inicial // 4))
        entrada = random.randint(5, max(15, inicial // 5))
        correta = inicial - saida1 + entrada
        return _qnum(
            (
                f"Um estoque tinha {inicial} peças. Foram usadas {saida1} e depois chegaram {entrada} novas. "
                f"Quantas peças há agora?"
            ),
            correta,
            interacoes,
            nivel,
            ano,
            complexidade,
            max(2, operacoes),
            desafio,
            erros=[inicial - saida1 - entrada, inicial + saida1 + entrada, inicial - saida1],
            explicacao=f"{inicial} - {saida1} = {inicial-saida1}; depois + {entrada} = {correta}.",
            habilidade="problema misto de adição e subtração",
        )

    if tipo == "problema_subtracao":
        total = random.randint(20, max(40, limite))
        retirado = random.randint(4, total - 5)
        correta = total - retirado
        if nivel >= 4:
            devolvido = random.randint(2, max(3, retirado // 2))
            correta += devolvido
            pergunta = (
                f"Uma caixa tinha {total} peças. {retirado} foram retiradas e depois {devolvido} foram devolvidas. "
                f"Quantas peças ficaram na caixa?"
            )
            explicacao = f"{total} - {retirado} + {devolvido} = {correta}."
            erros = [total - retirado, total + retirado - devolvido, total - retirado - devolvido]
        else:
            pergunta = f"Uma caixa tinha {total} brinquedos e {retirado} foram retirados. Quantos sobraram?"
            explicacao = f"{total} - {retirado} = {correta}."
            erros = [total + retirado, retirado, correta + 1]
        return _qnum(
            pergunta,
            correta,
            interacoes,
            nivel,
            ano,
            complexidade,
            operacoes,
            desafio,
            erros=erros,
            explicacao=explicacao,
            habilidade="problema de subtração",
        )

    # --------------------------------------------------------
    # VALOR POSICIONAL / COMPOSIÇÃO
    # --------------------------------------------------------
    if tipo in (
        "composicao_visual", "composicao", "decomposicao",
        "composicao_desafio", "milhar", "decomposicao4"
    ):
        if nivel <= 2:
            dezenas = random.randint(1, 9)
            unidades = random.randint(0, 9)
            correta = dezenas * 10 + unidades
            return _qnum(
                f"{dezenas} dezenas e {unidades} unidades formam qual número?",
                correta,
                interacoes,
                nivel,
                ano,
                complexidade,
                operacoes,
                desafio,
                visual={"tipo": "material_dourado", "dezenas": dezenas, "unidades": unidades},
                erros=[dezenas + unidades, unidades * 10 + dezenas, dezenas * 10],
                explicacao=f"{dezenas} dezenas valem {dezenas*10}; somando {unidades}, obtemos {correta}.",
                habilidade="composição de números",
            )

        if nivel <= 4:
            centenas = random.randint(1, 9)
            dezenas = random.randint(0, 9)
            unidades = random.randint(0, 9)
            correta = centenas * 100 + dezenas * 10 + unidades
            return _qnum(
                f"Forme o número com {centenas} centenas, {dezenas} dezenas e {unidades} unidades.",
                correta,
                interacoes,
                nivel,
                ano,
                complexidade,
                operacoes,
                desafio,
                erros=[centenas*100 + unidades*10 + dezenas, centenas*10 + dezenas + unidades, correta + 100],
                explicacao=f"{centenas*100} + {dezenas*10} + {unidades} = {correta}.",
                habilidade="valor posicional até centenas",
            )

        valor = random.randint(1000, 9999 if nivel <= 5 else 99999)
        ordem = random.choice((10, 100, 1000))
        nomes = {10: "dezenas", 100: "centenas", 1000: "unidades de milhar"}
        correta = (valor // ordem) % 10
        return _qnum(
            f"No número {valor}, qual algarismo ocupa a ordem das {nomes[ordem]}?",
            correta,
            interacoes,
            nivel,
            ano,
            complexidade,
            operacoes,
            desafio,
            erros=[valor % 10, (valor // 10) % 10, (valor // 100) % 10],
            explicacao=f"Observando o valor posicional de {valor}, o algarismo pedido é {correta}.",
            habilidade="valor posicional",
        )

    # --------------------------------------------------------
    # MULTIPLICAÇÃO
    # --------------------------------------------------------
    if tipo == "multiplicacao_visual":
        grupos = random.randint(2, 5 if nivel <= 2 else 8)
        itens = random.randint(2, 5 if nivel <= 2 else 9)
        correta = grupos * itens
        return _qnum(
            "Observe os grupos. Quantos objetos existem ao todo?",
            correta,
            interacoes,
            nivel,
            ano,
            complexidade,
            operacoes,
            desafio,
            visual={"tipo": "multiplicacao_grupos", "icone": "🍎", "grupos": grupos, "itens": itens},
            erros=[grupos + itens, grupos * (itens - 1), correta + grupos],
            explicacao=f"São {grupos} grupos de {itens}: {grupos} × {itens} = {correta}.",
            habilidade="multiplicação como grupos iguais",
        )

    if tipo in ("multiplicacao", "multiplicacao_avancada", "multiplicacao_desafio"):
        max_fator = {1: 5, 2: 10, 3: 12, 4: 20, 5: 30, 6: 50, 7: 99}[nivel]
        a = random.randint(2, max_fator)
        b = random.randint(2, 10 if nivel <= 3 else min(20, max_fator))
        correta = a * b

        if nivel <= 3 and not desafio:
            pergunta = f"Calcule {a} × {b}."
            explicacao = f"{a} × {b} = {correta}."
            erros = [a + b, a * (b - 1), correta + a]
        elif nivel <= 4 and not desafio:
            pergunta = f"Qual número completa a igualdade? {a} × □ = {correta}."
            correta = b
            explicacao = f"Como {a} × {b} = {a*b}, o fator que falta é {b}."
            erros = [a, b + 1, max(1, b - 1)]
        else:
            perdas = random.randint(3, max(5, b))
            total = a * b
            correta = total - perdas
            pergunta = (
                f"Uma fábrica montou {a} caixas com {b} peças em cada uma. "
                f"Na inspeção, {perdas} peças foram descartadas. Quantas peças válidas restaram?"
            )
            explicacao = f"Primeiro {a} × {b} = {total}; depois {total} - {perdas} = {correta}."
            erros = [total, a * (b - 1), total + perdas]

        return _qnum(
            pergunta,
            correta,
            interacoes,
            nivel,
            ano,
            complexidade,
            max(1, operacoes),
            desafio,
            erros=erros,
            explicacao=explicacao,
            habilidade="multiplicação e resolução de problemas",
        )

    if tipo == "problema_multiplicacao":
        caixas = random.randint(3, 8 if nivel <= 3 else 20)
        itens = random.randint(3, 10 if nivel <= 3 else 25)
        total = caixas * itens
        if nivel >= 5:
            usados = random.randint(5, min(total - 1, max(10, itens * 2)))
            correta = total - usados
            pergunta = (
                f"Há {caixas} caixas com {itens} objetos em cada. Depois, {usados} objetos foram usados. "
                f"Quantos restaram?"
            )
            explicacao = f"{caixas} × {itens} = {total}; {total} - {usados} = {correta}."
            erros = [total, caixas + itens - usados, total + usados]
        else:
            correta = total
            pergunta = f"Há {caixas} caixas com {itens} objetos em cada. Quantos objetos existem ao todo?"
            explicacao = f"{caixas} × {itens} = {correta}."
            erros = [caixas + itens, caixas * (itens - 1), total + caixas]
        return _qnum(
            pergunta, correta, interacoes, nivel, ano, complexidade, operacoes, desafio,
            erros=erros, explicacao=explicacao, habilidade="problema multiplicativo"
        )

    # --------------------------------------------------------
    # DIVISÃO
    # --------------------------------------------------------
    if tipo == "divisao_visual":
        grupos = random.randint(2, 6)
        por_grupo = random.randint(2, 8)
        total = grupos * por_grupo
        return _qnum(
            f"{total} doces serão divididos igualmente entre {grupos} crianças. Quantos cada uma recebe?",
            por_grupo,
            interacoes,
            nivel,
            ano,
            complexidade,
            operacoes,
            desafio,
            visual={"tipo": "divisao", "icone": "🍬", "total": total, "grupos": grupos},
            erros=[grupos, total - grupos, por_grupo + 1],
            explicacao=f"{total} ÷ {grupos} = {por_grupo}.",
            habilidade="divisão como repartição equitativa",
        )

    if tipo in ("divisao", "divisao_desafio"):
        divisor = random.randint(2, 10 if nivel <= 3 else 20)
        quociente = random.randint(2, 12 if nivel <= 3 else 30)
        total = divisor * quociente
        if nivel <= 3 and not desafio:
            pergunta = f"Calcule {total} ÷ {divisor}."
            correta = quociente
            explicacao = f"{total} ÷ {divisor} = {quociente}."
            erros = [divisor, quociente + 1, max(1, quociente - 1)]
        elif nivel <= 4 and not desafio:
            pergunta = f"Qual divisor completa a igualdade? {total} ÷ □ = {quociente}."
            correta = divisor
            explicacao = f"Como {divisor} × {quociente} = {total}, o divisor é {divisor}."
            erros = [quociente, divisor + 1, max(1, divisor - 1)]
        else:
            lotes = random.randint(2, 5)
            novo_total = total * lotes
            pergunta = (
                f"{novo_total} unidades serão organizadas em grupos de {divisor}. "
                f"Quantos grupos completos serão formados?"
            )
            correta = novo_total // divisor
            explicacao = f"{novo_total} ÷ {divisor} = {correta}."
            erros = [divisor, quociente, correta + 1]
        return _qnum(
            pergunta, correta, interacoes, nivel, ano, complexidade, operacoes, desafio,
            erros=erros, explicacao=explicacao, habilidade="divisão e relação inversa"
        )

    if tipo == "problema_divisao":
        pessoas = random.randint(2, 8 if nivel <= 3 else 15)
        quantidade = random.randint(3, 10 if nivel <= 3 else 20)
        total = pessoas * quantidade
        correta = quantidade
        pergunta = (
            f"{total} objetos foram divididos igualmente entre {pessoas} pessoas. "
            f"Quantos objetos cada pessoa recebeu?"
        )
        if nivel >= 5:
            lotes = random.randint(2, 4)
            total *= lotes
            correta = total // pessoas
            pergunta = (
                f"Foram reunidos {lotes} lotes de {pessoas * quantidade} objetos. "
                f"Todo o material foi dividido igualmente entre {pessoas} pessoas. Quantos objetos cada uma recebeu?"
            )
        return _qnum(
            pergunta, correta, interacoes, nivel, ano, complexidade, operacoes, desafio,
            erros=[pessoas, total - pessoas, correta + 1],
            explicacao=f"Dividimos o total igualmente: {total} ÷ {pessoas} = {correta}.",
            habilidade="problema de divisão"
        )

    # --------------------------------------------------------
    # DOBRO / METADE / TRIPLO / TERÇA PARTE
    # --------------------------------------------------------
    if tipo in ("dobro", "metade", "triplo", "terca", "dobro_metade_desafio"):
        base = random.randint(4, 20 if nivel <= 3 else 60)
        if tipo == "dobro":
            correta = base * 2
            pergunta = f"Qual é o dobro de {base}?"
            explicacao = f"Dobro significa multiplicar por 2: {base} × 2 = {correta}."
        elif tipo == "metade":
            base *= 2
            correta = base // 2
            pergunta = f"Qual é a metade de {base}?"
            explicacao = f"Metade significa dividir por 2: {base} ÷ 2 = {correta}."
        elif tipo == "triplo":
            correta = base * 3
            pergunta = f"Qual é o triplo de {base}?"
            explicacao = f"Triplo significa multiplicar por 3: {base} × 3 = {correta}."
        elif tipo == "terca":
            base *= 3
            correta = base // 3
            pergunta = f"Qual é a terça parte de {base}?"
            explicacao = f"Terça parte significa dividir por 3: {base} ÷ 3 = {correta}."
        else:
            correta = base * 6
            pergunta = f"Qual é o dobro do triplo de {base}?"
            explicacao = f"Triplo: {base} × 3 = {base*3}; dobro: {base*3} × 2 = {correta}."
        return _qnum(
            pergunta, correta, interacoes, nivel, ano, complexidade, operacoes, desafio,
            erros=[base * 2, base * 3, max(0, correta // 2)],
            explicacao=explicacao, habilidade="relações multiplicativas"
        )

    # --------------------------------------------------------
    # COMPARAÇÃO / EQUIVALÊNCIA
    # --------------------------------------------------------
    if tipo == "comparacao":
        if nivel <= 2:
            valores = random.sample(range(1, max(20, limite) + 1), 4)
            correta = max(valores)
            return _qnum(
                f"Qual é o maior número entre {', '.join(map(str, valores))}?",
                correta,
                interacoes,
                nivel,
                ano,
                complexidade,
                operacoes,
                desafio,
                erros=[v for v in valores if v != correta],
                explicacao=f"O maior valor da lista é {correta}.",
                habilidade="comparação de números",
                suportadas=("numero", "multipla_escolha", "verdadeiro_falso"),
            )
        a, b, c, d = [random.randint(5, max(20, limite // 3)) for _ in range(4)]
        valor1 = a + b
        valor2 = c + d
        if valor1 == valor2:
            d += 1
            valor2 += 1
        correta = max(valor1, valor2)
        return _qnum(
            f"Compare as expressões {a} + {b} e {c} + {d}. Qual delas produz o maior resultado? Digite esse resultado.",
            correta,
            interacoes,
            nivel,
            ano,
            complexidade,
            operacoes,
            desafio,
            erros=[min(valor1, valor2), abs(valor1-valor2), correta + 1],
            explicacao=f"Os resultados são {valor1} e {valor2}; o maior é {correta}.",
            habilidade="comparação de expressões",
        )

    if tipo == "equivalencia":
        resultado = random.randint(20, max(30, limite))
        a = random.randint(3, resultado - 3)
        b = resultado - a
        c = random.randint(3, resultado - 3)
        faltante = resultado - c
        return _qnum(
            f"Complete para manter a igualdade: {a} + {b} = {c} + □.",
            faltante,
            interacoes,
            nivel,
            ano,
            complexidade,
            operacoes,
            desafio,
            erros=[resultado, c, abs(c - resultado)],
            explicacao=f"{a} + {b} = {resultado}. Então {c} + {faltante} também deve resultar em {resultado}.",
            habilidade="equivalência de expressões",
        )

    # --------------------------------------------------------
    # DECIMAIS
    # --------------------------------------------------------
    if tipo == "decimal":
        inteiro = random.randint(1, 20 if nivel <= 3 else 100)
        dec1 = random.randint(1, 9)
        dec2 = random.randint(1, 9)
        if dec1 == dec2:
            dec2 = 9 if dec1 != 9 else 8
        a = inteiro + dec1 / 10
        b = inteiro + dec2 / 10
        correta = max(a, b)
        correta_txt = _decimal_pt(correta)
        erradas = [_decimal_pt(min(a, b)), str(inteiro), _decimal_pt(inteiro + 0.5)]
        pergunta = f"Qual número é maior: {_decimal_pt(a)} ou {_decimal_pt(b)}?"
        return _qtext(
            pergunta,
            correta_txt,
            erradas,
            interacoes,
            nivel,
            ano,
            complexidade,
            operacoes,
            desafio,
            explicacao=f"As partes inteiras são iguais; comparamos os décimos. O maior é {correta_txt}.",
            habilidade="comparação de números decimais",
        )

    # --------------------------------------------------------
    # QUATRO OPERAÇÕES
    # --------------------------------------------------------
    if tipo == "quatro_operacoes":
        if nivel <= 4:
            op = random.choice(("+", "-", "×", "÷"))
            if op == "+":
                a, b = random.randint(20, 200), random.randint(10, 100)
                correta = a + b
            elif op == "-":
                a = random.randint(60, 250)
                b = random.randint(10, a - 1)
                correta = a - b
            elif op == "×":
                a, b = random.randint(3, 15), random.randint(2, 12)
                correta = a * b
            else:
                correta = random.randint(3, 15)
                b = random.randint(2, 10)
                a = correta * b
            return _qnum(
                f"Resolva: {a} {op} {b}.",
                correta,
                interacoes,
                nivel,
                ano,
                complexidade,
                operacoes,
                desafio,
                erros=[a + b, abs(a-b), a*b if op != "×" else a+b],
                explicacao=f"Aplicando a operação indicada, o resultado é {correta}.",
                habilidade="quatro operações",
            )

        a = random.randint(20, 80)
        b = random.randint(2, 12)
        c = random.randint(2, 12)
        correta = a + b * c
        erro_ordem = (a + b) * c
        return _qnum(
            f"Resolva respeitando a ordem das operações: {a} + {b} × {c}.",
            correta,
            interacoes,
            nivel,
            ano,
            complexidade,
            max(2, operacoes),
            desafio,
            erros=[erro_ordem, a + b + c, a * b + c],
            explicacao=f"Multiplicamos primeiro: {b} × {c} = {b*c}; depois {a} + {b*c} = {correta}.",
            habilidade="ordem das operações",
        )

    # --------------------------------------------------------
    # FRAÇÕES
    # --------------------------------------------------------
    if tipo in ("fracao_basica", "fracao", "fracao_desafio"):
        if nivel <= 3 and not desafio:
            denominador = random.randint(2, 8)
            numerador = random.randint(1, denominador - 1)
            correta = f"{numerador}/{denominador}"
            erradas = [
                f"{denominador}/{numerador}",
                f"{max(1, numerador-1)}/{denominador}",
                f"{numerador}/{denominador+1}",
            ]
            return _qtext(
                "Qual fração está representada na imagem?",
                correta,
                erradas,
                interacoes,
                nivel,
                ano,
                complexidade,
                operacoes,
                desafio,
                visual={"tipo": "fracao", "numerador": numerador, "denominador": denominador},
                explicacao=f"Há {numerador} partes destacadas de um total de {denominador}: {correta}.",
                habilidade="leitura de frações",
            )

        denominador = random.choice((2, 3, 4, 5, 6, 8))
        numerador = random.randint(1, denominador - 1)
        unidade = random.randint(3, 10)
        total = denominador * unidade
        correta = numerador * unidade
        return _qnum(
            f"Em um grupo de {total} itens, {numerador}/{denominador} foram selecionados. Quantos itens foram selecionados?",
            correta,
            interacoes,
            nivel,
            ano,
            complexidade,
            max(2, operacoes),
            desafio,
            erros=[total // denominador, total - correta, numerador + denominador],
            explicacao=f"1/{denominador} de {total} é {unidade}; multiplicando por {numerador}, obtemos {correta}.",
            habilidade="fração de uma quantidade",
        )

    # --------------------------------------------------------
    # DINHEIRO
    # --------------------------------------------------------
    if tipo in ("dinheiro_basico", "dinheiro", "problema_dinheiro", "dinheiro_desafio"):
        if nivel <= 2 and tipo in ("dinheiro_basico", "dinheiro"):
            valores = random.choices((1, 2, 5, 10), k=random.randint(2, 4))
            correta = sum(valores)
            return _qnum(
                "Quanto dinheiro há ao todo?",
                correta,
                interacoes,
                nivel,
                ano,
                complexidade,
                operacoes,
                desafio,
                visual={"tipo": "dinheiro", "valores": valores},
                erros=[max(valores), correta - 1, correta + 2],
                explicacao=f"Somando os valores {valores}, temos R$ {correta}.",
                habilidade="sistema monetário",
            )

        quantidade = random.randint(2, 6 if nivel <= 4 else 12)
        preco = random.randint(3, 20 if nivel <= 4 else 50)
        custo = quantidade * preco
        pago = custo + random.randint(5, 40)
        troco = pago - custo
        return _qnum(
            (
                f"Uma pessoa comprou {quantidade} itens a R$ {preco} cada e pagou com R$ {pago}. "
                f"Quanto deve receber de troco?"
            ),
            troco,
            interacoes,
            nivel,
            ano,
            complexidade,
            max(2, operacoes),
            desafio,
            erros=[custo, pago + custo, pago - preco],
            explicacao=f"Custo: {quantidade} × {preco} = {custo}. Troco: {pago} - {custo} = {troco}.",
            habilidade="problema monetário em duas etapas",
        )

    # --------------------------------------------------------
    # TEMPO / CALENDÁRIO
    # --------------------------------------------------------
    if tipo in ("calendario_basico", "calendario", "calendario_desafio"):
        if nivel <= 2 and tipo != "calendario_desafio":
            pergunta, correta, erros = random.choice((
                ("Quantos dias possui uma semana?", 7, [5, 6, 8]),
                ("Quantos meses possui um ano?", 12, [10, 11, 13]),
                ("Quantas horas possui um dia?", 24, [12, 20, 48]),
            ))
            return _qnum(
                pergunta, correta, interacoes, nivel, ano, complexidade, operacoes, desafio,
                erros=erros, explicacao=f"A resposta correta é {correta}.", habilidade="calendário e unidades de tempo"
            )

        inicio = random.randint(0, 6)
        avanco = random.randint(8, 30 if nivel <= 4 else 60)
        correta = _dia_semana(inicio + avanco)
        erradas = [_dia_semana(inicio + avanco + k) for k in (1, 2, -1)]
        return _qtext(
            f"Hoje é {_dia_semana(inicio)}. Que dia da semana será daqui a {avanco} dias?",
            correta,
            erradas,
            interacoes,
            nivel,
            ano,
            complexidade,
            operacoes,
            desafio,
            explicacao=f"Avançamos {avanco} dias no ciclo de 7 dias e chegamos a {correta}.",
            habilidade="raciocínio com calendário",
        )

    if tipo == "tempo":
        if nivel <= 3:
            horas = random.randint(2, 8)
            correta = horas * 60
            return _qnum(
                f"{horas} horas correspondem a quantos minutos?",
                correta,
                interacoes,
                nivel,
                ano,
                complexidade,
                operacoes,
                desafio,
                erros=[horas * 100, correta - 60, correta + 60],
                explicacao=f"Cada hora tem 60 minutos: {horas} × 60 = {correta}.",
                habilidade="conversão de tempo",
            )
        hora = random.randint(7, 18)
        duracao_h = random.randint(1, 3)
        duracao_m = random.choice((15, 30, 45))
        inicio_min = hora * 60
        total = inicio_min + duracao_h * 60 + duracao_m
        hora_final = (total // 60) % 24
        minuto_final = total % 60
        correta = f"{hora_final:02d}:{minuto_final:02d}"
        erradas = [
            f"{(hora_final+1)%24:02d}:{minuto_final:02d}",
            f"{hora_final:02d}:{(minuto_final+15)%60:02d}",
            f"{hora:02d}:{duracao_m:02d}",
        ]
        return _qtext(
            f"Uma atividade começou às {hora:02d}:00 e durou {duracao_h} h e {duracao_m} min. A que horas terminou?",
            correta,
            erradas,
            interacoes,
            nivel,
            ano,
            complexidade,
            max(2, operacoes),
            desafio,
            explicacao=f"Somamos {duracao_h} h e {duracao_m} min ao horário inicial: término às {correta}.",
            habilidade="duração e horário final",
        )

    # --------------------------------------------------------
    # PROBABILIDADE
    # --------------------------------------------------------
    if tipo in ("probabilidade_basica", "probabilidade", "probabilidade_desafio"):
        if nivel <= 2 and tipo != "probabilidade_desafio":
            return None  # preserva as questões visuais do gerador existente

        favoraveis = random.randint(2, 6)
        outros = random.randint(2, 8)
        total = favoraveis + outros
        correta = f"{favoraveis}/{total}"
        erradas = [f"{outros}/{total}", f"{favoraveis}/{outros}", f"1/{total}"]
        return _qtext(
            f"Uma sacola tem {favoraveis} bolas azuis e {outros} vermelhas. Qual é a probabilidade de retirar uma azul?",
            correta,
            erradas,
            interacoes,
            nivel,
            ano,
            complexidade,
            operacoes,
            desafio,
            explicacao=f"Há {favoraveis} casos favoráveis em {total} possibilidades: {correta}.",
            habilidade="probabilidade como razão",
        )

    # --------------------------------------------------------
    # GRÁFICOS
    # --------------------------------------------------------
    if tipo in ("grafico_basico", "grafico", "grafico_desafio"):
        dados = {
            "Maçã": random.randint(4, 18 if nivel <= 3 else 40),
            "Banana": random.randint(4, 18 if nivel <= 3 else 40),
            "Uva": random.randint(4, 18 if nivel <= 3 else 40),
            "Laranja": random.randint(4, 18 if nivel <= 3 else 40),
        }
        if nivel <= 2 and tipo == "grafico_basico":
            maior = max(dados, key=dados.get)
            erradas = [x for x in dados if x != maior]
            return _qtext(
                "Observe o gráfico. Qual fruta possui a maior quantidade?",
                maior,
                erradas,
                interacoes,
                nivel,
                ano,
                complexidade,
                operacoes,
                desafio,
                visual={"tipo": "grafico_barras", "dados": dados},
                explicacao=f"A maior barra corresponde a {maior}, com {dados[maior]} unidades.",
                habilidade="leitura direta de gráfico",
            )

        nomes = random.sample(list(dados), 2)
        if nivel <= 4:
            correta = dados[nomes[0]] + dados[nomes[1]]
            pergunta = f"Quantas unidades há ao todo ao juntar {nomes[0]} e {nomes[1]}?"
            explicacao = f"{dados[nomes[0]]} + {dados[nomes[1]]} = {correta}."
            erros = [abs(dados[nomes[0]] - dados[nomes[1]]), max(dados.values()), correta + 2]
        else:
            maior_nome = max(dados, key=dados.get)
            menor_nome = min(dados, key=dados.get)
            correta = dados[maior_nome] - dados[menor_nome]
            pergunta = f"Qual é a diferença entre a maior e a menor quantidade mostradas no gráfico?"
            explicacao = f"Maior: {dados[maior_nome]}; menor: {dados[menor_nome]}; diferença = {correta}."
            erros = [dados[maior_nome] + dados[menor_nome], dados[maior_nome], dados[menor_nome]]
        return _qnum(
            pergunta,
            correta,
            interacoes,
            nivel,
            ano,
            complexidade,
            max(2, operacoes),
            desafio,
            visual={"tipo": "grafico_barras", "dados": dados},
            erros=erros,
            explicacao=explicacao,
            habilidade="interpretação de gráfico",
            suportadas=("numero", "multipla_escolha", "verdadeiro_falso"),
        )

    # --------------------------------------------------------
    # COMPRIMENTO / MASSA / CONVERSÃO
    # --------------------------------------------------------
    if tipo in ("comprimento", "conversao"):
        metros = random.randint(2, 20 if nivel <= 4 else 80)
        correta = metros * 100
        if nivel >= 6:
            extra_cm = random.randint(10, 90)
            correta += extra_cm
            pergunta = f"Uma fita mede {metros} m e {extra_cm} cm. Qual é o comprimento total em centímetros?"
            explicacao = f"{metros} m = {metros*100} cm; somando {extra_cm} cm, obtemos {correta} cm."
            erros = [metros*100, metros + extra_cm, correta + 100]
        else:
            pergunta = f"{metros} metros correspondem a quantos centímetros?"
            explicacao = f"1 m = 100 cm; então {metros} × 100 = {correta} cm."
            erros = [metros*10, metros*1000, correta + 100]
        return _qnum(
            pergunta, correta, interacoes, nivel, ano, complexidade, operacoes, desafio,
            erros=erros, explicacao=explicacao, habilidade="conversão de comprimento"
        )

    if tipo == "massa":
        kg = random.randint(2, 12 if nivel <= 4 else 40)
        correta = kg * 1000
        if nivel >= 6:
            extra = random.choice((250, 500, 750))
            correta += extra
            pergunta = f"Uma carga pesa {kg} kg e {extra} g. Quantos gramas ela pesa ao todo?"
            explicacao = f"{kg} kg = {kg*1000} g; + {extra} g = {correta} g."
            erros = [kg*1000, kg*100 + extra, correta - 1000]
        else:
            pergunta = f"{kg} kg correspondem a quantos gramas?"
            explicacao = f"1 kg = 1000 g; então {kg} × 1000 = {correta} g."
            erros = [kg*100, kg*10, correta + 1000]
        return _qnum(
            pergunta, correta, interacoes, nivel, ano, complexidade, operacoes, desafio,
            erros=erros, explicacao=explicacao, habilidade="conversão de massa"
        )

    # --------------------------------------------------------
    # TEMPERATURA
    # --------------------------------------------------------
    if tipo == "temperatura":
        inicial = random.randint(5, 35)
        variacao1 = random.randint(3, 12)
        if nivel <= 3:
            correta = inicial + variacao1
            pergunta = f"A temperatura era {inicial} °C e aumentou {variacao1} °C. Qual é a nova temperatura?"
            explicacao = f"{inicial} + {variacao1} = {correta} °C."
            erros = [inicial - variacao1, variacao1, correta + 1]
        else:
            queda = random.randint(2, variacao1)
            correta = inicial + variacao1 - queda
            pergunta = (
                f"A temperatura era {inicial} °C, subiu {variacao1} °C e depois caiu {queda} °C. "
                f"Qual é a temperatura final?"
            )
            explicacao = f"{inicial} + {variacao1} - {queda} = {correta} °C."
            erros = [inicial + variacao1 + queda, inicial - variacao1 - queda, inicial + variacao1]
        return _qnum(
            pergunta, correta, interacoes, nivel, ano, complexidade, operacoes, desafio,
            visual={"tipo": "termometro", "valor": inicial},
            erros=erros, explicacao=explicacao, habilidade="variação de temperatura"
        )

    # --------------------------------------------------------
    # FIGURAS / POLÍGONOS / LADOS E VÉRTICES
    # --------------------------------------------------------
    if tipo in ("figuras_lados", "figuras_planas", "lados_vertices", "poligonos", "figuras_desafio"):
        opcoes = [
            ("triângulo", 3, 3, "triangulo"),
            ("quadrado", 4, 4, "quadrado"),
            ("pentágono", 5, 5, "pentagono"),
            ("hexágono", 6, 6, "hexagono"),
        ]
        nome, lados, vertices, forma = random.choice(opcoes)
        if tipo == "figuras_desafio" or nivel >= 5:
            correta = vertices
            pergunta = f"Um {nome} possui {lados} lados. Quantos vértices ele possui?"
            habilidade = "relação entre lados e vértices"
        else:
            correta = lados
            pergunta = f"Quantos lados possui este {nome}?"
            habilidade = "classificação de polígonos"
        return _qnum(
            pergunta, correta, interacoes, nivel, ano, complexidade, operacoes, desafio,
            visual={"tipo": "forma", "forma": forma},
            erros=[max(0, correta-1), correta+1, correta+2],
            explicacao=f"Um {nome} possui {lados} lados e {vertices} vértices.",
            habilidade=habilidade,
        )

    # --------------------------------------------------------
    # ÂNGULOS
    # --------------------------------------------------------
    if tipo == "angulos":
        if nivel <= 5:
            angulo = random.choice((30, 45, 60, 90, 120, 135, 150))
            resposta = "agudo" if angulo < 90 else ("reto" if angulo == 90 else "obtuso")
            return _qtext(
                f"Observe o ângulo de {angulo}°. Como ele é classificado?",
                resposta,
                ["agudo", "reto", "obtuso"],
                interacoes,
                nivel,
                ano,
                complexidade,
                operacoes,
                desafio,
                visual={"tipo": "angulo", "graus": angulo},
                explicacao=(
                    "Ângulos menores que 90° são agudos, 90° é reto e entre 90° e 180° são obtusos."
                ),
                habilidade="classificação de ângulos",
            )
        angulo = random.choice((25, 35, 40, 55, 65, 70))
        correta = 90 - angulo
        return _qnum(
            f"Um ângulo de {angulo}° precisa de quantos graus para completar um ângulo reto?",
            correta,
            interacoes,
            nivel,
            ano,
            complexidade,
            operacoes,
            desafio,
            erros=[180-angulo, 90+angulo, angulo],
            explicacao=f"Ângulo reto = 90°. Então 90 - {angulo} = {correta}°.",
            habilidade="ângulos complementares",
        )

    # --------------------------------------------------------
    # PERÍMETRO / ÁREA
    # --------------------------------------------------------
    if tipo in ("perimetro", "area", "perimetro_area"):
        largura = random.randint(3, 14 if nivel <= 5 else 30)
        altura = random.randint(3, 14 if nivel <= 5 else 30)
        if tipo == "perimetro":
            correta = 2 * (largura + altura)
            pergunta = "Qual é o perímetro do retângulo?"
            explicacao = f"P = 2 × ({largura} + {altura}) = {correta}."
            erros = [largura*altura, largura+altura, 2*largura+altura]
            habilidade = "perímetro"
        elif tipo == "area":
            correta = largura * altura
            pergunta = "Qual é a área do retângulo?"
            explicacao = f"A = {largura} × {altura} = {correta}."
            erros = [2*(largura+altura), largura+altura, largura*2]
            habilidade = "área"
        else:
            area = largura * altura
            if nivel >= 6:
                correta = altura
                pergunta = f"Um retângulo tem área {area} e largura {largura}. Qual é a altura?"
                explicacao = f"Altura = área ÷ largura = {area} ÷ {largura} = {altura}."
                erros = [area-largura, largura, largura+altura]
                habilidade = "dimensão desconhecida a partir da área"
            else:
                correta = 2*(largura+altura)
                pergunta = f"Um retângulo mede {largura} por {altura}. Qual é seu perímetro?"
                explicacao = f"P = 2 × ({largura} + {altura}) = {correta}."
                erros = [area, largura+altura, 2*largura+altura]
                habilidade = "perímetro e área"
        return _qnum(
            pergunta, correta, interacoes, nivel, ano, complexidade, operacoes, desafio,
            visual={"tipo": "retangulo_medidas", "largura": largura, "altura": altura, "grade": tipo != "perimetro"},
            erros=erros, explicacao=explicacao, habilidade=habilidade
        )

    # --------------------------------------------------------
    # PROPORÇÃO
    # --------------------------------------------------------
    if tipo == "proporcao":
        quantidade = random.randint(2, 8)
        preco_unitario = random.randint(3, 15)
        nova_quantidade = random.randint(quantidade + 1, quantidade * (3 if nivel >= 6 else 2))
        correta = nova_quantidade * preco_unitario
        total_inicial = quantidade * preco_unitario
        return _qnum(
            f"{quantidade} itens custam R$ {total_inicial}. Mantendo o mesmo preço por item, quanto custam {nova_quantidade} itens?",
            correta,
            interacoes,
            nivel,
            ano,
            complexidade,
            max(2, operacoes),
            desafio,
            erros=[total_inicial*2, nova_quantidade+preco_unitario, total_inicial+nova_quantidade],
            explicacao=f"Preço unitário = {total_inicial} ÷ {quantidade} = {preco_unitario}; então {nova_quantidade} × {preco_unitario} = {correta}.",
            habilidade="proporcionalidade direta",
        )

    # --------------------------------------------------------
    # PLANO CARTESIANO
    # --------------------------------------------------------
    if tipo == "plano_cartesiano":
        x = random.randint(0, 8)
        y = random.randint(0, 8)
        if nivel <= 5:
            eixo = random.choice(("x", "y"))
            correta = x if eixo == "x" else y
            pergunta = f"Observe o ponto no plano cartesiano. Qual é a coordenada {eixo.upper()}?"
            explicacao = f"O ponto mostrado é ({x}, {y}); portanto a coordenada {eixo.upper()} é {correta}."
        else:
            dx = random.randint(1, 5)
            dy = random.randint(1, 5)
            correta = x + dx
            pergunta = (
                f"O ponto começa em ({x}, {y}) e se desloca {dx} unidades para a direita e {dy} para cima. "
                f"Qual será a nova coordenada X?"
            )
            explicacao = f"Mover para a direita aumenta X: {x} + {dx} = {correta}."
        return _qnum(
            pergunta, correta, interacoes, nivel, ano, complexidade, operacoes, desafio,
            visual={"tipo": "plano_cartesiano", "x": x, "y": y},
            erros=[y, x-dx if nivel > 5 else x+1, correta+1],
            explicacao=explicacao, habilidade="coordenadas cartesianas"
        )

    # --------------------------------------------------------
    # POLIEDROS
    # --------------------------------------------------------
    if tipo == "poliedros":
        solidos = [
            ("cubo", 6, 8, 12),
            ("prisma triangular", 5, 6, 9),
            ("pirâmide quadrangular", 5, 5, 8),
        ]
        nome, faces, vertices, arestas = random.choice(solidos)
        if nivel >= 7:
            correta = arestas
            pergunta = f"Um {nome} possui {faces} faces e {vertices} vértices. Pela relação V - A + F = 2, quantas arestas ele possui?"
            explicacao = f"A = V + F - 2 = {vertices} + {faces} - 2 = {arestas}."
            erros = [faces+vertices, arestas-1, arestas+1]
            habilidade = "relação de Euler em poliedros"
        else:
            correta = faces
            pergunta = f"Quantas faces possui um {nome}?"
            explicacao = f"O {nome} possui {faces} faces."
            erros = [vertices, arestas, max(1, faces-1)]
            habilidade = "características de poliedros"
        return _qnum(
            pergunta, correta, interacoes, nivel, ano, complexidade, operacoes, desafio,
            erros=erros, explicacao=explicacao, habilidade=habilidade
        )

    # --------------------------------------------------------
    # VOLUME
    # --------------------------------------------------------
    if tipo == "volume":
        a = random.randint(2, 8 if nivel <= 5 else 15)
        b = random.randint(2, 8 if nivel <= 5 else 15)
        c = random.randint(2, 8 if nivel <= 5 else 15)
        volume = a*b*c
        if nivel >= 7:
            correta = c
            pergunta = f"Um bloco tem volume {volume}, comprimento {a} e largura {b}. Qual é sua altura?"
            explicacao = f"Altura = {volume} ÷ ({a} × {b}) = {c}."
            erros = [a+b, volume//a, c+1]
            habilidade = "dimensão desconhecida a partir do volume"
        else:
            correta = volume
            pergunta = f"Um bloco mede {a} × {b} × {c}. Qual é seu volume?"
            explicacao = f"V = {a} × {b} × {c} = {volume}."
            erros = [a+b+c, a*b+c, 2*(a+b+c)]
            habilidade = "volume de bloco retangular"
        return _qnum(
            pergunta, correta, interacoes, nivel, ano, complexidade, operacoes, desafio,
            visual={"tipo": "bloco", "a": a, "b": b, "c": c},
            erros=erros, explicacao=explicacao, habilidade=habilidade
        )

    # Os tipos eminentemente visuais (nome de figura e sólido) continuam
    # usando o gerador existente, que já possui imagens e associações.
    return None


def gerar_questao_avancada(
    tipo,
    interacoes=None,
    nivel=None,
    ano=None,
    complexidade=None,
    operacoes=None,
    desafio=False
):
    nivel = _nivel_progressivo(
        nivel,
        ano,
        tipo
    )

    # ========================================================
    # ADIÇÃO
    # ========================================================

    if tipo == "adicao":
        modelo = random.choice(
            (
                "soma",
                "incognita",
                "comparacao"
            )
        )

        if modelo == "soma":
            a = random.randint(
                18,
                180
            )

            b = random.randint(
                12,
                120
            )

            correta = a + b

            return numerica_avancada(
                (
                    f"Calcule {a} + {b}. "
                    f"Faça a decomposição mental em dezenas e unidades."
                ),
                correta,
                interacoes,
                erros=[
                    a + (b // 10),
                    correta - 10,
                    correta + 10
                ],
                dificuldade=2,
                habilidade="adição com reagrupamento"
            )

        if modelo == "incognita":
            total = random.randint(
                90,
                260
            )

            parcela = random.randint(
                20,
                total - 20
            )

            faltante = total - parcela

            return numerica_avancada(
                (
                    f"Qual número deve ocupar o espaço? "
                    f"{parcela} + □ = {total}"
                ),
                faltante,
                interacoes,
                erros=[
                    total + parcela,
                    total - parcela - 10,
                    parcela
                ],
                dificuldade=2,
                habilidade="termo desconhecido da adição"
            )

        a = random.randint(
            30,
            120
        )

        b = random.randint(
            20,
            90
        )

        c = random.randint(
            20,
            90
        )

        return numerica_avancada(
            (
                f"A expressão A vale {a} + {b}. "
                f"A expressão B vale {a} + {c}. "
                f"Qual é a diferença entre os dois resultados?"
            ),
            abs(b - c),
            interacoes,
            erros=[
                b + c,
                abs(a - b),
                abs(a - c)
            ],
            dificuldade=2,
            habilidade="comparação de somas"
        )

    if tipo == "problema_adicao":
        inicio = random.randint(
            25,
            90
        )

        ganhou = random.randint(
            15,
            70
        )

        usou = random.randint(
            5,
            min(
                40,
                inicio + ganhou - 1
            )
        )

        correta = (
            inicio
            +
            ganhou
            -
            usou
        )

        return numerica_avancada(
            (
                f"Uma coleção tinha {inicio} cards. "
                f"Foram adicionados {ganhou} cards e, depois, "
                f"{usou} foram usados em uma troca. "
                f"Quantos cards ficaram na coleção?"
            ),
            correta,
            interacoes,
            erros=[
                inicio + ganhou + usou,
                inicio + ganhou,
                ganhou - usou
            ],
            dificuldade=2,
            habilidade="problema de duas etapas"
        )

    if tipo == "adicao_desafio":
        a = random.randint(
            80,
            260
        )

        b = random.randint(
            40,
            180
        )

        c = random.randint(
            20,
            100
        )

        d = random.randint(
            10,
            80
        )

        correta = (
            a + b + c - d
        )

        return numerica_avancada(
            (
                f"Em um evento entraram {a} pessoas pela manhã, "
                f"{b} à tarde e {c} à noite. "
                f"Antes do encerramento, {d} pessoas saíram. "
                f"Quantas pessoas permaneceram?"
            ),
            correta,
            interacoes,
            erros=[
                a + b + c + d,
                a + b - c - d,
                a + b + c
            ],
            dificuldade=3,
            habilidade="adição e subtração encadeadas"
        )

    # ========================================================
    # SUBTRAÇÃO
    # ========================================================

    if tipo == "subtracao":
        modelo = random.choice(
            (
                "direta",
                "incognita",
                "distancia"
            )
        )

        if modelo == "incognita":
            inicial = random.randint(
                100,
                350
            )

            sobrou = random.randint(
                20,
                inicial - 30
            )

            retirado = inicial - sobrou

            return numerica_avancada(
                (
                    f"De {inicial} unidades restaram {sobrou}. "
                    f"Quantas unidades foram retiradas?"
                ),
                retirado,
                interacoes,
                erros=[
                    inicial + sobrou,
                    inicial - sobrou - 10,
                    sobrou
                ],
                dificuldade=2,
                habilidade="subtração inversa"
            )

        if modelo == "distancia":
            a = random.randint(
                150,
                500
            )

            b = random.randint(
                60,
                a - 20
            )

            return numerica_avancada(
                (
                    f"Dois participantes fizeram {a} e {b} pontos. "
                    f"Quantos pontos separam as duas pontuações?"
                ),
                a - b,
                interacoes,
                erros=[
                    a + b,
                    a - b + 10,
                    a - b - 10
                ],
                dificuldade=2,
                habilidade="diferença entre quantidades"
            )

        a = random.randint(
            120,
            500
        )

        b = random.randint(
            30,
            a - 30
        )

        return numerica_avancada(
            f"Calcule {a} - {b}.",
            a - b,
            interacoes,
            erros=[
                a + b,
                abs(
                    (a // 10)
                    -
                    (b // 10)
                ),
                a - b + 10
            ],
            dificuldade=2,
            habilidade="subtração com reagrupamento"
        )

    if tipo == "problema_subtracao":
        estoque = random.randint(
            80,
            240
        )

        vendidos = random.randint(
            15,
            estoque // 2
        )

        recebidos = random.randint(
            10,
            70
        )

        correta = (
            estoque
            -
            vendidos
            +
            recebidos
        )

        return numerica_avancada(
            (
                f"Uma loja tinha {estoque} itens. "
                f"Vendeu {vendidos} e depois recebeu mais {recebidos}. "
                f"Quantos itens há agora?"
            ),
            correta,
            interacoes,
            erros=[
                estoque - vendidos - recebidos,
                estoque + vendidos + recebidos,
                estoque - vendidos
            ],
            dificuldade=2,
            habilidade="subtração em contexto"
        )

    if tipo == "subtracao_desafio":
        total = random.randint(
            300,
            900
        )

        primeira = random.randint(
            80,
            220
        )

        segunda = random.randint(
            60,
            180
        )

        if primeira + segunda >= total:
            segunda = max(
                20,
                total - primeira - 50
            )

        correta = (
            total
            -
            primeira
            -
            segunda
        )

        return numerica_avancada(
            (
                f"Um reservatório tinha {total} litros. "
                f"Foram usados {primeira} litros e depois mais "
                f"{segunda} litros. Quantos litros restaram?"
            ),
            correta,
            interacoes,
            erros=[
                total - primeira + segunda,
                total - segunda,
                total - primeira
            ],
            dificuldade=3,
            habilidade="subtrações sucessivas"
        )

    # ========================================================
    # COMPOSIÇÃO E VALOR POSICIONAL
    # ========================================================

    if tipo in (
        "composicao",
        "decomposicao"
    ):
        numero = random.randint(
            100,
            999
        )

        centena = (
            numero // 100
        )

        dezena = (
            numero // 10
            % 10
        )

        unidade = (
            numero % 10
        )

        modelo = random.choice(
            (
                "algarismo",
                "valor",
                "recompor"
            )
        )

        if modelo == "algarismo":
            return numerica_avancada(
                (
                    f"No número {numero}, qual é o algarismo "
                    f"das dezenas?"
                ),
                dezena,
                interacoes,
                erros=[
                    centena,
                    unidade,
                    dezena * 10
                ],
                dificuldade=2,
                habilidade="valor posicional"
            )

        if modelo == "valor":
            return numerica_avancada(
                (
                    f"No número {numero}, qual é o valor "
                    f"posicional do algarismo {dezena}?"
                ),
                dezena * 10,
                interacoes,
                erros=[
                    dezena,
                    centena * 100,
                    unidade
                ],
                dificuldade=2,
                habilidade="valor posicional"
            )

        return numerica_avancada(
            (
                f"Qual número é formado por {centena} centenas, "
                f"{dezena} dezenas e {unidade} unidades?"
            ),
            numero,
            interacoes,
            erros=[
                centena * 100 + unidade * 10 + dezena,
                centena * 100 + dezena + unidade,
                centena * 10 + dezena + unidade
            ],
            dificuldade=2,
            habilidade="composição numérica"
        )

    if tipo == "composicao_desafio":
        numero = random.randint(
            1000,
            9999
        )

        milhar = numero // 1000
        centena = numero // 100 % 10
        dezena = numero // 10 % 10
        unidade = numero % 10

        return numerica_avancada(
            (
                f"Forme o número com {milhar} unidades de milhar, "
                f"{centena} centenas, {dezena} dezenas e "
                f"{unidade} unidades."
            ),
            numero,
            interacoes,
            erros=[
                milhar * 1000
                + dezena * 100
                + centena * 10
                + unidade,
                milhar * 1000
                + centena * 100
                + unidade * 10
                + dezena,
                milhar * 100
                + centena * 10
                + dezena
                + unidade
            ],
            dificuldade=3,
            habilidade="composição até 9999"
        )

    if tipo == "milhar":
        numero = random.randint(
            1000,
            9999
        )

        posicao = random.choice(
            (
                "milhar",
                "centena",
                "dezena"
            )
        )

        if posicao == "milhar":
            resposta = (
                numero // 1000
            )
            valor = resposta * 1000
        elif posicao == "centena":
            resposta = (
                numero // 100
                % 10
            )
            valor = resposta * 100
        else:
            resposta = (
                numero // 10
                % 10
            )
            valor = resposta * 10

        if random.random() < 0.5:
            pergunta = (
                f"No número {numero}, qual é o algarismo "
                f"na posição de {posicao}?"
            )
            correta = resposta
            erros = [
                valor,
                numero % 10,
                numero // 1000
            ]
        else:
            pergunta = (
                f"No número {numero}, qual é o valor posicional "
                f"do algarismo que está na posição de {posicao}?"
            )
            correta = valor
            erros = [
                resposta,
                resposta * 10,
                resposta * 100
            ]

        return numerica_avancada(
            pergunta,
            correta,
            interacoes,
            erros=erros,
            dificuldade=2,
            habilidade="valor posicional até unidade de milhar"
        )

    if tipo == "decomposicao4":
        numero = random.randint(
            1000,
            9999
        )

        milhares = numero // 1000
        centenas = numero // 100 % 10
        dezenas = numero // 10 % 10
        unidades = numero % 10

        pergunta = (
            f"Considere {numero} = "
            f"{milhares * 1000} + {centenas * 100} + "
            f"{dezenas * 10} + {unidades}. "
            f"Qual é o valor da parcela das centenas?"
        )

        return numerica_avancada(
            pergunta,
            centenas * 100,
            interacoes,
            erros=[
                centenas,
                dezenas * 10,
                milhares * 1000
            ],
            dificuldade=2,
            habilidade="decomposição decimal"
        )

    # ========================================================
    # MULTIPLICAÇÃO
    # ========================================================

    if tipo == "multiplicacao":
        modelo = random.choice(
            (
                "direta",
                "fator_faltante",
                "distributiva"
            )
        )

        if modelo == "fator_faltante":
            a = random.randint(
                3,
                12
            )

            b = random.randint(
                3,
                12
            )

            produto = (
                a * b
            )

            return numerica_avancada(
                (
                    f"Qual número completa a igualdade? "
                    f"{a} × □ = {produto}"
                ),
                b,
                interacoes,
                erros=[
                    produto - a,
                    produto // 2,
                    a + b
                ],
                dificuldade=2,
                habilidade="fator desconhecido"
            )

        if modelo == "distributiva":
            a = random.randint(
                3,
                9
            )

            b = random.randint(
                11,
                19
            )

            correta = (
                a * b
            )

            return numerica_avancada(
                (
                    f"Use uma estratégia mental: "
                    f"{a} × {b} = {a} × 10 + {a} × {b - 10}. "
                    f"Qual é o resultado?"
                ),
                correta,
                interacoes,
                erros=[
                    a * 10 + b - 10,
                    a + b,
                    correta - a
                ],
                dificuldade=2,
                habilidade="propriedade distributiva"
            )

        a = random.randint(
            4,
            15
        )

        b = random.randint(
            4,
            15
        )

        return numerica_avancada(
            f"Calcule {a} × {b}.",
            a * b,
            interacoes,
            erros=[
                a + b,
                a * (b - 1),
                (a - 1) * b
            ],
            dificuldade=2,
            habilidade="multiplicação"
        )

    if tipo == "multiplicacao_avancada":
        a = random.randint(
            12,
            49
        )

        b = random.randint(
            3,
            12
        )

        correta = (
            a * b
        )

        return numerica_avancada(
            (
                f"Calcule {a} × {b}. "
                f"Uma boa estratégia é decompor {a} "
                f"em dezenas e unidades."
            ),
            correta,
            interacoes,
            erros=[
                (a // 10) * b + (a % 10),
                a * (b - 1),
                a + b
            ],
            dificuldade=3,
            habilidade="multiplicação por decomposição"
        )

    if tipo == "problema_multiplicacao":
        fileiras = random.randint(
            4,
            12
        )

        por_fileira = random.randint(
            5,
            15
        )

        extras = random.randint(
            2,
            20
        )

        correta = (
            fileiras
            *
            por_fileira
            +
            extras
        )

        return numerica_avancada(
            (
                f"Um auditório tem {fileiras} fileiras com "
                f"{por_fileira} cadeiras em cada uma e ainda "
                f"{extras} cadeiras extras. "
                f"Quantas cadeiras há ao todo?"
            ),
            correta,
            interacoes,
            erros=[
                fileiras + por_fileira + extras,
                fileiras * por_fileira,
                fileiras * (por_fileira + extras)
            ],
            dificuldade=2,
            habilidade="multiplicação em problema de duas etapas"
        )

    if tipo == "multiplicacao_desafio":
        a = random.randint(
            18,
            65
        )

        b = random.randint(
            6,
            15
        )

        retirar = random.randint(
            10,
            80
        )

        correta = (
            a * b
            -
            retirar
        )

        return numerica_avancada(
            (
                f"Uma fábrica montou {a} caixas com {b} peças "
                f"em cada uma. Na inspeção, {retirar} peças "
                f"foram descartadas. Quantas peças válidas restaram?"
            ),
            correta,
            interacoes,
            erros=[
                a * b,
                a * (b - 1) - retirar,
                a + b - retirar
            ],
            dificuldade=3,
            habilidade="multiplicação e subtração"
        )

    # ========================================================
    # DIVISÃO
    # ========================================================

    if tipo == "divisao":
        modelo = random.choice(
            (
                "quociente",
                "divisor",
                "dividendo"
            )
        )

        divisor = random.randint(
            3,
            12
        )

        quociente = random.randint(
            4,
            18
        )

        dividendo = (
            divisor
            *
            quociente
        )

        if modelo == "divisor":
            return numerica_avancada(
                (
                    f"Complete: {dividendo} ÷ □ = {quociente}"
                ),
                divisor,
                interacoes,
                erros=[
                    quociente,
                    dividendo - quociente,
                    divisor + 1
                ],
                dificuldade=2,
                habilidade="divisor desconhecido"
            )

        if modelo == "dividendo":
            return numerica_avancada(
                (
                    f"Complete: □ ÷ {divisor} = {quociente}"
                ),
                dividendo,
                interacoes,
                erros=[
                    divisor + quociente,
                    divisor * (quociente - 1),
                    quociente
                ],
                dificuldade=2,
                habilidade="dividendo desconhecido"
            )

        return numerica_avancada(
            f"Calcule {dividendo} ÷ {divisor}.",
            quociente,
            interacoes,
            erros=[
                divisor,
                quociente - 1,
                quociente + divisor
            ],
            dificuldade=2,
            habilidade="divisão exata"
        )

    if tipo == "problema_divisao":
        grupos = random.randint(
            3,
            9
        )

        por_grupo = random.randint(
            4,
            14
        )

        total = (
            grupos
            *
            por_grupo
        )

        reserva = random.randint(
            1,
            12
        )

        correta = (
            por_grupo
        )

        return numerica_avancada(
            (
                f"Uma escola separou {total + reserva} lápis. "
                f"{reserva} ficaram de reserva e os demais foram "
                f"divididos igualmente entre {grupos} grupos. "
                f"Quantos lápis cada grupo recebeu?"
            ),
            correta,
            interacoes,
            erros=[
                (total + reserva) // grupos,
                grupos,
                por_grupo + reserva
            ],
            dificuldade=2,
            habilidade="divisão após subtração"
        )

    if tipo == "divisao_desafio":
        divisor = random.randint(
            4,
            12
        )

        quociente = random.randint(
            12,
            30
        )

        total = (
            divisor
            *
            quociente
        )

        usado = (
            divisor
            *
            random.randint(
                2,
                6
            )
        )

        restante = (
            total
            -
            usado
        )

        correta = (
            restante
            //
            divisor
        )

        return numerica_avancada(
            (
                f"Havia {total} itens organizados igualmente em "
                f"{divisor} grupos. Foram retirados {usado} itens, "
                f"sempre retirando a mesma quantidade de cada grupo. "
                f"Se a distribuição continuar equilibrada, "
                f"quantos itens ficam em cada grupo?"
            ),
            correta,
            interacoes,
            erros=[
                quociente,
                restante,
                quociente - usado
            ],
            dificuldade=3,
            habilidade="divisão em duas etapas"
        )

    # ========================================================
    # DOBRO, METADE, TRIPLO E RELAÇÕES
    # ========================================================

    if tipo in (
        "dobro",
        "metade",
        "triplo",
        "terca"
    ):
        base = random.randint(
            8,
            60
        )

        if tipo == "dobro":
            correta = base * 2
            texto = (
                f"Uma quantidade aumentou para o dobro de {base}. "
                f"Qual é a nova quantidade?"
            )
            erros = [
                base + 2,
                base * 3,
                base + base // 2
            ]

        elif tipo == "triplo":
            correta = base * 3
            texto = (
                f"Qual é o triplo de {base}?"
            )
            erros = [
                base * 2,
                base + 3,
                base * 4
            ]

        elif tipo == "metade":
            correta = base
            valor = base * 2
            texto = (
                f"Uma equipe dividiu {valor} pontos igualmente "
                f"em duas partes. Quanto vale cada parte?"
            )
            erros = [
                valor,
                base - 1,
                base + 2
            ]

        else:
            correta = base
            valor = base * 3
            texto = (
                f"Qual é a terça parte de {valor}?"
            )
            erros = [
                valor // 2,
                base * 2,
                base + 3
            ]

        return numerica_avancada(
            texto,
            correta,
            interacoes,
            erros=erros,
            dificuldade=2,
            habilidade="relações multiplicativas"
        )

    if tipo == "dobro_metade_desafio":
        valor = random.randint(
            6,
            40
        )

        triplo = (
            valor * 3
        )

        correta = (
            triplo * 2
        )

        return numerica_avancada(
            (
                f"Primeiro calcule o triplo de {valor}. "
                f"Depois calcule o dobro do resultado. "
                f"Qual é o valor final?"
            ),
            correta,
            interacoes,
            erros=[
                valor * 5,
                valor * 3,
                valor * 2
            ],
            dificuldade=3,
            habilidade="operações encadeadas"
        )

    # ========================================================
    # COMPARAÇÃO, ORDENAÇÃO E EQUIVALÊNCIA
    # ========================================================

    if tipo == "comparacao":
        if (
            interacoes
            and "ordenacao" in interacoes
            and random.random() < 0.45
        ):
            valores = random.sample(
                range(
                    30,
                    300
                ),
                5
            )

            return questao(
                "Ordene os números do menor para o maior.",
                [
                    str(v)
                    for v
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
                                    str(v),
                                "texto":
                                    str(v)
                            }
                            for v
                            in valores
                        ]
                    )
                )
            )

        a = random.randint(
            20,
            90
        )
        b = random.randint(
            10,
            60
        )
        c = random.randint(
            3,
            12
        )
        d = random.randint(
            3,
            12
        )

        expressoes = [
            (
                "A",
                f"{a} + {b}",
                a + b
            ),
            (
                "B",
                f"{c} × {d}",
                c * d
            ),
            (
                "C",
                f"{a + b + 20} - 20",
                a + b
            )
        ]

        maior_valor = max(
            item[2]
            for item
            in expressoes
        )

        maiores = [
            item
            for item
            in expressoes
            if item[2] == maior_valor
        ]

        if len(maiores) != 1:
            # Garante uma resposta única.
            expressoes[1] = (
                "B",
                f"{c} × {d + 5}",
                c * (d + 5)
            )

        maior = max(
            expressoes,
            key=lambda item:
                item[2]
        )

        return questao(
            (
                "Sem calcular apenas pelo tamanho dos números, "
                "compare os resultados e marque a expressão de "
                "maior valor."
            ),
            maior[0],
            "multipla_escolha",
            alternativas=(
                embaralhar(
                    [
                        {
                            "id":
                                codigo,
                            "texto":
                                f"{codigo}) {texto}"
                        }

                        for (
                            codigo,
                            texto,
                            _
                        )
                        in expressoes
                    ]
                )
            )
        )

    if tipo == "equivalencia":
        resultado = random.randint(
            30,
            120
        )

        a = random.randint(
            10,
            resultado - 10
        )

        b = (
            resultado - a
        )

        multiplicador = random.randint(
            2,
            8
        )

        alvo = random.randint(
            2,
            10
        )

        esquerda = (
            a + b
        )

        if random.random() < 0.5:
            termo = random.randint(
                5,
                esquerda - 5
            )

            correta = (
                esquerda - termo
            )

            pergunta = (
                f"{a} + {b} possui o mesmo valor que "
                f"{termo} + □. Qual número completa a igualdade?"
            )

            erros = [
                esquerda + termo,
                termo,
                correta + termo
            ]

        else:
            produto = (
                multiplicador
                *
                alvo
            )

            termo = random.randint(
                1,
                produto - 1
            )

            correta = (
                produto - termo
            )

            pergunta = (
                f"{multiplicador} × {alvo} possui o mesmo valor "
                f"que {termo} + □. Qual número completa?"
            )

            erros = [
                produto,
                multiplicador + alvo,
                termo
            ]

        return numerica_avancada(
            pergunta,
            correta,
            interacoes,
            erros=erros,
            dificuldade=3,
            habilidade="equivalência de expressões"
        )

    # ========================================================
    # DECIMAIS
    # ========================================================

    if tipo == "decimal":
        inteiro = random.randint(
            1,
            20
        )

        decimos = random.randint(
            1,
            9
        )

        centesimos = random.randint(
            0,
            9
        )

        valor = (
            inteiro
            +
            decimos / 10
            +
            centesimos / 100
        )

        texto_valor = (
            f"{valor:.2f}"
            .replace(
                ".",
                ","
            )
        )

        modelo = random.choice(
            (
                "leitura",
                "comparacao",
                "posicao"
            )
        )

        if modelo == "leitura":
            correta = (
                f"{inteiro} inteiros e "
                f"{decimos * 10 + centesimos} centésimos"
            )

            erradas = [
                f"{inteiro} inteiros e {decimos} centésimos",
                f"{inteiro} inteiros e {centesimos} décimos",
                f"{inteiro + 1} inteiros e {decimos * 10 + centesimos} centésimos"
            ]

            return textual_avancada(
                (
                    f"Qual leitura representa melhor o número "
                    f"{texto_valor}?"
                ),
                correta,
                erradas,
                interacoes,
                dificuldade=2,
                habilidade="leitura de números decimais"
            )

        if modelo == "posicao":
            return numerica_avancada(
                (
                    f"No número {texto_valor}, qual algarismo "
                    f"ocupa a casa dos décimos?"
                ),
                decimos,
                interacoes,
                erros=[
                    centesimos,
                    inteiro,
                    decimos * 10
                ],
                dificuldade=2,
                habilidade="valor posicional decimal"
            )

        outro = round(
            valor
            +
            random.choice(
                (
                    -0.30,
                    -0.10,
                    0.10,
                    0.20,
                    0.40
                )
            ),
            2
        )

        if outro < 0:
            outro = (
                valor + 0.2
            )

        outro_texto = (
            f"{outro:.2f}"
            .replace(
                ".",
                ","
            )
        )

        correta = (
            texto_valor
            if valor > outro
            else outro_texto
        )

        return textual_avancada(
            (
                f"Qual é o maior número: "
                f"{texto_valor} ou {outro_texto}?"
            ),
            correta,
            [
                texto_valor
                if correta != texto_valor
                else outro_texto,
                "São iguais",
                "Não é possível comparar"
            ],
            interacoes,
            dificuldade=2,
            habilidade="comparação de decimais"
        )

    # ========================================================
    # CALENDÁRIO
    # ========================================================

    if tipo in (
        "calendario",
        "calendario_desafio"
    ):
        inicio = random.randint(
            0,
            6
        )

        dias = random.randint(
            3,
            18
            if tipo == "calendario_desafio"
            else 10
        )

        # "daqui a N dias" avança N posições.
        resposta = _dia_semana(
            inicio + dias
        )

        return textual_avancada(
            (
                f"Hoje é {_dia_semana(inicio)}. "
                f"Daqui a {dias} dias, que dia da semana será?"
            ),
            resposta,
            [
                _dia_semana(
                    inicio + dias - 1
                ),
                _dia_semana(
                    inicio + dias + 1
                ),
                _dia_semana(
                    inicio + dias + 2
                )
            ],
            interacoes,
            dificuldade=(
                3
                if tipo == "calendario_desafio"
                else 2
            ),
            habilidade="ciclos semanais"
        )

    # ========================================================
    # TEMPO
    # ========================================================

    if tipo == "tempo":
        modelo = random.choice(
            (
                "duracao",
                "hora_final",
                "conversao"
            )
        )

        if modelo == "conversao":
            horas = random.randint(
                2,
                7
            )

            minutos_extra = random.choice(
                (
                    15,
                    20,
                    30,
                    45
                )
            )

            correta = (
                horas * 60
                +
                minutos_extra
            )

            return numerica_avancada(
                (
                    f"{horas} horas e {minutos_extra} minutos "
                    f"correspondem a quantos minutos?"
                ),
                correta,
                interacoes,
                erros=[
                    horas * 60,
                    horas * 100 + minutos_extra,
                    correta - 60
                ],
                dificuldade=2,
                habilidade="conversão de tempo"
            )

        hora = random.randint(
            7,
            17
        )

        minuto = random.choice(
            (
                0,
                10,
                15,
                20,
                30,
                40,
                45,
                50
            )
        )

        duracao = random.choice(
            (
                35,
                45,
                50,
                70,
                80,
                90,
                110
            )
        )

        total_inicio = (
            hora * 60
            +
            minuto
        )

        total_fim = (
            total_inicio
            +
            duracao
        )

        hora_fim = (
            total_fim // 60
        )

        minuto_fim = (
            total_fim % 60
        )

        correta = (
            f"{hora_fim:02d}:"
            f"{minuto_fim:02d}"
        )

        if modelo == "hora_final":
            erradas = [
                f"{hora_fim:02d}:{(minuto_fim + 10) % 60:02d}",
                f"{max(0, hora_fim - 1):02d}:{minuto_fim:02d}",
                f"{hora:02d}:{minuto:02d}"
            ]

            return textual_avancada(
                (
                    f"Uma atividade começou às {hora:02d}:{minuto:02d} "
                    f"e durou {duracao} minutos. "
                    f"Em que horário terminou?"
                ),
                correta,
                erradas,
                interacoes,
                visual={
                    "tipo":
                        "relogio",
                    "hora":
                        hora,
                    "minuto":
                        minuto
                },
                dificuldade=2,
                habilidade="cálculo de horário"
            )

        inicio2 = (
            total_inicio
        )
        fim2 = (
            total_fim
        )

        return numerica_avancada(
            (
                f"Uma atividade começou às "
                f"{inicio2 // 60:02d}:{inicio2 % 60:02d} "
                f"e terminou às {fim2 // 60:02d}:{fim2 % 60:02d}. "
                f"Quantos minutos ela durou?"
            ),
            duracao,
            interacoes,
            erros=[
                duracao - 10,
                duracao + 10,
                (
                    fim2 // 60
                    -
                    inicio2 // 60
                ) * 60
            ],
            dificuldade=2,
            habilidade="duração de intervalo"
        )

    # ========================================================
    # DINHEIRO
    # ========================================================

    if tipo in (
        "dinheiro",
        "problema_dinheiro",
        "dinheiro_desafio"
    ):
        preco1 = random.randint(
            8,
            45
        )

        preco2 = random.randint(
            6,
            35
        )

        qtd = random.randint(
            2,
            5
        )

        total = (
            preco1 * qtd
            +
            preco2
        )

        pagamento = (
            ((total + 9) // 10)
            *
            10
        )

        if pagamento == total:
            pagamento += 10

        troco = (
            pagamento
            -
            total
        )

        return numerica_avancada(
            (
                f"Uma pessoa comprou {qtd} itens de R$ {preco1} "
                f"e mais um item de R$ {preco2}. "
                f"Pagou com R$ {pagamento}. "
                f"Qual foi o troco?"
            ),
            troco,
            interacoes,
            erros=[
                pagamento - preco1 - preco2,
                total,
                pagamento - total + 10
            ],
            dificuldade=(
                3
                if tipo == "dinheiro_desafio"
                else 2
            ),
            habilidade="sistema monetário e operações"
        )

    # ========================================================
    # PROBABILIDADE
    # ========================================================

    if tipo in (
        "probabilidade",
        "probabilidade_desafio"
    ):
        vermelhas = random.randint(
            2,
            8
        )

        azuis = random.randint(
            2,
            8
        )

        verdes = random.randint(
            1,
            6
        )

        total = (
            vermelhas
            +
            azuis
            +
            verdes
        )

        if tipo == "probabilidade_desafio":
            maior = max(
                (
                    (
                        "vermelha",
                        vermelhas
                    ),
                    (
                        "azul",
                        azuis
                    ),
                    (
                        "verde",
                        verdes
                    )
                ),
                key=lambda item:
                    item[1]
            )

            # Se houver empate, ajusta uma cor.
            contagens = [
                vermelhas,
                azuis,
                verdes
            ]

            if contagens.count(
                max(
                    contagens
                )
            ) > 1:
                vermelhas += 2
                maior = (
                    "vermelha",
                    vermelhas
                )
                total = (
                    vermelhas
                    +
                    azuis
                    +
                    verdes
                )

            return textual_avancada(
                (
                    f"Uma sacola tem {vermelhas} fichas vermelhas, "
                    f"{azuis} azuis e {verdes} verdes. "
                    f"Sem olhar, qual cor tem maior chance de ser retirada?"
                ),
                maior[0],
                [
                    cor
                    for cor
                    in (
                        "vermelha",
                        "azul",
                        "verde"
                    )
                    if cor != maior[0]
                ]
                +
                [
                    "Todas têm a mesma chance"
                ],
                interacoes,
                dificuldade=3,
                habilidade="comparação de probabilidades"
            )

        return numerica_avancada(
            (
                f"Uma sacola tem {vermelhas} fichas vermelhas, "
                f"{azuis} azuis e {verdes} verdes. "
                f"Quantos resultados elementares existem "
                f"ao considerar cada ficha individualmente?"
            ),
            total,
            interacoes,
            erros=[
                3,
                vermelhas + azuis,
                max(
                    vermelhas,
                    azuis,
                    verdes
                )
            ],
            dificuldade=2,
            habilidade="espaço amostral simples"
        )

    # ========================================================
    # GRÁFICOS
    # ========================================================

    if tipo in (
        "grafico",
        "grafico_desafio"
    ):
        dados = {
            "Maçã":
                random.randint(
                    8,
                    30
                ),

            "Banana":
                random.randint(
                    8,
                    30
                ),

            "Uva":
                random.randint(
                    8,
                    30
                ),

            "Laranja":
                random.randint(
                    8,
                    30
                )
        }

        nomes = list(
            dados.keys()
        )

        a, b = random.sample(
            nomes,
            2
        )

        if tipo == "grafico_desafio":
            correta = (
                dados[a]
                +
                dados[b]
            )

            return numerica_avancada(
                (
                    f"Observe o gráfico. "
                    f"Quantas unidades há ao todo ao juntar "
                    f"{a} e {b}?"
                ),
                correta,
                interacoes,
                visual={
                    "tipo":
                        "grafico_barras",
                    "dados":
                        dados
                },
                erros=[
                    abs(
                        dados[a]
                        -
                        dados[b]
                    ),
                    max(
                        dados[a],
                        dados[b]
                    ),
                    correta + 5
                ],
                dificuldade=3,
                habilidade="leitura e combinação de dados"
            )

        maior = max(
            dados,
            key=dados.get
        )
        menor = min(
            dados,
            key=dados.get
        )

        correta = (
            dados[maior]
            -
            dados[menor]
        )

        return numerica_avancada(
            (
                f"Observe o gráfico. "
                f"Qual é a diferença entre a maior e a menor "
                f"quantidade?"
            ),
            correta,
            interacoes,
            visual={
                "tipo":
                    "grafico_barras",
                "dados":
                    dados
            },
            erros=[
                dados[maior],
                dados[menor],
                dados[maior]
                +
                dados[menor]
            ],
            dificuldade=2,
            habilidade="interpretação de gráfico"
        )

    # ========================================================
    # COMPRIMENTO / MASSA / CONVERSÃO
    # ========================================================

    if tipo in (
        "comprimento",
        "conversao"
    ):
        metros = random.randint(
            2,
            25
        )

        cm_extra = random.choice(
            (
                10,
                20,
                25,
                50,
                75
            )
        )

        correta = (
            metros * 100
            +
            cm_extra
        )

        return numerica_avancada(
            (
                f"Uma fita mede {metros} m e {cm_extra} cm. "
                f"Qual é o comprimento total em centímetros?"
            ),
            correta,
            interacoes,
            erros=[
                metros * 100,
                metros + cm_extra,
                metros * 10 + cm_extra
            ],
            dificuldade=2,
            habilidade="conversão de comprimento"
        )

    if tipo == "massa":
        kg = random.randint(
            1,
            12
        )

        g_extra = random.choice(
            (
                100,
                250,
                500,
                750
            )
        )

        correta = (
            kg * 1000
            +
            g_extra
        )

        return numerica_avancada(
            (
                f"Uma carga pesa {kg} kg e {g_extra} g. "
                f"Qual é a massa total em gramas?"
            ),
            correta,
            interacoes,
            erros=[
                kg * 1000,
                kg * 100 + g_extra,
                kg + g_extra
            ],
            dificuldade=2,
            habilidade="conversão de massa"
        )

    # ========================================================
    # QUATRO OPERAÇÕES
    # ========================================================

    if tipo == "quatro_operacoes":
        modelo = random.choice(
            (
                "precedencia",
                "parenteses",
                "problema"
            )
        )

        if modelo == "precedencia":
            a = random.randint(
                15,
                60
            )

            b = random.randint(
                3,
                9
            )

            c = random.randint(
                3,
                9
            )

            correta = (
                a
                +
                b * c
            )

            return numerica_avancada(
                (
                    f"Resolva respeitando a ordem das operações: "
                    f"{a} + {b} × {c}"
                ),
                correta,
                interacoes,
                erros=[
                    (a + b) * c,
                    a + b + c,
                    a * b + c
                ],
                dificuldade=3,
                habilidade="ordem das operações"
            )

        if modelo == "parenteses":
            a = random.randint(
                8,
                30
            )

            b = random.randint(
                3,
                15
            )

            c = random.randint(
                2,
                6
            )

            correta = (
                (a + b)
                *
                c
            )

            return numerica_avancada(
                (
                    f"Resolva: ({a} + {b}) × {c}"
                ),
                correta,
                interacoes,
                erros=[
                    a + b * c,
                    a * c + b,
                    a + b + c
                ],
                dificuldade=3,
                habilidade="parênteses e multiplicação"
            )

        grupos = random.randint(
            4,
            10
        )

        por_grupo = random.randint(
            8,
            20
        )

        perdidos = random.randint(
            5,
            25
        )

        extras = random.randint(
            3,
            18
        )

        correta = (
            grupos
            *
            por_grupo
            -
            perdidos
            +
            extras
        )

        return numerica_avancada(
            (
                f"Há {grupos} caixas com {por_grupo} itens em cada. "
                f"{perdidos} itens foram descartados e depois "
                f"{extras} novos itens foram adicionados. "
                f"Quantos itens há agora?"
            ),
            correta,
            interacoes,
            erros=[
                grupos * por_grupo,
                grupos + por_grupo - perdidos + extras,
                grupos * por_grupo + perdidos + extras
            ],
            dificuldade=3,
            habilidade="problema com três operações"
        )

    # ========================================================
    # FRAÇÕES
    # ========================================================

    if tipo == "fracao_desafio":
        denominador = random.choice(
            (
                4,
                5,
                6,
                8,
                10,
                12
            )
        )

        numerador = random.randint(
            1,
            denominador - 1
        )

        quantidade_base = random.randint(
            2,
            8
        )

        total = (
            denominador
            *
            quantidade_base
        )

        correta = (
            numerador
            *
            quantidade_base
        )

        return numerica_avancada(
            (
                f"Em uma turma com {total} estudantes, "
                f"{numerador}/{denominador} participaram de uma "
                f"atividade. Quantos estudantes participaram?"
            ),
            correta,
            interacoes,
            erros=[
                denominador,
                numerador,
                total // numerador
                if numerador
                else total
            ],
            dificuldade=3,
            habilidade="fração de uma quantidade"
        )

    if tipo == "fracao":
        base = random.choice(
            (
                2,
                3,
                4,
                5
            )
        )

        numerador = random.randint(
            1,
            base - 1
        )

        fator = random.randint(
            2,
            5
        )

        correta = (
            f"{numerador * fator}/"
            f"{base * fator}"
        )

        original = (
            f"{numerador}/{base}"
        )

        erradas = [
            f"{numerador + fator}/{base + fator}",
            f"{numerador}/{base * fator}",
            f"{numerador * fator}/{base}"
        ]

        return textual_avancada(
            (
                f"Qual fração é equivalente a {original}?"
            ),
            correta,
            erradas,
            interacoes,
            dificuldade=2,
            habilidade="frações equivalentes"
        )

    # ========================================================
    # POLÍGONOS / ÂNGULOS / POLIEDROS
    # ========================================================

    if tipo == "poligonos":
        dados = random.choice(
            (
                (
                    "triângulo",
                    3,
                    3
                ),
                (
                    "quadrilátero",
                    4,
                    4
                ),
                (
                    "pentágono",
                    5,
                    5
                ),
                (
                    "hexágono",
                    6,
                    6
                ),
                (
                    "octógono",
                    8,
                    8
                )
            )
        )

        nome, lados, vertices = dados

        if random.random() < 0.5:
            pergunta = (
                f"Um {nome} possui {lados} lados. "
                f"Quantos vértices ele possui?"
            )
            correta = vertices
        else:
            pergunta = (
                f"Um polígono possui {lados} lados. "
                f"Quantos segmentos formam seu contorno?"
            )
            correta = lados

        return numerica_avancada(
            pergunta,
            correta,
            interacoes,
            erros=[
                correta - 1,
                correta + 1,
                correta * 2
            ],
            dificuldade=2,
            habilidade="propriedades de polígonos"
        )

    if tipo == "angulos":
        angulo = random.choice(
            (
                25,
                35,
                45,
                60,
                90,
                110,
                125,
                150
            )
        )

        complemento = (
            180 - angulo
        )

        if random.random() < 0.5:
            if angulo < 90:
                resposta = "agudo"
            elif angulo == 90:
                resposta = "reto"
            else:
                resposta = "obtuso"

            return textual_avancada(
                (
                    f"Um ângulo mede {angulo}°. "
                    f"Como ele é classificado?"
                ),
                resposta,
                [
                    item
                    for item
                    in (
                        "agudo",
                        "reto",
                        "obtuso"
                    )
                    if item != resposta
                ]
                +
                [
                    "raso"
                ],
                interacoes,
                visual={
                    "tipo":
                        "angulo",
                    "graus":
                        angulo
                },
                dificuldade=2,
                habilidade="classificação de ângulos"
            )

        return numerica_avancada(
            (
                f"Dois ângulos formam juntos um ângulo raso "
                f"de 180°. Se um deles mede {angulo}°, "
                f"quanto mede o outro?"
            ),
            complemento,
            interacoes,
            visual={
                "tipo":
                    "angulo",
                "graus":
                    angulo
            },
            erros=[
                90 - angulo,
                angulo,
                180 + angulo
            ],
            dificuldade=3,
            habilidade="ângulos suplementares"
        )

    if tipo == "poliedros":
        solido = random.choice(
            (
                (
                    "cubo",
                    6,
                    12,
                    8
                ),
                (
                    "paralelepípedo",
                    6,
                    12,
                    8
                ),
                (
                    "prisma triangular",
                    5,
                    9,
                    6
                )
            )
        )

        nome, faces, arestas, vertices = solido

        propriedade = random.choice(
            (
                "faces",
                "arestas",
                "vértices"
            )
        )

        if propriedade == "faces":
            correta = faces
        elif propriedade == "arestas":
            correta = arestas
        else:
            correta = vertices

        return numerica_avancada(
            (
                f"Considere um {nome}. "
                f"Quantos {propriedade} ele possui?"
            ),
            correta,
            interacoes,
            erros=[
                faces,
                arestas,
                vertices
            ],
            dificuldade=2,
            habilidade="elementos de poliedros"
        )

    # ========================================================
    # TEMPERATURA
    # ========================================================

    if tipo == "temperatura":
        inicial = random.randint(
            5,
            35
        )

        aumento = random.randint(
            4,
            12
        )

        queda = random.randint(
            3,
            10
        )

        correta = (
            inicial
            +
            aumento
            -
            queda
        )

        return numerica_avancada(
            (
                f"A temperatura era {inicial} °C. "
                f"Subiu {aumento} °C durante o dia e depois "
                f"caiu {queda} °C. Qual foi a temperatura final?"
            ),
            correta,
            interacoes,
            visual={
                "tipo":
                    "termometro",
                "valor":
                    inicial
            },
            erros=[
                inicial + aumento + queda,
                inicial - aumento - queda,
                inicial + aumento
            ],
            dificuldade=2,
            habilidade="variação de temperatura"
        )

    # ========================================================
    # PERÍMETRO / ÁREA
    # ========================================================

    if tipo == "perimetro":
        largura = random.randint(
            4,
            16
        )

        altura = random.randint(
            3,
            12
        )

        if random.random() < 0.45:
            perimetro = (
                2
                *
                (
                    largura
                    +
                    altura
                )
            )

            return numerica_avancada(
                (
                    f"Um retângulo tem perímetro {perimetro} cm "
                    f"e largura {largura} cm. "
                    f"Qual é a altura?"
                ),
                altura,
                interacoes,
                erros=[
                    perimetro - largura,
                    perimetro // 2 - largura + 1,
                    largura
                ],
                dificuldade=3,
                habilidade="dimensão desconhecida pelo perímetro"
            )

        return numerica_avancada(
            (
                f"Um retângulo mede {largura} cm por {altura} cm. "
                f"Qual é seu perímetro?"
            ),
            2 * (largura + altura),
            interacoes,
            visual={
                "tipo":
                    "retangulo_medidas",
                "largura":
                    largura,
                "altura":
                    altura
            },
            erros=[
                largura * altura,
                largura + altura,
                2 * largura + altura
            ],
            dificuldade=2,
            habilidade="perímetro"
        )

    if tipo == "area":
        largura = random.randint(
            4,
            15
        )

        altura = random.randint(
            3,
            12
        )

        area = (
            largura
            *
            altura
        )

        if random.random() < 0.45:
            return numerica_avancada(
                (
                    f"Um retângulo possui área de {area} cm² "
                    f"e largura de {largura} cm. "
                    f"Qual é a altura?"
                ),
                altura,
                interacoes,
                erros=[
                    area - largura,
                    area // 2,
                    largura + altura
                ],
                dificuldade=3,
                habilidade="dimensão desconhecida pela área"
            )

        return numerica_avancada(
            (
                f"Um retângulo mede {largura} cm por {altura} cm. "
                f"Qual é sua área?"
            ),
            area,
            interacoes,
            visual={
                "tipo":
                    "retangulo_medidas",
                "largura":
                    largura,
                "altura":
                    altura,
                "grade":
                    True
            },
            erros=[
                2 * (largura + altura),
                largura + altura,
                area + largura
            ],
            dificuldade=2,
            habilidade="área"
        )

    if tipo == "perimetro_area":
        largura = random.randint(
            4,
            12
        )

        altura = random.randint(
            3,
            10
        )

        area = (
            largura * altura
        )

        perimetro = (
            2
            *
            (
                largura + altura
            )
        )

        if random.random() < 0.5:
            pergunta = (
                f"Um retângulo mede {largura} cm por {altura} cm. "
                f"Quanto a área excede o perímetro numericamente?"
            )
            correta = (
                area - perimetro
                if area >= perimetro
                else perimetro - area
            )
        else:
            pergunta = (
                f"Um retângulo mede {largura} cm por {altura} cm. "
                f"Calcule a soma numérica de sua área com seu perímetro."
            )
            correta = (
                area + perimetro
            )

        return numerica_avancada(
            pergunta,
            correta,
            interacoes,
            erros=[
                area,
                perimetro,
                largura + altura
            ],
            dificuldade=3,
            habilidade="relação entre área e perímetro"
        )

    # ========================================================
    # PROPORÇÃO
    # ========================================================

    if tipo == "proporcao":
        itens = random.randint(
            3,
            8
        )

        custo_unitario = random.randint(
            4,
            15
        )

        custo = (
            itens
            *
            custo_unitario
        )

        nova_qtd = random.randint(
            itens + 2,
            itens * 3
        )

        correta = (
            nova_qtd
            *
            custo_unitario
        )

        return numerica_avancada(
            (
                f"{itens} itens custam R$ {custo}. "
                f"Mantendo o mesmo preço por unidade, "
                f"quanto custam {nova_qtd} itens?"
            ),
            correta,
            interacoes,
            erros=[
                custo + nova_qtd,
                custo * nova_qtd,
                custo_unitario + nova_qtd
            ],
            dificuldade=3,
            habilidade="proporcionalidade direta"
        )

    # ========================================================
    # PLANO CARTESIANO
    # ========================================================

    if tipo == "plano_cartesiano":
        x = random.randint(
            1,
            8
        )

        y = random.randint(
            1,
            8
        )

        dx = random.randint(
            1,
            4
        )

        dy = random.randint(
            1,
            4
        )

        perguntar_x = (
            random.random() < 0.5
        )

        if perguntar_x:
            correta = (
                x + dx
            )

            pergunta = (
                f"O ponto P está em ({x}, {y}). "
                f"Ele se desloca {dx} unidades para a direita "
                f"e {dy} para cima. "
                f"Qual será a nova coordenada X?"
            )

            erros = [
                x,
                y + dy,
                x - dx
            ]

        else:
            correta = (
                y + dy
            )

            pergunta = (
                f"O ponto P está em ({x}, {y}). "
                f"Ele se desloca {dx} unidades para a direita "
                f"e {dy} para cima. "
                f"Qual será a nova coordenada Y?"
            )

            erros = [
                y,
                x + dx,
                y - dy
            ]

        return numerica_avancada(
            pergunta,
            correta,
            interacoes,
            visual={
                "tipo":
                    "plano_cartesiano",
                "x":
                    x,
                "y":
                    y
            },
            erros=erros,
            dificuldade=3,
            habilidade="translação no plano cartesiano"
        )

    # ========================================================
    # VOLUME
    # ========================================================

    if tipo == "volume":
        a = random.randint(
            3,
            8
        )

        b = random.randint(
            3,
            8
        )

        c = random.randint(
            2,
            7
        )

        volume = (
            a * b * c
        )

        if random.random() < 0.4:
            return numerica_avancada(
                (
                    f"Um bloco tem volume {volume} cm³, "
                    f"comprimento {a} cm e largura {b} cm. "
                    f"Qual é a altura?"
                ),
                c,
                interacoes,
                erros=[
                    volume // a,
                    a + b,
                    volume - a - b
                ],
                dificuldade=3,
                habilidade="dimensão desconhecida pelo volume"
            )

        return numerica_avancada(
            (
                f"Um bloco mede {a} cm × {b} cm × {c} cm. "
                f"Qual é seu volume?"
            ),
            volume,
            interacoes,
            visual={
                "tipo":
                    "bloco",
                "a":
                    a,
                "b":
                    b,
                "c":
                    c
            },
            erros=[
                a + b + c,
                a * b + c,
                2 * (a + b + c)
            ],
            dificuldade=2,
            habilidade="volume de bloco retangular"
        )

    return None



# ============================================================
# GERADOR PRINCIPAL
# ============================================================

def gerar_questao(
    tipo,
    interacoes=None,
    nivel=None,
    ano=None,
    complexidade=None,
    operacoes=None,
    desafio=False
):

    # 1) Tenta primeiro o motor progressivo orientado pelo currículo.
    questao_progressiva = gerar_questao_progressiva(
        tipo,
        interacoes=interacoes,
        nivel=nivel,
        ano=ano,
        complexidade=complexidade,
        operacoes=operacoes,
        desafio=desafio
    )

    if questao_progressiva is not None:
        return questao_progressiva

    # 2) Mantém o motor pedagógico avançado anterior como fallback.
    questao_avancada = gerar_questao_avancada(
        tipo,
        interacoes=interacoes,
        nivel=nivel,
        ano=ano,
        complexidade=complexidade,
        operacoes=operacoes,
        desafio=desafio
    )

    if questao_avancada is not None:
        return _anexar_progressao(
            questao_avancada,
            _nivel_progressivo(nivel, ano, tipo),
            ano,
            complexidade,
            operacoes,
            desafio
        )

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
                            "",

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
                            "o",

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
                            "",

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
                            "",

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
                            "",

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
                            "",

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
                            "",

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
                            "",

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
                            "",

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
                            "",

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
                            "",

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
                            "",

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
                            "",

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
                            "",

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
                            "",

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