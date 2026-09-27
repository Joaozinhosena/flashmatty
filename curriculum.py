# ============================================================
# INTERAÇÕES DISPONÍVEIS POR TIPO DE EXERCÍCIO
# ============================================================


def interacoes_para_tipo(tipo):
    """Define as interfaces que cada família de exercício pode usar."""

    if tipo == "figuras_nome":
        return [
            "multipla_escolha",
            "imagem_escolha",
            "associacao",
        ]

    if tipo == "solidos":
        return [
            "imagem_escolha",
            "multipla_escolha",
        ]

    if tipo in ("comprimento", "massa"):
        return [
            "imagem_escolha",
            "multipla_escolha",
            "numero",
            "verdadeiro_falso",
        ]

    if tipo in (
        "probabilidade_basica",
        "probabilidade",
        "probabilidade_desafio",
    ):
        return [
            "multipla_escolha",
            "verdadeiro_falso",
            "imagem_escolha",
        ]

    if tipo == "comparacao":
        return [
            "multipla_escolha",
            "ordenacao",
            "verdadeiro_falso",
        ]

    if tipo == "equivalencia":
        return [
            "multipla_escolha",
            "associacao",
            "verdadeiro_falso",
        ]

    if tipo in (
        "figuras_desafio",
        "angulos",
        "grafico_basico",
        "grafico",
        "grafico_desafio",
        "poligonos",
        "poliedros",
    ):
        return [
            "multipla_escolha",
            "verdadeiro_falso",
        ]

    if tipo == "tempo":
        return [
            "multipla_escolha",
            "numero",
            "verdadeiro_falso",
        ]

    if tipo in (
        "adicao_visual",
        "problema_adicao",
        "subtracao_visual",
        "problema_subtracao",
        "composicao_visual",
        "composicao",
        "decomposicao",
        "multiplicacao_visual",
        "problema_multiplicacao",
        "divisao_visual",
        "problema_divisao",
        "figuras_lados",
        "figuras_planas",
        "lados_vertices",
        "dinheiro_basico",
        "dinheiro",
        "fracao_basica",
        "fracao",
        "temperatura",
        "perimetro",
        "area",
        "perimetro_area",
        "plano_cartesiano",
        "volume",
    ):
        return [
            "multipla_escolha",
            "numero",
            "verdadeiro_falso",
        ]

    return [
        "numero",
        "multipla_escolha",
        "verdadeiro_falso",
    ]


# ============================================================
# ETAPA
# ============================================================


def etapa(
    nome,
    tipo,
    quantidade=6,
    desafio=False,
    interacoes=None,
    nivel_etapa=1,
    complexidade="introducao",
    operacoes=1,
):
    """Cria uma etapa com metadados pedagógicos de progressão."""

    if interacoes is None:
        interacoes = interacoes_para_tipo(tipo)

    return {
        "nome": nome,
        "tipo": tipo,
        "quantidade": quantidade,
        "desafio": desafio,
        "interacoes": interacoes,
        "nivel_etapa": int(nivel_etapa),
        "complexidade": str(complexidade),
        "operacoes": int(operacoes),
    }


# ============================================================
# TRILHA
# ============================================================


def trilha(
    tipo1,
    tipo2=None,
    tipo3=None,
    tipo4=None,
    desafio=None,
):
    """Monta uma progressão real, não apenas uma troca de título."""

    tipo2 = tipo2 or tipo1
    tipo3 = tipo3 or tipo2
    tipo4 = tipo4 or tipo3
    desafio = desafio or tipo4

    return {
        "1": etapa(
            "Primeiros passos",
            tipo1,
            6,
            nivel_etapa=1,
            complexidade="introducao",
            operacoes=1,
        ),
        "2": etapa(
            "Treinando",
            tipo2,
            7,
            nivel_etapa=2,
            complexidade="treino",
            operacoes=1,
        ),
        "3": etapa(
            "Praticando",
            tipo3,
            8,
            nivel_etapa=3,
            complexidade="contexto",
            operacoes=2,
        ),
        "4": etapa(
            "Aplicando",
            tipo4,
            8,
            nivel_etapa=4,
            complexidade="aplicacao",
            operacoes=2,
        ),
        "5": etapa(
            "Desafio final",
            desafio,
            10,
            True,
            nivel_etapa=5,
            complexidade="desafio",
            operacoes=3,
        ),
    }


# ============================================================
# ASSUNTO
# ============================================================


def assunto(
    nome,
    descricao,
    explicacao,
    exemplo,
    tipos,
):
    return {
        "nome": nome,
        "descricao": descricao,
        "explicacao": explicacao,
        "exemplo": exemplo,
        "etapas": trilha(*tipos),
    }


