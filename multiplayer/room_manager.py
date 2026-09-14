import random
import time
import threading


SALAS = {}

LOCK = threading.RLock()


def gerar_codigo():

    with LOCK:

        while True:

            codigo = str(
                random.randint(
                    100000,
                    999999
                )
            )

            if codigo not in SALAS:
                return codigo


def criar_sala(
    host_id,
    host_nome,
    configuracao
):

    codigo = gerar_codigo()

    with LOCK:

        SALAS[codigo] = {

            "codigo": codigo,

            "host_id": str(host_id),

            "host_nome": host_nome,

            "estado": "lobby",

            "configuracao": configuracao,

            "jogadores": {},

            "rodada": 0,

            "questoes": [],

            "questao_atual": None,

            "inicio_questao": None,

            "respostas_rodada": set(),

            "ranking_rodada": [],

            "criada_em": time.time()
        }

    return SALAS[codigo]


def buscar_sala(codigo):

    with LOCK:
        return SALAS.get(
            str(codigo)
        )


def adicionar_jogador(
    codigo,
    jogador_id,
    nome,
    sid=None
):

    with LOCK:

        sala = SALAS.get(
            str(codigo)
        )

        if not sala:
            return None

        jogador_id = str(
            jogador_id
        )

        sala["jogadores"][
            jogador_id
        ] = {

            "id": jogador_id,

            "nome": nome,

            "sid": sid,

            "pontos": 0,

            "acertos": 0,

            "erros": 0,

            "sequencia": 0,

            "maior_sequencia": 0,

            "respondeu": False,

            "online": True
        }

        return sala["jogadores"][
            jogador_id
        ]


def remover_jogador(
    codigo,
    jogador_id
):

    with LOCK:

        sala = SALAS.get(
            str(codigo)
        )

        if not sala:
            return

        sala["jogadores"].pop(
            str(jogador_id),
            None
        )


def ranking(codigo):

    with LOCK:

        sala = SALAS.get(
            str(codigo)
        )

        if not sala:
            return []

        jogadores = list(
            sala["jogadores"].values()
        )

        jogadores.sort(
            key=lambda j: (
                j["pontos"],
                j["acertos"]
            ),
            reverse=True
        )

        return [
            {
                "posicao": indice + 1,
                "id": jogador["id"],
                "nome": jogador["nome"],
                "pontos": jogador["pontos"],
                "acertos": jogador["acertos"],
                "erros": jogador["erros"],
                "sequencia": jogador["sequencia"]
            }

            for indice, jogador
            in enumerate(jogadores)
        ]


def serializar_jogadores(
    codigo
):

    with LOCK:

        sala = SALAS.get(
            str(codigo)
        )

        if not sala:
            return []

        return [
            {
                "id": jogador["id"],
                "nome": jogador["nome"],
                "pontos": jogador["pontos"],
                "online": jogador["online"]
            }

            for jogador
            in sala["jogadores"].values()
        ]


def apagar_sala(codigo):

    with LOCK:

        SALAS.pop(
            str(codigo),
            None
        )