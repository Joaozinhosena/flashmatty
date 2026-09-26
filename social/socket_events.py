import threading
import time

from datetime import datetime

from flask import (
    request,
    url_for
)

from flask_login import (
    current_user
)

from models import (
    db,
    Usuario
)

from multiplayer import socketio

from multiplayer.room_manager import (
    criar_sala,
    adicionar_jogador
)

from .models import (
    PerfilUsuario
)

from .presence import (
    registrar_presenca,
    sids_do_usuario,
    status_varios
)

from .routes import (
    sao_amigos
)

from notificacoes.push import (
    enviar_push_usuario
)


# ============================================================
# DESAFIOS PENDENTES
# ============================================================
#
# Como o seu multiplayer também funciona em memória,
# os desafios pendentes seguem a mesma lógica.
#
# Chave:
# (desafiante_id, desafiado_id)
#
# ============================================================

DESAFIOS_PENDENTES = {}

DESAFIOS_LOCK = threading.RLock()

TEMPO_MAXIMO_DESAFIO = 120


# ============================================================
# LIMPAR DESAFIOS EXPIRADOS
# ============================================================

def limpar_desafios_expirados():

    agora = time.time()

    with DESAFIOS_LOCK:

        expirados = [

            chave

            for chave, desafio
            in DESAFIOS_PENDENTES.items()

            if (
                agora
                -
                desafio.get(
                    "criado_em",
                    agora
                )
                >
                TEMPO_MAXIMO_DESAFIO
            )

        ]


        for chave in expirados:

            DESAFIOS_PENDENTES.pop(
                chave,
                None
            )


# ============================================================
# REGISTRAR DESAFIO
# ============================================================

def registrar_desafio(
    desafiante_id,
    desafiado_id,
    configuracao=None
):

    limpar_desafios_expirados()


    chave = (

        int(
            desafiante_id
        ),

        int(
            desafiado_id
        )

    )


    configuracao_padrao = {

        "assunto":
            "misto",

        "quantidade":
            10,

        "tempo":
            20,

        "modo":
            "classico",

        "origem":
            "desafio_amigo"

    }


    if configuracao:

        configuracao_padrao.update(
            configuracao
        )


    with DESAFIOS_LOCK:

        DESAFIOS_PENDENTES[
            chave
        ] = {

            "criado_em":
                time.time(),

            "configuracao":
                configuracao_padrao

        }


# ============================================================
# CONSUMIR DESAFIO
# ============================================================

def consumir_desafio(
    desafiante_id,
    desafiado_id
):

    limpar_desafios_expirados()


    chave = (

        int(
            desafiante_id
        ),

        int(
            desafiado_id
        )

    )


    with DESAFIOS_LOCK:

        return DESAFIOS_PENDENTES.pop(
            chave,
            None
        )


# ============================================================
# ÚLTIMO ACESSO
# ============================================================

def atualizar_ultimo_acesso(
    usuario_id
):

    perfil = PerfilUsuario.obter(
        usuario_id,
        criar=True
    )


    agora = datetime.utcnow()


    if (

        not perfil.ultimo_acesso

        or

        (
            agora
            -
            perfil.ultimo_acesso
        ).total_seconds()
        >=
        60

    ):

        perfil.ultimo_acesso = (
            agora
        )


        db.session.commit()


# ============================================================
# PRESENÇA
# ============================================================

@socketio.on(
    "social_presenca"
)
def social_presenca():

    if (
        not current_user.is_authenticated
    ):

        return


    ficou_online = registrar_presenca(

        current_user.id,

        request.sid

    )


    atualizar_ultimo_acesso(
        current_user.id
    )


    if ficou_online:

        socketio.emit(

            "social_status",

            {

                "usuario_id":
                    current_user.id,

                "online":
                    True

            }

        )


# ============================================================
# CONSULTAR PRESENÇA
# ============================================================

@socketio.on(
    "social_consultar_presenca"
)
def social_consultar_presenca(
    dados
):

    if (
        not current_user.is_authenticated
    ):

        return


    ids = (

        (dados or {})

        .get(
            "usuarios",
            []
        )

    )


    resultado = status_varios(
        ids
    )


    socketio.emit(

        "social_presenca_resultado",

        resultado,

        to=
            request.sid

    )


# ============================================================
# DESAFIAR AMIGO
# ============================================================

