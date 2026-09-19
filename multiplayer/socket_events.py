import time

from flask import request, session

from flask_socketio import (
    emit,
    join_room
)

from multiplayer import socketio

from multiplayer.room_manager import (
    LOCK,
    SALAS,
    buscar_sala,
    serializar_jogadores,
    ranking
)

from multiplayer.questions import (
    gerar_partida
)

from multiplayer.scoring import (
    calcular_pontos
)


# ============================================================
# CONFIGURAÇÕES
# ============================================================

MINIMO_JOGADORES = 1

TOLERANCIA_RESPOSTA = 1.0


# ============================================================
# AUXILIARES
# ============================================================

def obter_jogador_sessao():

    return str(
        session.get(
            "multiplayer_jogador",
            ""
        )
        or
        ""
    ).strip()


def obter_jogador_evento(
    dados=None
):
    """
    Utiliza preferencialmente o ID armazenado
    na sessão Flask.

    O ID enviado pelo navegador é usado apenas
    como fallback.
    """

    dados = dados or {}

    jogador_sessao = (
        obter_jogador_sessao()
    )

    jogador_recebido = str(
        dados.get(
            "jogador_id",
            ""
        )
        or
        ""
    ).strip()


    # Se existem os dois e são diferentes,
    # há inconsistência de identidade.
    if (
        jogador_sessao
        and
        jogador_recebido
        and
        jogador_sessao
        !=
        jogador_recebido
    ):

        return ""


    return (
        jogador_sessao
        or
        jogador_recebido
    )


def jogador_e_host(
    sala,
    jogador_id
):

    if not sala:
        return False

    return (
        bool(jogador_id)
        and
        str(jogador_id)
        ==
        str(
            sala.get(
                "host_id",
                ""
            )
        )
    )


def jogadores_online(
    sala
):

    if not sala:
        return []

    return [

        jogador

        for jogador
        in sala[
            "jogadores"
        ].values()

        if jogador.get(
            "online",
            False
        )

    ]


def ids_jogadores_online(
    sala
):

    return {

        str(
            jogador["id"]
        )

        for jogador
        in jogadores_online(
            sala
        )

    }


def atualizar_atividade(
    sala
):

    if not sala:
        return

    sala[
        "ultima_atividade"
    ] = time.time()


# ============================================================
# ENTRAR NO SOCKET DA SALA
# ============================================================

@socketio.on(
    "entrar_socket"
)
def entrar_socket(
    dados
):

    dados = dados or {}

    codigo = str(
        dados.get(
            "codigo",
            ""
        )
        or
        ""
    ).strip()


    jogador_id = (
        obter_jogador_evento(
            dados
        )
    )


    if not codigo:

        emit(
            "erro_sala",
            {
                "mensagem":
                    "Código da sala inválido."
            }
        )

        return


    if not jogador_id:

        emit(
            "erro_sala",
            {
                "mensagem":
                    "Jogador inválido."
            }
        )

        return


    sala = buscar_sala(
        codigo
    )


    if not sala:

        emit(
            "erro_sala",
            {
                "mensagem":
                    "Sala não encontrada."
            }
        )

        return


    with LOCK:

        if (
            jogador_id
            not in
            sala[
                "jogadores"
            ]
        ):

            emit(
                "erro_sala",
                {
                    "mensagem":
                        "Jogador não pertence a esta sala."
                }
            )

            return


        jogador = (
            sala[
                "jogadores"
            ][
                jogador_id
            ]
        )


        # Atualiza o Socket atual.
        jogador[
            "sid"
        ] = request.sid

        jogador[
            "online"
        ] = True


        atualizar_atividade(
            sala
        )


    # Adiciona a conexão Socket.IO
    # ao room correspondente.
    join_room(
        codigo
    )


    emit(
        "jogadores_atualizados",
        {
            "jogadores":
                serializar_jogadores(
                    codigo
                )
        },
        to=codigo
    )


# ============================================================
# INICIAR PARTIDA
# ============================================================

