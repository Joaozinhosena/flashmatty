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

from multiplayer.questions import gerar_partida


# ============================================================
# AUXILIARES
# ============================================================

def obter_jogador_sessao():
    return str(
        session.get(
            "multiplayer_jogador",
            ""
        )
    )


def jogador_e_host(sala, jogador_id):
    return (
        bool(jogador_id)
        and
        jogador_id == str(sala["host_id"])
    )


def jogadores_online(sala):
    return [
        jogador
        for jogador in sala["jogadores"].values()
        if jogador.get("online", False)
    ]


def ids_jogadores_online(sala):
    return {
        str(jogador["id"])
        for jogador in jogadores_online(sala)
    }


# ============================================================
# ENTRAR NO SOCKET DA SALA
# ============================================================

@socketio.on("entrar_socket")
def entrar_socket(dados):

    codigo = str(
        dados.get("codigo", "")
    ).strip()

    # Primeiro tenta utilizar o ID recebido pelo navegador.
    jogador_id = str(
        dados.get("jogador_id", "")
    ).strip()

    # Se não veio, utiliza a sessão Flask.
    if not jogador_id:
        jogador_id = obter_jogador_sessao()

    sala = buscar_sala(codigo)

    if not sala:

        emit(
            "erro_sala",
            {
                "mensagem": "Sala não encontrada."
            }
        )

        return

    with LOCK:

        if jogador_id not in sala["jogadores"]:

            emit(
                "erro_sala",
                {
                    "mensagem": "Jogador inválido."
                }
            )

            return

        join_room(codigo)

        jogador = sala[
            "jogadores"
        ][jogador_id]

        jogador["sid"] = request.sid
        jogador["online"] = True

    emit(
        "jogadores_atualizados",
        {
            "jogadores":
                serializar_jogadores(codigo)
        },
        to=codigo
    )


# ============================================================
# INICIAR PARTIDA
# ============================================================

@socketio.on("iniciar_partida")
def iniciar_partida(dados):

    codigo = str(
        dados.get("codigo", "")
    ).strip()

    sala = buscar_sala(codigo)

    if not sala:

        emit(
            "erro_sala",
            {
                "mensagem": "Sala não encontrada."
            }
        )

        return

    jogador_id = obter_jogador_sessao()

    if not jogador_e_host(
        sala,
        jogador_id
    ):

        emit(
            "erro_sala",
            {
                "mensagem":
                    "Somente o criador da sala pode iniciar."
            }
        )

        return

    with LOCK:

        if sala["estado"] != "lobby":

            emit(
                "erro_sala",
                {
                    "mensagem":
                        "A partida já foi iniciada."
                }
            )

            return

        online = jogadores_online(sala)

        if len(online) < 1:

            emit(
                "erro_sala",
                {
                    "mensagem":
                        "Não existem jogadores conectados."
                }
            )

            return

        config = sala["configuracao"]

        try:

            quantidade = int(
                config.get(
                    "quantidade",
                    10
                )
            )

            tempo = int(
                config.get(
                    "tempo",
                    20
                )
            )

        except (TypeError, ValueError):

            quantidade = 10
            tempo = 20

        quantidade = max(
            1,
            min(50, quantidade)
        )

        tempo = max(
            5,
            min(120, tempo)
        )

        config["quantidade"] = quantidade
        config["tempo"] = tempo

        try:

            questoes = gerar_partida(
                config.get(
                    "assunto",
                    "misto"
                ),
                quantidade
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

        sala["questoes"] = questoes
        sala["estado"] = "jogando"
        sala["rodada"] = 0
        sala["questao_atual"] = None
        sala["inicio_questao"] = None
        sala["respostas_rodada"] = set()
        sala["ranking_rodada"] = []

        # Zera pontuação da partida.
        for jogador in sala[
            "jogadores"
        ].values():

            jogador["pontos"] = 0
            jogador["acertos"] = 0
            jogador["erros"] = 0
            jogador["sequencia"] = 0
            jogador["maior_sequencia"] = 0
            jogador["respondeu"] = False

    print(
        f"PARTIDA INICIADA | SALA {codigo} | "
        f"{len(online)} JOGADORES"
    )

    # Todos que fizeram join_room recebem.
    emit(
        "partida_iniciada",
        {
            "codigo": codigo
        },
        to=codigo
    )


# ============================================================
# PRÓXIMA QUESTÃO
# ============================================================

@socketio.on("proxima_questao")
def proxima_questao(dados):

    codigo = str(
        dados.get("codigo", "")
    ).strip()

    sala = buscar_sala(codigo)

    if not sala:
        return

    jogador_id = obter_jogador_sessao()

    if not jogador_e_host(
        sala,
        jogador_id
    ):
        return

    with LOCK:

        if sala["estado"] != "jogando":
            return

        # Evita criar outra questão enquanto uma
        # ainda está ativa.
        if sala.get("questao_atual"):
            return

        if (
            sala["rodada"]
            >=
            len(sala["questoes"])
        ):

            sala["estado"] = "finalizado"

            classificacao = ranking(
                codigo
            )

            emit(
                "partida_finalizada",
                {
                    "ranking":
                        classificacao
                },
                to=codigo
            )

            return

        questao = sala[
            "questoes"
        ][sala["rodada"]]

        sala[
            "questao_atual"
        ] = questao

        sala[
            "inicio_questao"
        ] = time.time()

        sala[
            "respostas_rodada"
        ] = set()

        sala[
            "ranking_rodada"
        ] = []

        for jogador in sala[
            "jogadores"
        ].values():

            jogador[
                "respondeu"
            ] = False

        numero_rodada = (
            sala["rodada"] + 1
        )

        total = len(
            sala["questoes"]
        )

        tempo = int(
            sala["configuracao"]["tempo"]
        )

    emit(
        "nova_questao",
        {
            "rodada": numero_rodada,
            "total": total,

            "pergunta":
                questao["pergunta"],

            "alternativas":
                questao["alternativas"],

            "tempo":
                tempo
        },
        to=codigo
    )


# ============================================================
# RESPONDER
# ============================================================

@socketio.on("responder")
def responder(dados):

    codigo = str(
        dados.get("codigo", "")
    ).strip()

    resposta = str(
        dados.get("resposta", "")
    ).strip()

    jogador_id = obter_jogador_sessao()

    sala = buscar_sala(codigo)

    if (
        not sala
        or
        sala["estado"] != "jogando"
    ):
        return

    with LOCK:

        if jogador_id not in sala[
            "jogadores"
        ]:
            return

        jogador = sala[
            "jogadores"
        ][jogador_id]

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

        questao = sala.get(
            "questao_atual"
        )

        if not questao:
            return

        inicio = sala.get(
            "inicio_questao"
        )

        if not inicio:
            return

        tempo_limite = int(
            sala["configuracao"]["tempo"]
        )

        decorrido = (
            time.time() - inicio
        )

        if decorrido > (
            tempo_limite + 1
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
                questao["correta"]
            )
            .strip()
            .casefold()
        )

        pontos = 0

        if acertou:

            jogador[
                "acertos"
            ] += 1

            jogador[
                "sequencia"
            ] += 1

            jogador[
                "maior_sequencia"
            ] = max(
                jogador[
                    "maior_sequencia"
                ],
                jogador[
                    "sequencia"
                ]
            )

            restante = max(
                0,
                tempo_limite
                -
                decorrido
            )

            bonus_tempo = round(
                (
                    restante
                    /
                    tempo_limite
                )
                *
                500
            )

            bonus_sequencia = min(
                jogador[
                    "sequencia"
                ]
                *
                25,
                200
            )

            pontos = (
                500
                +
                bonus_tempo
                +
                bonus_sequencia
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

        # ---------------------------------------------
        # SOMENTE JOGADORES ONLINE CONTAM
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
            len(online_ids) > 0
            and
            len(responderam_online)
            >=
            len(online_ids)
        )

    # Resposta somente para quem respondeu.
    emit(
        "resposta_recebida",
        {
            "correto":
                acertou,

            "pontos":
                pontos
        }
    )

    if todos_responderam:

        encerrar_rodada(
            codigo
        )