@socketio.on(
    "social_desafiar"
)
def social_desafiar(
    dados
):

    if (
        not current_user.is_authenticated
    ):

        return


    dados = (
        dados
        or
        {}
    )


    # ========================================================
    # ID DO AMIGO
    # ========================================================

    try:

        alvo_id = int(

            dados.get(
                "usuario_id"
            )

        )

    except (
        TypeError,
        ValueError
    ):

        socketio.emit(

            "social_desafio_resultado",

            {

                "ok":
                    False,

                "mensagem":
                    "Usuário inválido."

            },

            to=
                request.sid

        )

        return


    # ========================================================
    # NÃO PODE DESAFIAR A SI MESMO
    # ========================================================

    if (
        alvo_id
        ==
        current_user.id
    ):

        socketio.emit(

            "social_desafio_resultado",

            {

                "ok":
                    False,

                "mensagem":
                    "Você não pode desafiar a si mesmo."

            },

            to=
                request.sid

        )

        return


    # ========================================================
    # BUSCAR USUÁRIO
    # ========================================================

    alvo = db.session.get(
        Usuario,
        alvo_id
    )


    if not alvo:

        socketio.emit(

            "social_desafio_resultado",

            {

                "ok":
                    False,

                "mensagem":
                    "Usuário não encontrado."

            },

            to=
                request.sid

        )

        return


    # ========================================================
    # PRECISA SER AMIGO
    # ========================================================

    if not sao_amigos(

        current_user.id,

        alvo.id

    ):

        socketio.emit(

            "social_desafio_resultado",

            {

                "ok":
                    False,

                "mensagem":
                    "Só é possível desafiar amigos."

            },

            to=
                request.sid

        )

        return


    # ========================================================
    # USUÁRIO PRECISA ESTAR ONLINE
    # ========================================================

    sids = sids_do_usuario(
        alvo.id
    )


    if not sids:

        socketio.emit(

            "social_desafio_resultado",

            {

                "ok":
                    False,

                "mensagem":
                    f"{alvo.nome} está offline."

            },

            to=
                request.sid

        )

        return


    # ========================================================
    # CONFIGURAÇÃO DA FUTURA PARTIDA
    # ========================================================

    try:

        quantidade = int(
            dados.get(
                "quantidade",
                10
            )
        )

    except (
        TypeError,
        ValueError
    ):

        quantidade = 10


    quantidade = max(
        1,
        min(
            50,
            quantidade
        )
    )


    try:

        tempo = int(
            dados.get(
                "tempo",
                20
            )
        )

    except (
        TypeError,
        ValueError
    ):

        tempo = 20


    tempo = max(
        5,
        min(
            120,
            tempo
        )
    )


    assunto = str(

        dados.get(
            "assunto",
            "misto"
        )

        or
        "misto"

    ).strip()


    modo = str(

        dados.get(
            "modo",
            "classico"
        )

        or
        "classico"

    ).strip()


    configuracao = {

        "assunto":
            assunto,

        "quantidade":
            quantidade,

        "tempo":
            tempo,

        "modo":
            modo,

        "origem":
            "desafio_amigo"

    }


    # ========================================================
    # REGISTRAR DESAFIO PENDENTE
    # ========================================================

    registrar_desafio(

        current_user.id,

        alvo.id,

        configuracao

    )


    # ========================================================
    # DADOS ENVIADOS AO AMIGO
    # ========================================================

    payload = {

        "desafiante_id":
            current_user.id,

        "nome":
            current_user.nome,

        "username":
            current_user.username,

        "expira_em":
            TEMPO_MAXIMO_DESAFIO

    }


    # ========================================================
    # ENVIAR PARA TODAS AS ABAS DO AMIGO
    # ========================================================

    for sid in sids:

        socketio.emit(

            "social_desafio_recebido",

            payload,

            to=
                sid

        )


    # ========================================================
    # NOTIFICAÇÃO PUSH
    # ========================================================

    try:

        enviar_push_usuario(

            alvo.id,

            "🎮 Novo desafio",

            (
                f"{current_user.nome} "
                "desafiou você no FlashMatty!"
            ),

            url=
                url_for(
                    "social.amigos"
                ),

            categoria=
                "desafios",

            tag=
                (
                    "desafio-"
                    +
                    str(
                        current_user.id
                    )
                )

        )

    except Exception as erro:

        print(
            "Erro ao enviar Push do desafio:",
            erro
        )


    # ========================================================
    # CONFIRMAR PARA QUEM ENVIOU
    # ========================================================

    socketio.emit(

        "social_desafio_resultado",

        {

            "ok":
                True,

            "mensagem":
                (
                    f"Desafio enviado "
                    f"para {alvo.nome}! 🎮"
                )

        },

        to=
            request.sid

    )


# ============================================================
# DESAFIO ACEITO
# ============================================================