@socketio.on(
    "iniciar_partida"
)
def iniciar_partida(
    dados
):

    dados = dados or {}


    codigo = str(
        dados.get(
            "codigo",
            ""
        )
        or
        ""
    ).strip()


    sala = buscar_sala(
        codigo
    )


    if not sala:

        emit(
            "erro_sala",
            {
                "mensagem":
                    "Sala não encontrada."
            }
        )

        return


    jogador_id = (
        obter_jogador_evento(
            dados
        )
    )


    if not jogador_e_host(
        sala,
        jogador_id
    ):

        emit(
            "erro_sala",
            {
                "mensagem":
                    "Somente o anfitrião pode iniciar a partida."
            }
        )

        return


    with LOCK:

        if (
            sala.get(
                "estado"
            )
            !=
            "lobby"
        ):

            emit(
                "erro_sala",
                {
                    "mensagem":
                        "A partida já foi iniciada."
                }
            )

            return


        online = (
            jogadores_online(
                sala
            )
        )


        if (
            len(online)
            <
            MINIMO_JOGADORES
        ):

            emit(
                "erro_sala",
                {
                    "mensagem":
                        "Não existem jogadores suficientes para iniciar."
                }
            )

            return


        config = (
            sala.get(
                "configuracao",
                {}
            )
        )


        try:

            quantidade = int(
                config.get(
                    "quantidade",
                    10
                )
            )

        except (
            TypeError,
            ValueError
        ):

            quantidade = 10


        try:

            tempo = int(
                config.get(
                    "tempo",
                    20
                )
            )

        except (
            TypeError,
            ValueError
        ):

            tempo = 20


        quantidade = max(
            1,
            min(
                50,
                quantidade
            )
        )


        tempo = max(
            5,
            min(
                120,
                tempo
            )
        )


        config[
            "quantidade"
        ] = quantidade

        config[
            "tempo"
        ] = tempo


        try:

            questoes = (
                gerar_partida(

                    config.get(
                        "assunto",
                        "misto"
                    ),

                    quantidade

                )
            )

        except Exception as erro:

            print(
                "ERRO AO GERAR PARTIDA:",
                erro
            )


            emit(
                "erro_sala",
                {
                    "mensagem":
                        "Erro ao gerar as perguntas."
                }
            )

            return


        if not questoes:

            emit(
                "erro_sala",
                {
                    "mensagem":
                        "Não foi possível gerar as perguntas."
                }
            )

            return


        sala[
            "questoes"
        ] = questoes

        sala[
            "estado"
        ] = "jogando"

        sala[
            "rodada"
        ] = 0

        sala[
            "questao_atual"
        ] = None

        sala[
            "inicio_questao"
        ] = None

        sala[
            "respostas_rodada"
        ] = set()

        sala[
            "ranking_rodada"
        ] = []


        # Reinicia as estatísticas.
        for jogador in (
            sala[
                "jogadores"
            ].values()
        ):

            jogador[
                "pontos"
            ] = 0

            jogador[
                "acertos"
            ] = 0

            jogador[
                "erros"
            ] = 0

            jogador[
                "sequencia"
            ] = 0

            jogador[
                "maior_sequencia"
            ] = 0

            jogador[
                "respondeu"
            ] = False


        atualizar_atividade(
            sala
        )


    print(
        f"PARTIDA INICIADA | "
        f"SALA {codigo} | "
        f"{len(online)} JOGADORES"
    )


    emit(
        "partida_iniciada",
        {
            "codigo":
                codigo
        },
        to=codigo
    )


# ============================================================
# TIMER DO SERVIDOR
# ============================================================

def vigiar_tempo_questao(
    codigo,
    numero_rodada,
    inicio_questao,
    tempo_limite
):
    """
    Timer executado pelo servidor.

    Dessa forma a partida não depende
    exclusivamente do navegador do host.
    """

    socketio.sleep(
        tempo_limite
        +
        0.5
    )


    sala = buscar_sala(
        codigo
    )


    if not sala:
        return


    deve_encerrar = False


    with LOCK:

        if (
            sala.get(
                "estado"
            )
            !=
            "jogando"
        ):
            return


        if not sala.get(
            "questao_atual"
        ):
            return


        # Verifica se ainda estamos
        # na mesma rodada.
        rodada_atual = (
            sala.get(
                "rodada",
                0
            )
            +
            1
        )


        if (
            rodada_atual
            !=
            numero_rodada
        ):
            return


        inicio_atual = (
            sala.get(
                "inicio_questao"
            )
        )


        if (
            inicio_atual
            !=
            inicio_questao
        ):
            return


        decorrido = (
            time.time()
            -
            inicio_atual
        )


        if (
            decorrido
            >=
            tempo_limite
        ):

            deve_encerrar = True


    if deve_encerrar:

        encerrar_rodada(
            codigo,
            motivo="tempo"
        )