# ============================================================
# TEMPO ESGOTADO
# ============================================================

@socketio.on("tempo_esgotado")
def tempo_esgotado(dados):

    codigo = str(
        dados.get("codigo", "")
    ).strip()

    sala = buscar_sala(codigo)

    if not sala:
        return

    jogador_id = obter_jogador_sessao()

    if not jogador_e_host(
        sala,
        jogador_id
    ):
        return

    encerrar_rodada(
        codigo
    )


# ============================================================
# ENCERRAR RODADA
# ============================================================

def encerrar_rodada(codigo):

    sala = buscar_sala(
        codigo
    )

    if not sala:
        return

    with LOCK:

        if sala[
            "estado"
        ] != "jogando":
            return

        questao = sala.get(
            "questao_atual"
        )

        # Evita encerrar duas vezes.
        if not questao:
            return

        correta = questao[
            "correta"
        ]

        # IMPORTANTE:
        # limpa antes de emitir para impedir
        # duplo encerramento.
        sala[
            "questao_atual"
        ] = None

        sala[
            "inicio_questao"
        ] = None

        sala[
            "rodada"
        ] += 1

        classificacao = ranking(
            codigo
        )

        terminou = (
            sala["rodada"]
            >=
            len(sala["questoes"])
        )

        if terminou:
            sala["estado"] = "finalizado"

    emit(
        "rodada_finalizada",
        {
            "correta":
                correta,

            "ranking":
                classificacao,

            "terminou":
                terminou
        },
        to=codigo
    )

    if terminou:

        emit(
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

@socketio.on("pedir_ranking")
def pedir_ranking(dados):

    codigo = str(
        dados.get("codigo", "")
    ).strip()

    sala = buscar_sala(
        codigo
    )

    if not sala:
        return

    emit(
        "ranking_final",
        {
            "ranking":
                ranking(codigo)
        }
    )


# ============================================================
# DESCONECTOU
# ============================================================

@socketio.on("disconnect")
def desconectou():

    sid = request.sid

    salas_afetadas = []

    with LOCK:

        for codigo, sala in list(
            SALAS.items()
        ):

            for jogador in sala[
                "jogadores"
            ].values():

                if jogador.get(
                    "sid"
                ) == sid:

                    jogador[
                        "online"
                    ] = False

                    jogador[
                        "sid"
                    ] = None

                    salas_afetadas.append(
                        codigo
                    )

                    break

    # Emit fora do LOCK.
    for codigo in salas_afetadas:

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

        sala = buscar_sala(
            codigo
        )

        if (
            sala
            and
            sala["estado"] == "jogando"
            and
            sala.get("questao_atual")
        ):

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
                    len(online_ids) > 0
                    and
                    len(responderam)
                    >=
                    len(online_ids)
                )

            if todos_responderam:

                encerrar_rodada(
                    codigo
                )