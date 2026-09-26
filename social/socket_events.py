from datetime import datetime

from flask import request, url_for
from flask_login import current_user

from models import (
    db,
    Usuario,
)

from multiplayer import socketio

from .models import PerfilUsuario

from .presence import (
    registrar_presenca,
    sids_do_usuario,
    status_varios,
)

from .routes import sao_amigos


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


    try:

        alvo_id = int(

            (dados or {})

            .get(
                "usuario_id"
            )

        )

    except (
        TypeError,
        ValueError
    ):

        return


    if (
        alvo_id
        ==
        current_user.id
    ):

        return


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
    # USUÁRIO ONLINE?
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
    # DADOS DO DESAFIO
    # ========================================================

    payload = {

        "desafiante_id":
            current_user.id,

        "nome":
            current_user.nome,

        "username":
            current_user.username,

        "url_multiplayer":
            url_for(
                "multiplayer.inicio"
            )

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
    # CONFIRMAR PARA QUEM ENVIOU
    # ========================================================

    socketio.emit(

        "social_desafio_resultado",

        {
            "ok":
                True,

            "mensagem":
                f"Desafio enviado para {alvo.nome}! 🎮"
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


    try:

        desafiante_id = int(

            (dados or {})

            .get(
                "desafiante_id"
            )

        )

    except (
        TypeError,
        ValueError
    ):

        return


    if not sao_amigos(

        current_user.id,

        desafiante_id

    ):

        return


    sids = sids_do_usuario(
        desafiante_id
    )


    payload = {

        "nome":
            current_user.nome,

        "username":
            current_user.username,

        "url_multiplayer":
            url_for(
                "multiplayer.inicio"
            )

    }


    for sid in sids:

        socketio.emit(

            "social_desafio_aceito",

            payload,

            to=
                sid

        )