# ============================================================
# PRÓXIMA QUESTÃO
# ============================================================

@socketio.on(
    "proxima_questao"
)
def proxima_questao(
    dados
):

    dados = dados or {}


    codigo = str(
        dados.get(
            "codigo",
            ""
        )
        or
        ""
    ).strip()


    sala = buscar_sala(
        codigo
    )


    if not sala:
        return


    jogador_id = (
        obter_jogador_evento(
            dados
        )
    )


    if not jogador_e_host(
        sala,
        jogador_id
    ):
        return


    with LOCK:

        if (
            sala.get(
                "estado"
            )
            !=
            "jogando"
        ):
            return


        # Já existe uma questão ativa.
        if sala.get(
            "questao_atual"
        ):
            return


        # Proteção adicional.
        if (
            sala[
                "rodada"
            ]
            >=
            len(
                sala[
                    "questoes"
                ]
            )
        ):

            sala[
                "estado"
            ] = "finalizado"


            classificacao = (
                ranking(
                    codigo
                )
            )


            socketio.emit(
                "partida_finalizada",
                {
                    "ranking":
                        classificacao
                },
                to=codigo
            )

            return


        questao = (
            sala[
                "questoes"
            ][
                sala[
                    "rodada"
                ]
            ]
        )


        sala[
            "questao_atual"
        ] = questao


        inicio_questao = (
            time.time()
        )


        sala[
            "inicio_questao"
        ] = inicio_questao


        sala[
            "respostas_rodada"
        ] = set()


        sala[
            "ranking_rodada"
        ] = []


        for jogador in (
            sala[
                "jogadores"
            ].values()
        ):

            jogador[
                "respondeu"
            ] = False


        numero_rodada = (
            sala[
                "rodada"
            ]
            +
            1
        )


        total = len(
            sala[
                "questoes"
            ]
        )


        tempo = int(
            sala[
                "configuracao"
            ][
                "tempo"
            ]
        )


        atualizar_atividade(
            sala
        )


    socketio.emit(
        "nova_questao",
        {
            "rodada":
                numero_rodada,

            "total":
                total,

            "pergunta":
                questao[
                    "pergunta"
                ],

            "alternativas":
                questao[
                    "alternativas"
                ],

            "tempo":
                tempo
        },
        to=codigo
    )


    # Inicia o relógio também no servidor.
    socketio.start_background_task(

        vigiar_tempo_questao,

        codigo,

        numero_rodada,

        inicio_questao,

        tempo

    )


# ============================================================
# RESPONDER
# ============================================================