CURRICULO = {

    # ========================================================
    # 1º ANO
    # ========================================================

    "1-ano": {

        "ordem": 1,
        "nome": "1º Ano",
        "icone": "",
        "descricao": "Primeiros passos na matemática.",

        "temas": {

            "numeros": {

                "nome": "Números",
                "icone": "🔢",

                "assuntos": {

                    "composicao-decomposicao": assunto(

                        "Composição e Decomposição",

                        "Descubra como os números são formados.",

                        "Os números podem ser separados em dezenas e unidades.",

                        "34 = 30 + 4",

                        (
                            "composicao_visual",
                            "composicao",
                            "decomposicao",
                            "composicao",
                            "composicao_desafio"
                        )
                    ),

                    "problemas-adicao": assunto(

                        "Problemas de Adição",

                        "Resolva situações usando adição.",

                        "Somar significa juntar quantidades.",

                        "3 maçãs + 2 maçãs = 5 maçãs.",

                        (
                            "adicao_visual",
                            "adicao",
                            "problema_adicao",
                            "problema_adicao",
                            "adicao_desafio"
                        )
                    ),

                    "subtracao": assunto(

                        "Subtração",

                        "Aprenda a retirar e comparar quantidades.",

                        "Subtrair significa retirar uma quantidade de outra.",

                        "8 - 3 = 5",

                        (
                            "subtracao_visual",
                            "subtracao",
                            "subtracao",
                            "problema_subtracao",
                            "subtracao_desafio"
                        )
                    )
                }
            },

            "geometria": {

                "nome": "Geometria",
                "icone": "🔷",

                "assuntos": {

                    "figuras-planas": assunto(

                        "Figuras Geométricas Planas",

                        "Conheça círculo, quadrado, triângulo e retângulo.",

                        "As figuras planas possuem diferentes formas e características.",

                        "Um triângulo possui 3 lados.",

                        (
                            "figuras_nome",
                            "figuras_lados",
                            "figuras_planas",
                            "figuras_planas",
                            "figuras_desafio"
                        )
                    )
                }
            },

            "grandezas-medidas": {

                "nome": "Grandezas e Medidas",
                "icone": "📏",

                "assuntos": {

                    "tempo-calendario": assunto(

                        "Tempo e Calendário",

                        "Aprenda sobre dias, semanas, meses e horas.",

                        "O calendário organiza os dias, semanas e meses.",

                        "Uma semana possui 7 dias.",

                        (
                            "calendario_basico",
                            "calendario",
                            "tempo",
                            "calendario",
                            "calendario_desafio"
                        )
                    ),

                    "sistema-monetario": assunto(

                        "Sistema Monetário",

                        "Aprenda sobre cédulas e moedas.",

                        "Usamos reais e centavos para representar valores.",

                        "R$ 2 + R$ 3 = R$ 5.",

                        (
                            "dinheiro_basico",
                            "dinheiro",
                            "dinheiro",
                            "problema_dinheiro",
                            "dinheiro_desafio"
                        )
                    )
                }
            },

            "probabilidade-estatistica": {

                "nome": "Probabilidade e Estatística",
                "icone": "📊",

                "assuntos": {

                    "probabilidade": assunto(

                        "Probabilidade",

                        "Descubra possibilidades.",

                        "Probabilidade ajuda a pensar sobre o que pode acontecer.",

                        "Uma moeda pode cair em cara ou coroa.",

                        (
                            "probabilidade_basica",
                            "probabilidade",
                            "probabilidade",
                            "probabilidade",
                            "probabilidade_desafio"
                        )
                    ),

                    "analise-graficos": assunto(

                        "Análise de Gráficos",

                        "Aprenda a interpretar dados.",

                        "Gráficos representam informações de maneira visual.",

                        "Uma barra maior representa uma quantidade maior.",

                        (
                            "grafico_basico",
                            "grafico",
                            "grafico",
                            "grafico",
                            "grafico_desafio"
                        )
                    )
                }
            }
        }
    },


    # ========================================================
    # 2º ANO
    # ========================================================

    "2-ano": {

        "ordem": 2,
        "nome": "2º Ano",
        "icone": "",
        "descricao": "Novas operações e formas.",

        "temas": {

            "numeros": {

                "nome": "Números",
                "icone": "🔢",

                "assuntos": {

                    "numeros-decimais": assunto(
                        "Números Decimais",
                        "Conheça números com parte decimal.",
                        "Os números decimais representam partes de uma unidade.",
                        "2,5 possui parte inteira 2.",
                        ("decimal", "decimal", "decimal", "decimal", "decimal")
                    ),

                    "introducao-multiplicacao": assunto(
                        "Introdução à Multiplicação",
                        "Entenda grupos de quantidades.",
                        "Multiplicar pode representar uma soma repetida.",
                        "3 × 2 = 2 + 2 + 2.",
                        (
                            "multiplicacao_visual",
                            "multiplicacao_visual",
                            "multiplicacao",
                            "multiplicacao",
                            "multiplicacao_desafio"
                        )
                    ),

                    "multiplicacao": assunto(
                        "Multiplicação",
                        "Treine multiplicações.",
                        "Multiplicação representa grupos iguais.",
                        "4 × 3 = 12.",
                        (
                            "multiplicacao_visual",
                            "multiplicacao",
                            "multiplicacao",
                            "problema_multiplicacao",
                            "multiplicacao_desafio"
                        )
                    ),

                    "dobro-metade-triplo-terca": assunto(
                        "Dobro, Metade, Triplo e Terça Parte",
                        "Aprenda relações entre quantidades.",
                        "Dobro é duas vezes, triplo é três vezes.",
                        "Dobro de 5 = 10.",
                        (
                            "dobro",
                            "metade",
                            "triplo",
                            "terca",
                            "dobro_metade_desafio"
                        )
                    ),

                    "adicao": assunto(
                        "Adição",
                        "Pratique somas maiores.",
                        "Adição junta quantidades.",
                        "25 + 13 = 38.",
                        (
                            "adicao",
                            "adicao",
                            "adicao",
                            "problema_adicao",
                            "adicao_desafio"
                        )
                    ),

                    "subtracao": assunto(
                        "Subtração",
                        "Pratique subtrações.",
                        "Subtração representa retirar ou descobrir uma diferença.",
                        "30 - 12 = 18.",
                        (
                            "subtracao",
                            "subtracao",
                            "subtracao",
                            "problema_subtracao",
                            "subtracao_desafio"
                        )
                    ),

                    "comparacao-quantidades": assunto(
                        "Comparação de Quantidades",
                        "Compare números.",
                        "Podemos identificar qual número é maior ou menor.",
                        "10 é maior que 7.",
                        ("comparacao", "comparacao", "comparacao", "comparacao", "comparacao")
                    ),

                    "igualdade-equivalencia": assunto(
                        "Igualdade e Equivalência",
                        "Descubra expressões equivalentes.",
                        "Duas expressões são equivalentes quando possuem o mesmo resultado.",
                        "3 + 2 = 4 + 1.",
                        ("equivalencia", "equivalencia", "equivalencia", "equivalencia", "equivalencia")
                    )
                }
            },

            "geometria": {

                "nome": "Geometria",
                "icone": "🧊",

                "assuntos": {

                    "figuras-solidas": assunto(
                        "Figuras Sólidas",
                        "Conheça cubo, esfera e outros sólidos.",
                        "Sólidos geométricos ocupam espaço.",
                        "Uma bola lembra uma esfera.",
                        ("solidos", "solidos", "solidos", "solidos", "solidos")
                    ),

                    "lados-vertices": assunto(
                        "Lados e Vértices",
                        "Observe características das figuras.",
                        "Os encontros entre lados formam vértices.",
                        "Um quadrado possui 4 lados e 4 vértices.",
                        (
                            "lados_vertices",
                            "lados_vertices",
                            "lados_vertices",
                            "lados_vertices",
                            "lados_vertices"
                        )
                    )
                }
            },

            "grandezas-medidas": {

                "nome": "Grandezas e Medidas",
                "icone": "📐",

                "assuntos": {

                    "comprimento": assunto(
                        "Medição de Comprimento",
                        "Aprenda metros e centímetros.",
                        "Comprimento indica o tamanho de algo.",
                        "1 metro = 100 centímetros.",
                        ("comprimento", "comprimento", "comprimento", "comprimento", "comprimento")
                    ),

                    "capacidade-massa": assunto(
                        "Capacidade e Massa",
                        "Aprenda medidas de capacidade e massa.",
                        "Quilogramas medem massa e litros podem medir capacidade.",
                        "1 kg = 1000 g.",
                        ("massa", "massa", "massa", "massa", "massa")
                    )
                }
            }
        }
    },


    # ========================================================
    # 3º ANO
    # ========================================================

    "3-ano": {

        "ordem": 3,
        "nome": "3º Ano",
        "icone": "",
        "descricao": "Operações, frações e medidas.",

        "temas": {

            "numeros": {

                "nome": "Números",
                "icone": "🔢",

                "assuntos": {

                    "unidade-milhar": assunto(
                        "Unidade de Milhar",
                        "Leia números maiores.",
                        "Uma unidade de milhar representa 1000 unidades.",
                        "3000 = 3 milhares.",
                        ("milhar", "milhar", "milhar", "milhar", "milhar")
                    ),

                    "decomposicao-quatro-ordens": assunto(
                        "Decomposição até 4 Ordens",
                        "Decomponha números.",
                        "Podemos separar milhares, centenas, dezenas e unidades.",
                        "2345 = 2000 + 300 + 40 + 5.",
                        (
                            "decomposicao4",
                            "decomposicao4",
                            "decomposicao4",
                            "decomposicao4",
                            "decomposicao4"
                        )
                    ),

                    "quatro-operacoes": assunto(
                        "As Quatro Operações",
                        "Misture diferentes operações.",
                        "Adição, subtração, multiplicação e divisão resolvem diferentes situações.",
                        "20 ÷ 4 = 5.",
                        (
                            "adicao",
                            "subtracao",
                            "multiplicacao",
                            "quatro_operacoes",
                            "quatro_operacoes"
                        )
                    ),

                    "divisao": assunto(
                        "Divisão",
                        "Aprenda a repartir.",
                        "Dividir significa repartir em grupos iguais.",
                        "12 ÷ 3 = 4.",
                        (
                            "divisao_visual",
                            "divisao",
                            "divisao",
                            "problema_divisao",
                            "divisao_desafio"
                        )
                    ),

                    "multiplicacao-avancada": assunto(
                        "Multiplicação Avançada",
                        "Resolva multiplicações maiores.",
                        "Podemos multiplicar números maiores usando estratégias.",
                        "12 × 4 = 48.",
                        (
                            "multiplicacao",
                            "multiplicacao_avancada",
                            "multiplicacao_avancada",
                            "problema_multiplicacao",
                            "multiplicacao_desafio"
                        )
                    ),

                    "fracao": assunto(
                        "Frações",
                        "Entenda partes de um todo.",
                        "Frações representam partes iguais.",
                        "1/2 representa uma de duas partes iguais.",
                        (
                            "fracao_basica",
                            "fracao",
                            "fracao",
                            "fracao",
                            "fracao_desafio"
                        )
                    )
                }
            },

            "geometria": {

                "nome": "Geometria",
                "icone": "🔷",

                "assuntos": {

                    "poligonos": assunto(
                        "Classificação de Polígonos",
                        "Classifique figuras pelos lados.",
                        "Polígonos podem ser classificados pelo número de lados.",
                        "Um pentágono possui 5 lados.",
                        ("poligonos", "poligonos", "poligonos", "poligonos", "poligonos")
                    )
                }
            },

            "grandezas-medidas": {

                "nome": "Grandezas e Medidas",
                "icone": "🌡️",

                "assuntos": {

                    "temperatura": assunto(
                        "Temperatura Celsius",
                        "Leia temperaturas.",
                        "Temperatura pode ser medida em graus Celsius.",
                        "25 °C.",
                        ("temperatura", "temperatura", "temperatura", "temperatura", "temperatura")
                    ),

                    "horas-minutos": assunto(
                        "Horas e Minutos",
                        "Trabalhe com medidas de tempo.",
                        "Uma hora possui 60 minutos.",
                        "2 horas = 120 minutos.",
                        ("tempo", "tempo", "tempo", "tempo", "tempo")
                    )
                }
            }
        }
    },


    # ========================================================
    # 4º ANO
    # ========================================================

    "4-ano": {

        "ordem": 4,
        "nome": "4º Ano",
        "icone": "",
        "descricao": "Geometria e medidas.",

        "temas": {

            "geometria": {

                "nome": "Geometria",
                "icone": "📐",

                "assuntos": {

                    "angulos": assunto(
                        "Ângulos",
                        "Aprenda a identificar ângulos.",
                        "Ângulos podem ser agudos, retos ou obtusos.",
                        "90° é um ângulo reto.",
                        ("angulos", "angulos", "angulos", "angulos", "angulos")
                    )
                }
            },

            "grandezas-medidas": {

                "nome": "Grandezas e Medidas",
                "icone": "📏",

                "assuntos": {

                    "perimetro-area": assunto(
                        "Perímetro e Área",
                        "Calcule medidas de figuras.",
                        "Perímetro mede o contorno e área mede a superfície.",
                        "Retângulo 3 × 4 possui área 12.",
                        (
                            "perimetro",
                            "area",
                            "perimetro_area",
                            "perimetro_area",
                            "perimetro_area"
                        )
                    )
                }
            }
        }
    },


    # ========================================================
    # 5º ANO
    # ========================================================

    "5-ano": {

        "ordem": 5,
        "nome": "5º Ano",
        "icone": "",
        "descricao": "Desafios matemáticos mais avançados.",

        "temas": {

            "matematica": {

                "nome": "Matemática",
                "icone": "🎓",

                "assuntos": {

                    "proporcionalidade": assunto(
                        "Grandezas Diretamente Proporcionais",
                        "Aprenda relações proporcionais.",
                        "Quando uma quantidade aumenta na mesma razão que outra, existe proporcionalidade.",
                        "2 itens custam 6 reais; 4 itens custam 12 reais.",
                        ("proporcao", "proporcao", "proporcao", "proporcao", "proporcao")
                    ),

                    "plano-cartesiano": assunto(
                        "Plano Cartesiano",
                        "Localize pontos.",
                        "Um ponto pode ser representado por coordenadas (x, y).",
                        "(3, 2).",
                        (
                            "plano_cartesiano",
                            "plano_cartesiano",
                            "plano_cartesiano",
                            "plano_cartesiano",
                            "plano_cartesiano"
                        )
                    ),

                    "poliedros": assunto(
                        "Poliedros",
                        "Conheça sólidos com faces planas.",
                        "Poliedros possuem faces formadas por polígonos.",
                        "O cubo possui 6 faces.",
                        ("poliedros", "poliedros", "poliedros", "poliedros", "poliedros")
                    ),

                    "conversao-medidas": assunto(
                        "Conversão de Medidas",
                        "Converta unidades.",
                        "Uma medida pode ser representada em unidades diferentes.",
                        "2 m = 200 cm.",
                        ("conversao", "conversao", "conversao", "conversao", "conversao")
                    ),

                    "volume": assunto(
                        "Volume",
                        "Calcule o espaço ocupado.",
                        "Volume mede o espaço ocupado por um sólido.",
                        "2 × 3 × 4 = 24 unidades cúbicas.",
                        ("volume", "volume", "volume", "volume", "volume")
                    ),

                    "graficos": assunto(
                        "Gráficos de Barras e Pizza",
                        "Analise informações em gráficos.",
                        "Gráficos ajudam a comparar e interpretar dados.",
                        "A maior barra representa a maior quantidade.",
                        ("grafico", "grafico", "grafico", "grafico", "grafico_desafio")
                    )
                }
            }
        }
    }
}