@socketio.on(
    "social_desafio_aceito"
)
def social_desafio_aceito(
    dados
):

    if (
        not current_user.is_authenticated
    ):

        return


    dados = (
        dados
        or
        {}
    )


    # ========================================================
    # ID DO DESAFIANTE
    # ========================================================

    try:

        desafiante_id = int(

            dados.get(
                "desafiante_id"
            )

        )

    except (
        TypeError,
        ValueError
    ):

        socketio.emit(

            "social_desafio_resultado",

            {

                "ok":
                    False,

                "mensagem":
                    "Desafio inválido."

            },

            to=
                request.sid

        )

        return


    if (
        desafiante_id
        ==
        current_user.id
    ):

        return


    # ========================================================
    # VERIFICAR SE O DESAFIANTE EXISTE
    # ========================================================

    desafiante = db.session.get(
        Usuario,
        desafiante_id
    )


    if not desafiante:

        socketio.emit(

            "social_desafio_resultado",

            {

                "ok":
                    False,

                "mensagem":
                    "O desafiante não foi encontrado."

            },

            to=
                request.sid

        )

        return


    # ========================================================
    # PRECISAM CONTINUAR SENDO AMIGOS
    # ========================================================

    if not sao_amigos(

        current_user.id,

        desafiante.id

    ):

        socketio.emit(

            "social_desafio_resultado",

            {

                "ok":
                    False,

                "mensagem":
                    "Esse desafio não é mais válido."

            },

            to=
                request.sid

        )

        return


    # ========================================================
    # VERIFICAR DESAFIO PENDENTE
    # ========================================================

    desafio = consumir_desafio(

        desafiante.id,

        current_user.id

    )


    if not desafio:

        socketio.emit(

            "social_desafio_resultado",

            {

                "ok":
                    False,

                "mensagem":
                    (
                        "Esse desafio expirou "
                        "ou já foi aceito."
                    )

            },

            to=
                request.sid

        )

        return


    configuracao = desafio.get(

        "configuracao",

        {}

    )


    # ========================================================
    # CRIAR SALA
    #
    # QUEM ENVIOU O DESAFIO SERÁ O HOST
    # ========================================================

    try:

        sala = criar_sala(

            str(
                desafiante.id
            ),

            desafiante.nome,

            configuracao

        )


        codigo = str(
            sala[
                "codigo"
            ]
        )


        # ====================================================
        # ADICIONAR AUTOMATICAMENTE QUEM ACEITOU
        # ====================================================

        jogador = adicionar_jogador(

            codigo,

            str(
                current_user.id
            ),

            current_user.nome

        )


        if not jogador:

            raise RuntimeError(
                "Não foi possível adicionar o jogador."
            )


        # ====================================================
        # ATUALIZAR ESTADO REAL DO HOST
        # ====================================================

        host_online = bool(
            sids_do_usuario(
                desafiante.id
            )
        )


        host_id = str(
            desafiante.id
        )


        if (
            host_id
            in
            sala[
                "jogadores"
            ]
        ):

            sala[
                "jogadores"
            ][
                host_id
            ][
                "online"
            ] = host_online


    except Exception as erro:

        print(
            "ERRO AO CRIAR SALA DO DESAFIO:",
            erro
        )


        # Recoloca o desafio para permitir
        # uma nova tentativa.

        registrar_desafio(

            desafiante.id,

            current_user.id,

            configuracao

        )


        socketio.emit(

            "social_desafio_resultado",

            {

                "ok":
                    False,

                "mensagem":
                    (
                        "Não foi possível criar "
                        "a sala do desafio."
                    )

            },

            to=
                request.sid

        )

        return


    # ========================================================
    # URL DA SALA
    #
    # Esta rota será criada no multiplayer/routes.py
    # ========================================================

    url_sala = (
        "/multiplayer/desafio/"
        +
        codigo
    )


    # ========================================================
    # PAYLOAD PARA OS DOIS JOGADORES
    # ========================================================

    payload = {

        "ok":
            True,

        "codigo":
            codigo,

        "host_id":
            str(
                desafiante.id
            ),

        "desafiante_id":
            desafiante.id,

        "desafiado_id":
            current_user.id,

        "nome":
            current_user.nome,

        "username":
            current_user.username,

        "url_multiplayer":
            url_sala,

        "mensagem":
            (
                f"{current_user.nome} "
                "aceitou o desafio! 🎮"
            )

    }


    # ========================================================
    # ENVIAR PARA O DESAFIANTE
    # ========================================================

    sids_desafiante = sids_do_usuario(
        desafiante.id
    )


    for sid in sids_desafiante:

        socketio.emit(

            "social_desafio_aceito",

            payload,

            to=
                sid

        )


    # ========================================================
    # ENVIAR TAMBÉM PARA QUEM ACEITOU
    #
    # Assim os DOIS são redirecionados para a mesma sala.
    # ========================================================

    socketio.emit(

        "social_desafio_aceito",

        payload,

        to=
            request.sid

    )


    # ========================================================
    # CASO O DESAFIANTE TENHA SAÍDO DO SITE
    # ========================================================

    if not sids_desafiante:

        try:

            enviar_push_usuario(

                desafiante.id,

                "🎮 Desafio aceito",

                (
                    f"{current_user.nome} "
                    "aceitou seu desafio!"
                ),

                url=
                    url_sala,

                categoria=
                    "desafios",

                tag=
                    (
                        "desafio-aceito-"
                        +
                        codigo
                    )

            )

        except Exception as erro:

            print(
                "Erro ao enviar Push de desafio aceito:",
                erro
            )


    print(
        "SALA DE DESAFIO CRIADA:",
        codigo,
        "| HOST:",
        desafiante.nome,
        "| DESAFIADO:",
        current_user.nome
    )