@socketio.on(
    "responder"
)
def responder(
    dados
):

    dados = dados or {}


    codigo = str(
        dados.get(
            "codigo",
            ""
        )
        or
        ""
    ).strip()


    resposta = str(
        dados.get(
            "resposta",
            ""
        )
        or
        ""
    ).strip()


    jogador_id = (
        obter_jogador_evento(
            dados
        )
    )


    sala = buscar_sala(
        codigo
    )


    if (
        not sala
        or
        sala.get(
            "estado"
        )
        !=
        "jogando"
    ):
        return


    acertou = False

    pontos = 0

    sequencia_atual = 0

    todos_responderam = False


    with LOCK:

        if (
            jogador_id
            not in
            sala[
                "jogadores"
            ]
        ):
            return


        jogador = (
            sala[
                "jogadores"
            ][
                jogador_id
            ]
        )


        # O socket que respondeu precisa ser
        # o socket atualmente associado ao jogador.
        sid_jogador = (
            jogador.get(
                "sid"
            )
        )


        if (
            sid_jogador
            and
            sid_jogador
            !=
            request.sid
        ):
            return


        if not jogador.get(
            "online",
            False
        ):
            return


        if jogador.get(
            "respondeu",
            False
        ):
            return


        questao = (
            sala.get(
                "questao_atual"
            )
        )


        if not questao:
            return


        inicio = (
            sala.get(
                "inicio_questao"
            )
        )


        if not inicio:
            return


        tempo_limite = int(
            sala[
                "configuracao"
            ][
                "tempo"
            ]
        )


        decorrido = (
            time.time()
            -
            inicio
        )


        # Respostas excessivamente atrasadas
        # não são aceitas.
        if (
            decorrido
            >
            tempo_limite
            +
            TOLERANCIA_RESPOSTA
        ):
            return


        jogador[
            "respondeu"
        ] = True


        sala[
            "respostas_rodada"
        ].add(
            jogador_id
        )


        acertou = (

            resposta.casefold()

            ==

            str(
                questao[
                    "correta"
                ]
            )
            .strip()
            .casefold()

        )


        if acertou:

            jogador[
                "acertos"
            ] += 1


            jogador[
                "sequencia"
            ] += 1


            sequencia_atual = (
                jogador[
                    "sequencia"
                ]
            )


            jogador[
                "maior_sequencia"
            ] = max(

                jogador[
                    "maior_sequencia"
                ],

                sequencia_atual

            )


            # Usa o scoring.py.
            pontos = (
                calcular_pontos(

                    acertou=True,

                    tempo_resposta=
                        decorrido,

                    tempo_limite=
                        tempo_limite,

                    sequencia=
                        sequencia_atual

                )
            )


            jogador[
                "pontos"
            ] += pontos


        else:

            jogador[
                "erros"
            ] += 1


            jogador[
                "sequencia"
            ] = 0


            sequencia_atual = 0


            pontos = 0


        atualizar_atividade(
            sala
        )


        # ---------------------------------------------
        # JOGADORES ONLINE
        # ---------------------------------------------

        online_ids = (
            ids_jogadores_online(
                sala
            )
        )


        responderam_online = (

            sala[
                "respostas_rodada"
            ]

            &

            online_ids

        )


        todos_responderam = (

            len(
                online_ids
            )
            >
            0

            and

            len(
                responderam_online
            )
            >=
            len(
                online_ids
            )

        )


        total_pontos = (
            jogador[
                "pontos"
            ]
        )


    # Apenas o jogador que respondeu recebe
    # esse retorno.
    emit(
        "resposta_recebida",
        {
            "correto":
                acertou,

            "pontos":
                pontos,

            "total_pontos":
                total_pontos,

            "sequencia":
                sequencia_atual
        }
    )


    # Se todos responderam, não é necessário
    # aguardar o cronômetro acabar.
    if todos_responderam:

        encerrar_rodada(
            codigo,
            motivo="todos_responderam"
        )


# ============================================================
# TEMPO ESGOTADO PELO CLIENTE
# ============================================================

@socketio.on(
    "tempo_esgotado"
)
def tempo_esgotado(
    dados
):

    dados = dados or {}


    codigo = str(
        dados.get(
            "codigo",
            ""
        )
        or
        ""
    ).strip()


    sala = buscar_sala(
        codigo
    )


    if not sala:
        return


    jogador_id = (
        obter_jogador_evento(
            dados
        )
    )


    if not jogador_e_host(
        sala,
        jogador_id
    ):
        return


    with LOCK:

        inicio = (
            sala.get(
                "inicio_questao"
            )
        )


        if not inicio:
            return


        tempo_limite = int(
            sala[
                "configuracao"
            ][
                "tempo"
            ]
        )


        decorrido = (
            time.time()
            -
            inicio
        )


    # Impede que o host finalize
    # a rodada antes da hora.
    if (
        decorrido
        <
        tempo_limite
        -
        0.3
    ):
        return


    encerrar_rodada(
        codigo,
        motivo="tempo"
    )


# ============================================================
# ENCERRAR RODADA
# ============================================================