# ============================================================
# PROGRESSÃO PEDAGÓGICA POR ANO
# ============================================================
#
# O mesmo tipo de exercício pode aparecer em séries diferentes.
# Por isso cada etapa recebe um nível global de 1 a 7, além do
# nível interno da trilha (1 a 5). O game.py usa esses dados para
# escolher amplitude numérica, quantidade de etapas de raciocínio,
# incógnitas, interpretação e composição de operações.
# ============================================================

NIVEIS_POR_ANO = {
    1: (1, 1, 2, 2, 3),
    2: (2, 2, 3, 3, 4),
    3: (3, 3, 4, 4, 5),
    4: (4, 4, 5, 5, 6),
    5: (5, 5, 6, 6, 7),
}


def _aplicar_progressao_curricular():
    for ano_id, dados_ano in CURRICULO.items():
        numero_ano = int(dados_ano.get("ordem") or str(ano_id).split("-")[0])
        niveis = NIVEIS_POR_ANO.get(numero_ano, NIVEIS_POR_ANO[3])

        for tema in dados_ano.get("temas", {}).values():
            for dados_assunto in tema.get("assuntos", {}).values():
                for etapa_id, dados_etapa in dados_assunto.get("etapas", {}).items():
                    posicao = max(1, min(5, int(etapa_id)))
                    nivel_global = niveis[posicao - 1]

                    dados_etapa["ano"] = numero_ano
                    dados_etapa["nivel"] = nivel_global
                    dados_etapa["nivel_etapa"] = posicao

                    # A quantidade de operações cresce mais nas séries maiores.
                    if posicao <= 2:
                        operacoes = 1
                    elif posicao <= 4:
                        operacoes = 2 if numero_ano >= 2 else 1
                    else:
                        operacoes = 3 if numero_ano >= 3 else 2

                    dados_etapa["operacoes"] = operacoes
                    dados_etapa["desafio"] = bool(posicao == 5 or dados_etapa.get("desafio"))


_aplicar_progressao_curricular()
