import random
import time
import threading


# =========================================================
# SALAS EM MEMÓRIA
# =========================================================

SALAS = {}

LOCK = threading.RLock()


# Tempo máximo de uma sala abandonada:
# 6 horas
TEMPO_EXPIRACAO_SALA = 6 * 60 * 60


# =========================================================
# UTILITÁRIOS
# =========================================================

def normalizar_codigo(codigo):

    return str(
        codigo or ""
    ).strip()


def normalizar_id(jogador_id):

    return str(
        jogador_id or ""
    ).strip()


# =========================================================
# GERAR CÓDIGO
# =========================================================

def gerar_codigo():
    """
    Gera um código numérico de 6 dígitos
    que ainda não está sendo usado.
    """

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


# =========================================================
# CRIAR SALA
# =========================================================

def criar_sala(
    host_id,
    host_nome,
    configuracao
):

    host_id = normalizar_id(
        host_id
    )

    host_nome = str(
        host_nome or "Anfitrião"
    ).strip()

    if not host_nome:
        host_nome = "Anfitrião"


    with LOCK:

        # O código é gerado enquanto o LOCK
        # continua ativo, evitando colisões.
        while True:

            codigo = str(
                random.randint(
                    100000,
                    999999
                )
            )

            if codigo not in SALAS:
                break


        sala = {

            "codigo":
                codigo,

            "host_id":
                host_id,

            "host_nome":
                host_nome,

            "estado":
                "lobby",

            "configuracao":
                dict(
                    configuracao or {}
                ),

            "jogadores":
                {},

            "rodada":
                0,

            "questoes":
                [],

            "questao_atual":
                None,

            "inicio_questao":
                None,

            "respostas_rodada":
                set(),

            "ranking_rodada":
                [],

            "criada_em":
                time.time(),

            "ultima_atividade":
                time.time()

        }


        # Adiciona o host como primeiro jogador.
        sala["jogadores"][
            host_id
        ] = {

            "id":
                host_id,

            "nome":
                host_nome,

            "sid":
                None,

            "pontos":
                0,

            "acertos":
                0,

            "erros":
                0,

            "sequencia":
                0,

            "maior_sequencia":
                0,

            "respondeu":
                False,

            "online":
                True,

            "entrou_em":
                time.time()

        }


        SALAS[
            codigo
        ] = sala


        return sala


# =========================================================
# BUSCAR SALA
# =========================================================

def buscar_sala(
    codigo
):

    codigo = normalizar_codigo(
        codigo
    )

    with LOCK:

        return SALAS.get(
            codigo
        )


# =========================================================
# SALA EXISTE
# =========================================================

def sala_existe(
    codigo
):

    codigo = normalizar_codigo(
        codigo
    )

    with LOCK:

        return (
            codigo
            in SALAS
        )


# =========================================================
# ADICIONAR JOGADOR
# =========================================================

def adicionar_jogador(
    codigo,
    jogador_id,
    nome,
    sid=None
):

    codigo = normalizar_codigo(
        codigo
    )

    jogador_id = normalizar_id(
        jogador_id
    )

    nome = str(
        nome or "Jogador"
    ).strip()

    if not nome:
        nome = "Jogador"


    with LOCK:

        sala = SALAS.get(
            codigo
        )

        if not sala:
            return None


        # Não permite entrada de novo jogador
        # caso a partida já tenha terminado.
        if (
            sala.get("estado")
            ==
            "finalizada"
            and
            jogador_id
            not in sala["jogadores"]
        ):

            return None


        jogador_existente = (
            sala["jogadores"].get(
                jogador_id
            )
        )


        # =====================================
        # RECONEXÃO
        # =====================================

        if jogador_existente:

            jogador_existente[
                "nome"
            ] = nome

            jogador_existente[
                "sid"
            ] = sid

            jogador_existente[
                "online"
            ] = True

            sala[
                "ultima_atividade"
            ] = time.time()

            return jogador_existente


        # =====================================
        # NOVO JOGADOR
        # =====================================

        jogador = {

            "id":
                jogador_id,

            "nome":
                nome,

            "sid":
                sid,

            "pontos":
                0,

            "acertos":
                0,

            "erros":
                0,

            "sequencia":
                0,

            "maior_sequencia":
                0,

            "respondeu":
                False,

            "online":
                True,

            "entrou_em":
                time.time()

        }


        sala["jogadores"][
            jogador_id
        ] = jogador


        sala[
            "ultima_atividade"
        ] = time.time()


        return jogador


