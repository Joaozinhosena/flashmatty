import uuid

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from flask_login import (
    login_required,
    current_user
)

from curriculum import CURRICULO

from multiplayer.room_manager import (
    criar_sala,
    buscar_sala,
    adicionar_jogador
)


multiplayer_bp = Blueprint(
    "multiplayer",
    __name__,
    url_prefix="/multiplayer"
)


# ============================================================
# INÍCIO
# ============================================================

@multiplayer_bp.route("/")
@login_required
def inicio():

    return render_template(
        "multiplayer/inicio.html"
    )


# ============================================================
# CRIAR SALA
# ============================================================

@multiplayer_bp.route(
    "/criar",
    methods=["GET", "POST"]
)
@login_required
def criar():

    if request.method == "POST":

        assunto = request.form.get(
            "assunto",
            "misto"
        )

        quantidade = request.form.get(
            "quantidade",
            "10"
        )

        tempo = request.form.get(
            "tempo",
            "20"
        )

        try:

            quantidade = int(
                quantidade
            )

            tempo = int(
                tempo
            )

        except ValueError:

            quantidade = 10
            tempo = 20

        quantidade = max(
            5,
            min(
                quantidade,
                30
            )
        )

        tempo = max(
            5,
            min(
                tempo,
                60
            )
        )

        sala = criar_sala(

            current_user.id,

            current_user.nome,

            {
                "assunto": assunto,
                "quantidade": quantidade,
                "tempo": tempo
            }
        )

        # Host também participa
        adicionar_jogador(

            sala["codigo"],

            str(
                current_user.id
            ),

            current_user.nome
        )

        session[
            "multiplayer_codigo"
        ] = sala["codigo"]

        session[
            "multiplayer_jogador"
        ] = str(
            current_user.id
        )

        session[
            "multiplayer_host"
        ] = True

        return redirect(
            url_for(
                "multiplayer.lobby",
                codigo=sala["codigo"]
            )
        )

    return render_template(
        "multiplayer/criar.html",
        curriculo=CURRICULO
    )


# ============================================================
# ENTRAR
# ============================================================

@multiplayer_bp.route(
    "/entrar",
    methods=["GET", "POST"]
)
@login_required
def entrar():

    if request.method == "POST":

        codigo = request.form.get(
            "codigo",
            ""
        ).strip()

        apelido = request.form.get(
            "apelido",
            ""
        ).strip()

        sala = buscar_sala(
            codigo
        )

        if not sala:

            flash(
                "Sala não encontrada."
            )

            return redirect(
                url_for(
                    "multiplayer.entrar"
                )
            )

        if sala["estado"] != "lobby":

            flash(
                "A partida já começou."
            )

            return redirect(
                url_for(
                    "multiplayer.entrar"
                )
            )

        if not apelido:

            apelido = (
                current_user.nome
            )

        jogador_id = (
            f"{current_user.id}-"
            f"{uuid.uuid4().hex[:6]}"
        )

        adicionar_jogador(
            codigo,
            jogador_id,
            apelido
        )

        session[
            "multiplayer_codigo"
        ] = codigo

        session[
            "multiplayer_jogador"
        ] = jogador_id

        session[
            "multiplayer_host"
        ] = False

        return redirect(
            url_for(
                "multiplayer.lobby",
                codigo=codigo
            )
        )

    return render_template(
        "multiplayer/entrar.html"
    )


# ============================================================
# LOBBY
# ============================================================

@multiplayer_bp.route(
    "/sala/<codigo>"
)
@login_required
def lobby(codigo):

    sala = buscar_sala(
        codigo
    )

    if not sala:

        flash(
            "Sala não encontrada."
        )

        return redirect(
            url_for(
                "multiplayer.inicio"
            )
        )

    jogador_id = session.get(
        "multiplayer_jogador"
    )

    if (
        not jogador_id
        or
        jogador_id
        not in sala["jogadores"]
    ):

        flash(
            "Você não faz parte dessa sala."
        )

        return redirect(
            url_for(
                "multiplayer.inicio"
            )
        )

    host = (
        str(current_user.id)
        ==
        sala["host_id"]
        and
        session.get(
            "multiplayer_host"
        )
    )

    return render_template(

        "multiplayer/lobby.html",

        sala=sala,

        codigo=codigo,

        host=host,

        jogador_id=jogador_id
    )


# ============================================================
# JOGO
# ============================================================

@multiplayer_bp.route(
    "/jogo/<codigo>"
)
@login_required
def jogo(codigo):

    sala = buscar_sala(
        codigo
    )

    if not sala:

        return redirect(
            url_for(
                "multiplayer.inicio"
            )
        )

    jogador_id = session.get(
        "multiplayer_jogador"
    )

    if (
        not jogador_id
        or
        jogador_id
        not in sala["jogadores"]
    ):

        return redirect(
            url_for(
                "multiplayer.inicio"
            )
        )

    return render_template(

        "multiplayer/jogo.html",

        codigo=codigo,

        jogador_id=jogador_id,

        host=bool(
            session.get(
                "multiplayer_host"
            )
        )
    )


# ============================================================
# RESULTADO
# ============================================================

@multiplayer_bp.route(
    "/resultado/<codigo>"
)
@login_required
def resultado(codigo):

    sala = buscar_sala(
        codigo
    )

    if not sala:

        return redirect(
            url_for(
                "multiplayer.inicio"
            )
        )

    return render_template(

        "multiplayer/resultado.html",

        codigo=codigo
    )