def encerrar_rodada(
    codigo,
    motivo="normal"
):

    sala = buscar_sala(
        codigo
    )


    if not sala:
        return


    with LOCK:

        if (
            sala.get(
                "estado"
            )
            !=
            "jogando"
        ):
            return


        questao = (
            sala.get(
                "questao_atual"
            )
        )


        # Se já foi limpa, outra chamada já
        # encerrou essa rodada.
        if not questao:
            return


        correta = (
            questao[
                "correta"
            ]
        )


        # =============================================
        # JOGADORES QUE NÃO RESPONDERAM
        # =============================================

        for jogador in (
            sala[
                "jogadores"
            ].values()
        ):

            if not jogador.get(
                "online",
                False
            ):
                continue


            if jogador.get(
                "respondeu",
                False
            ):
                continue


            jogador[
                "respondeu"
            ] = True


            jogador[
                "erros"
            ] += 1


            jogador[
                "sequencia"
            ] = 0


        # =============================================
        # LIMPA QUESTÃO ANTES DE EMITIR
        # =============================================

        sala[
            "questao_atual"
        ] = None


        sala[
            "inicio_questao"
        ] = None


        sala[
            "rodada"
        ] += 1


        classificacao = (
            ranking(
                codigo
            )
        )


        terminou = (

            sala[
                "rodada"
            ]

            >=

            len(
                sala[
                    "questoes"
                ]
            )

        )


        if terminou:

            sala[
                "estado"
            ] = "finalizado"


        atualizar_atividade(
            sala
        )


    # socketio.emit é usado porque esta função
    # também pode ser chamada por background task.
    socketio.emit(
        "rodada_finalizada",
        {
            "correta":
                correta,

            "ranking":
                classificacao,

            "terminou":
                terminou,

            "motivo":
                motivo
        },
        to=codigo
    )


    if terminou:

        socketio.emit(
            "partida_finalizada",
            {
                "ranking":
                    classificacao
            },
            to=codigo
        )


# ============================================================
# RANKING FINAL
# ============================================================

@socketio.on(
    "pedir_ranking"
)
def pedir_ranking(
    dados
):

    dados = dados or {}


    codigo = str(
        dados.get(
            "codigo",
            ""
        )
        or
        ""
    ).strip()


    sala = buscar_sala(
        codigo
    )


    if not sala:

        emit(
            "ranking_final",
            {
                "ranking": []
            }
        )

        return


    emit(
        "ranking_final",
        {
            "ranking":
                ranking(
                    codigo
                )
        }
    )


# ============================================================
# DESCONECTOU
# ============================================================

@socketio.on(
    "disconnect"
)
def desconectou():

    sid = request.sid

    salas_afetadas = []


    with LOCK:

        for codigo, sala in list(
            SALAS.items()
        ):

            encontrou = False


            for jogador in (
                sala[
                    "jogadores"
                ].values()
            ):

                # Só marca offline se o SID ainda
                # pertence a essa conexão.
                if (
                    jogador.get(
                        "sid"
                    )
                    ==
                    sid
                ):

                    jogador[
                        "online"
                    ] = False


                    jogador[
                        "sid"
                    ] = None


                    atualizar_atividade(
                        sala
                    )


                    salas_afetadas.append(
                        codigo
                    )


                    encontrou = True

                    break


            if encontrou:
                continue


    # =============================================
    # AVISA OS OUTROS JOGADORES
    # =============================================

    for codigo in (
        salas_afetadas
    ):

        socketio.emit(
            "jogadores_atualizados",
            {
                "jogadores":
                    serializar_jogadores(
                        codigo
                    )
            },
            to=codigo
        )


        sala = buscar_sala(
            codigo
        )


        if not sala:
            continue


        if (
            sala.get(
                "estado"
            )
            !=
            "jogando"
        ):
            continue


        if not sala.get(
            "questao_atual"
        ):
            continue


        todos_responderam = False


        with LOCK:

            online_ids = (
                ids_jogadores_online(
                    sala
                )
            )


            responderam = (

                sala[
                    "respostas_rodada"
                ]

                &

                online_ids

            )


            todos_responderam = (

                len(
                    online_ids
                )
                >
                0

                and

                len(
                    responderam
                )
                >=
                len(
                    online_ids
                )

            )


        if todos_responderam:

            encerrar_rodada(
                codigo,
                motivo="desconexao"
            )