# =========================================================
# ATUALIZAR SID
# =========================================================

def atualizar_sid(
    codigo,
    jogador_id,
    sid
):

    codigo = normalizar_codigo(
        codigo
    )

    jogador_id = normalizar_id(
        jogador_id
    )


    with LOCK:

        sala = SALAS.get(
            codigo
        )

        if not sala:
            return None


        jogador = (
            sala["jogadores"].get(
                jogador_id
            )
        )

        if not jogador:
            return None


        jogador[
            "sid"
        ] = sid

        jogador[
            "online"
        ] = True


        sala[
            "ultima_atividade"
        ] = time.time()


        return jogador


# =========================================================
# BUSCAR JOGADOR
# =========================================================

def buscar_jogador(
    codigo,
    jogador_id
):

    codigo = normalizar_codigo(
        codigo
    )

    jogador_id = normalizar_id(
        jogador_id
    )


    with LOCK:

        sala = SALAS.get(
            codigo
        )

        if not sala:
            return None


        return (
            sala[
                "jogadores"
            ].get(
                jogador_id
            )
        )


# =========================================================
# BUSCAR JOGADOR PELO SID
# =========================================================

def buscar_jogador_por_sid(
    sid
):

    if not sid:
        return None, None


    with LOCK:

        for codigo, sala in SALAS.items():

            for jogador in (
                sala[
                    "jogadores"
                ].values()
            ):

                if (
                    jogador.get("sid")
                    ==
                    sid
                ):

                    return (
                        codigo,
                        jogador
                    )


    return (
        None,
        None
    )


# =========================================================
# MARCAR JOGADOR OFFLINE
# =========================================================

def marcar_jogador_offline(
    codigo,
    jogador_id
):

    codigo = normalizar_codigo(
        codigo
    )

    jogador_id = normalizar_id(
        jogador_id
    )


    with LOCK:

        sala = SALAS.get(
            codigo
        )

        if not sala:
            return None


        jogador = (
            sala["jogadores"].get(
                jogador_id
            )
        )

        if not jogador:
            return None


        jogador[
            "online"
        ] = False

        jogador[
            "sid"
        ] = None


        sala[
            "ultima_atividade"
        ] = time.time()


        return jogador


# =========================================================
# MARCAR OFFLINE PELO SID
# =========================================================

def marcar_offline_por_sid(
    sid
):

    with LOCK:

        for codigo, sala in SALAS.items():

            for jogador in (
                sala[
                    "jogadores"
                ].values()
            ):

                if (
                    jogador.get("sid")
                    ==
                    sid
                ):

                    jogador[
                        "online"
                    ] = False

                    jogador[
                        "sid"
                    ] = None


                    sala[
                        "ultima_atividade"
                    ] = time.time()


                    return (
                        codigo,
                        jogador
                    )


    return (
        None,
        None
    )


# =========================================================
# REMOVER JOGADOR
# =========================================================

def remover_jogador(
    codigo,
    jogador_id
):

    codigo = normalizar_codigo(
        codigo
    )

    jogador_id = normalizar_id(
        jogador_id
    )


    with LOCK:

        sala = SALAS.get(
            codigo
        )

        if not sala:
            return None


        jogador = (
            sala[
                "jogadores"
            ].pop(
                jogador_id,
                None
            )
        )


        sala[
            "ultima_atividade"
        ] = time.time()


        return jogador


# =========================================================
# JOGADOR É HOST?
# =========================================================

def jogador_e_host(
    codigo,
    jogador_id
):

    codigo = normalizar_codigo(
        codigo
    )

    jogador_id = normalizar_id(
        jogador_id
    )


    with LOCK:

        sala = SALAS.get(
            codigo
        )

        if not sala:
            return False


        return (
            str(
                sala.get(
                    "host_id"
                )
            )
            ==
            jogador_id
        )


# =========================================================
# QUANTIDADE DE JOGADORES
# =========================================================

def quantidade_jogadores(
    codigo,
    somente_online=False
):

    codigo = normalizar_codigo(
        codigo
    )


    with LOCK:

        sala = SALAS.get(
            codigo
        )

        if not sala:
            return 0


        if not somente_online:

            return len(
                sala[
                    "jogadores"
                ]
            )


        return sum(

            1

            for jogador
            in sala[
                "jogadores"
            ].values()

            if jogador.get(
                "online"
            )

        )


# =========================================================
# SERIALIZAR JOGADORES
# =========================================================

def serializar_jogadores(
    codigo
):

    codigo = normalizar_codigo(
        codigo
    )


    with LOCK:

        sala = SALAS.get(
            codigo
        )

        if not sala:
            return []


        jogadores = []


        for jogador in (
            sala[
                "jogadores"
            ].values()
        ):

            jogadores.append({

                "id":
                    jogador["id"],

                "nome":
                    jogador["nome"],

                "pontos":
                    jogador["pontos"],

                "acertos":
                    jogador["acertos"],

                "online":
                    jogador["online"],

                "host":
                    (
                        jogador["id"]
                        ==
                        sala["host_id"]
                    )

            })


        return jogadores


# =========================================================
# RANKING
# =========================================================

def ranking(
    codigo
):

    codigo = normalizar_codigo(
        codigo
    )


    with LOCK:

        sala = SALAS.get(
            codigo
        )

        if not sala:
            return []


        jogadores = list(
            sala[
                "jogadores"
            ].values()
        )


        jogadores.sort(

            key=lambda jogador: (

                jogador.get(
                    "pontos",
                    0
                ),

                jogador.get(
                    "acertos",
                    0
                ),

                jogador.get(
                    "maior_sequencia",
                    0
                )

            ),

            reverse=True

        )


        resultado = []


        for indice, jogador in enumerate(
            jogadores,
            start=1
        ):

            resultado.append({

                "posicao":
                    indice,

                "id":
                    jogador["id"],

                "nome":
                    jogador["nome"],

                "pontos":
                    jogador.get(
                        "pontos",
                        0
                    ),

                "acertos":
                    jogador.get(
                        "acertos",
                        0
                    ),

                "erros":
                    jogador.get(
                        "erros",
                        0
                    ),

                "sequencia":
                    jogador.get(
                        "sequencia",
                        0
                    ),

                "maior_sequencia":
                    jogador.get(
                        "maior_sequencia",
                        0
                    ),

                "online":
                    jogador.get(
                        "online",
                        False
                    )

            })


        return resultado


# =========================================================
# RESETAR RESPOSTAS DA RODADA
# =========================================================

def resetar_respostas_rodada(
    codigo
):

    codigo = normalizar_codigo(
        codigo
    )


    with LOCK:

        sala = SALAS.get(
            codigo
        )

        if not sala:
            return False


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


        sala[
            "ultima_atividade"
        ] = time.time()


        return True


# =========================================================
# ALTERAR ESTADO
# =========================================================

def alterar_estado(
    codigo,
    estado
):

    codigo = normalizar_codigo(
        codigo
    )


    with LOCK:

        sala = SALAS.get(
            codigo
        )

        if not sala:
            return False


        sala[
            "estado"
        ] = str(
            estado
        )


        sala[
            "ultima_atividade"
        ] = time.time()


        return True


# =========================================================
# APAGAR SALA
# =========================================================

def apagar_sala(
    codigo
):

    codigo = normalizar_codigo(
        codigo
    )


    with LOCK:

        return SALAS.pop(
            codigo,
            None
        )


# =========================================================
# LIMPAR SALAS ANTIGAS
# =========================================================

def limpar_salas_expiradas():
    """
    Remove salas abandonadas há várias horas.
    """

    agora = time.time()

    removidas = []


    with LOCK:

        for codigo, sala in list(
            SALAS.items()
        ):

            ultima_atividade = (
                sala.get(
                    "ultima_atividade"
                )
                or
                sala.get(
                    "criada_em",
                    agora
                )
            )


            if (
                agora
                -
                ultima_atividade
                >
                TEMPO_EXPIRACAO_SALA
            ):

                SALAS.pop(
                    codigo,
                    None
                )

                removidas.append(
                    codigo
                )


    return removidas