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

from multiplayer.room_manager import (
    criar_sala,
    buscar_sala,
    adicionar_jogador
)


# ============================================================
# BLUEPRINT
# ============================================================

multiplayer_bp = Blueprint(
    "multiplayer",
    __name__,
    url_prefix="/multiplayer"
)


# ============================================================
# CONFIGURAÇÕES PERMITIDAS
# ============================================================

ASSUNTOS_PERMITIDOS = {
    "misto",
    "adicao",
    "subtracao",
    "multiplicacao",
    "divisao",
    "fracao",
    "tempo",
    "area",
    "perimetro",
    "angulo"
}


QUANTIDADES_PERMITIDAS = {
    5,
    10,
    15,
    20
}


TEMPOS_PERMITIDOS = {
    10,
    20,
    30,
    45
}


# ============================================================
# AUXILIARES
# ============================================================

def obter_nome_usuario():
    """
    Retorna um nome seguro para utilizar
    dentro do multiplayer.
    """

    nome = str(
        getattr(
            current_user,
            "nome",
            ""
        )
        or
        ""
    ).strip()

    if not nome:

        nome = str(
            getattr(
                current_user,
                "username",
                ""
            )
            or
            ""
        ).strip()

    if not nome:

        nome = "Jogador"

    return nome[:20]


def obter_jogador_sessao():

    return str(
        session.get(
            "multiplayer_jogador",
            ""
        )
        or
        ""
    ).strip()


def jogador_pertence_sala(
    sala,
    jogador_id
):

    if (
        not sala
        or
        not jogador_id
    ):
        return False

    return (
        str(jogador_id)
        in
        sala.get(
            "jogadores",
            {}
        )
    )


def jogador_e_host(
    sala,
    jogador_id
):

    if (
        not sala
        or
        not jogador_id
    ):
        return False

    return (
        str(
            sala.get(
                "host_id",
                ""
            )
        )
        ==
        str(jogador_id)
    )


def registrar_sessao_multiplayer(
    codigo,
    jogador_id,
    host=False
):

    session[
        "multiplayer_codigo"
    ] = str(codigo)

    session[
        "multiplayer_jogador"
    ] = str(jogador_id)

    session[
        "multiplayer_host"
    ] = bool(host)


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
    methods=[
        "GET",
        "POST"
    ]
)
@login_required
def criar():

    if request.method == "POST":

        # ----------------------------------------------------
        # ASSUNTO
        # ----------------------------------------------------

        assunto = str(
            request.form.get(
                "assunto",
                "misto"
            )
            or
            "misto"
        ).strip().lower()


        if (
            assunto
            not in
            ASSUNTOS_PERMITIDOS
        ):

            assunto = "misto"


        # ----------------------------------------------------
        # QUANTIDADE
        # ----------------------------------------------------

        try:

            quantidade = int(
                request.form.get(
                    "quantidade",
                    10
                )
            )

        except (
            TypeError,
            ValueError
        ):

            quantidade = 10


        if (
            quantidade
            not in
            QUANTIDADES_PERMITIDAS
        ):

            quantidade = 10


        # ----------------------------------------------------
        # TEMPO
        # ----------------------------------------------------

        try:

            tempo = int(
                request.form.get(
                    "tempo",
                    20
                )
            )

        except (
            TypeError,
            ValueError
        ):

            tempo = 20


        if (
            tempo
            not in
            TEMPOS_PERMITIDOS
        ):

            tempo = 20


        # ----------------------------------------------------
        # HOST
        # ----------------------------------------------------

        host_id = str(
            current_user.id
        )

        host_nome = (
            obter_nome_usuario()
        )


        # ----------------------------------------------------
        # CRIA SALA
        # ----------------------------------------------------

        sala = criar_sala(

            host_id,

            host_nome,

            {
                "assunto":
                    assunto,

                "quantidade":
                    quantidade,

                "tempo":
                    tempo
            }
        )


        if not sala:

            flash(
                "Não foi possível criar a sala.",
                "error"
            )

            return redirect(
                url_for(
                    "multiplayer.criar"
                )
            )


      
  

       


        # ----------------------------------------------------
        # SESSÃO
        # ----------------------------------------------------

        registrar_sessao_multiplayer(

            sala[
                "codigo"
            ],

            host_id,

            host=True
        )


        # ----------------------------------------------------
        # LOBBY
        # ----------------------------------------------------

        return redirect(

            url_for(

                "multiplayer.lobby",

                codigo=
                    sala[
                        "codigo"
                    ]

            )

        )


    return render_template(
        "multiplayer/criar.html"
    )


# ============================================================
# ENTRAR NA SALA
# ============================================================

@multiplayer_bp.route(
    "/entrar",
    methods=[
        "GET",
        "POST"
    ]
)
@login_required
def entrar():

    if request.method == "POST":

        # ----------------------------------------------------
        # CÓDIGO
        # ----------------------------------------------------

        codigo = str(
            request.form.get(
                "codigo",
                ""
            )
            or
            ""
        ).strip()


        if (
            len(codigo) != 6
            or
            not codigo.isdigit()
        ):

            flash(
                "Digite um código de sala válido.",
                "error"
            )

            return redirect(
                url_for(
                    "multiplayer.entrar"
                )
            )


        # ----------------------------------------------------
        # BUSCAR SALA
        # ----------------------------------------------------

        sala = buscar_sala(
            codigo
        )


        if not sala:

            flash(
                "Sala não encontrada.",
                "error"
            )

            return redirect(
                url_for(
                    "multiplayer.entrar"
                )
            )


        # ----------------------------------------------------
        # ESTADO DA SALA
        # ----------------------------------------------------

        estado = sala.get(
            "estado",
            "lobby"
        )


        if estado != "lobby":

            flash(
                "Essa partida já foi iniciada.",
                "warning"
            )

            return redirect(
                url_for(
                    "multiplayer.entrar"
                )
            )


        # ----------------------------------------------------
        # APELIDO
        # ----------------------------------------------------

        apelido = str(
            request.form.get(
                "apelido",
                ""
            )
            or
            ""
        ).strip()


        if not apelido:

            apelido = (
                obter_nome_usuario()
            )


        apelido = (
            apelido[:20]
        )


        # ----------------------------------------------------
        # ID DO JOGADOR
        # ----------------------------------------------------

        jogador_id = (

            f"{current_user.id}-"

            f"{uuid.uuid4().hex[:8]}"

        )


        # ----------------------------------------------------
        # ADICIONA À SALA
        # ----------------------------------------------------

        jogador = adicionar_jogador(

            codigo,

            jogador_id,

            apelido

        )


        if not jogador:

            flash(
                "Não foi possível entrar na sala.",
                "error"
            )

            return redirect(
                url_for(
                    "multiplayer.entrar"
                )
            )


        # ----------------------------------------------------
        # SESSÃO
        # ----------------------------------------------------

        registrar_sessao_multiplayer(

            codigo,

            jogador_id,

            host=False
        )


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
def lobby(
    codigo
):

    codigo = str(
        codigo
    ).strip()


    sala = buscar_sala(
        codigo
    )


    if not sala:

        flash(
            "Sala não encontrada.",
            "error"
        )

        return redirect(
            url_for(
                "multiplayer.inicio"
            )
        )


    jogador_id = (
        obter_jogador_sessao()
    )


    if not jogador_pertence_sala(
        sala,
        jogador_id
    ):

        flash(
            "Você não faz parte dessa sala.",
            "error"
        )

        return redirect(
            url_for(
                "multiplayer.inicio"
            )
        )


    # --------------------------------------------------------
    # REDIRECIONAMENTO DE ESTADO
    # --------------------------------------------------------

    estado = sala.get(
        "estado",
        "lobby"
    )


    if estado == "jogando":

        return redirect(

            url_for(

                "multiplayer.jogo",

                codigo=codigo

            )

        )


    if estado == "finalizado":

        return redirect(

            url_for(

                "multiplayer.resultado",

                codigo=codigo

            )

        )


    # --------------------------------------------------------
    # HOST
    # --------------------------------------------------------

    host = jogador_e_host(
        sala,
        jogador_id
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
def jogo(
    codigo
):

    codigo = str(
        codigo
    ).strip()


    sala = buscar_sala(
        codigo
    )


    if not sala:

        flash(
            "Sala não encontrada.",
            "error"
        )

        return redirect(
            url_for(
                "multiplayer.inicio"
            )
        )


    jogador_id = (
        obter_jogador_sessao()
    )


    if not jogador_pertence_sala(
        sala,
        jogador_id
    ):

        flash(
            "Você não faz parte dessa partida.",
            "error"
        )

        return redirect(
            url_for(
                "multiplayer.inicio"
            )
        )


    estado = sala.get(
        "estado",
        "lobby"
    )


    # Ainda não começou.
    if estado == "lobby":

        return redirect(

            url_for(

                "multiplayer.lobby",

                codigo=codigo

            )

        )


    # Já terminou.
    if estado == "finalizado":

        return redirect(

            url_for(

                "multiplayer.resultado",

                codigo=codigo

            )

        )


    host = jogador_e_host(
        sala,
        jogador_id
    )


    return render_template(

        "multiplayer/jogo.html",

        codigo=codigo,

        jogador_id=jogador_id,

        host=host

    )


# ============================================================
# RESULTADO
# ============================================================

@multiplayer_bp.route(
    "/resultado/<codigo>"
)
@login_required
def resultado(
    codigo
):

    codigo = str(
        codigo
    ).strip()


    sala = buscar_sala(
        codigo
    )


    if not sala:

        flash(
            "Essa partida não está mais disponível.",
            "warning"
        )

        return redirect(
            url_for(
                "multiplayer.inicio"
            )
        )


    jogador_id = (
        obter_jogador_sessao()
    )


    if not jogador_pertence_sala(
        sala,
        jogador_id
    ):

        flash(
            "Você não participou dessa partida.",
            "error"
        )

        return redirect(
            url_for(
                "multiplayer.inicio"
            )
        )


    estado = sala.get(
        "estado"
    )


    # Se ainda estiver no lobby.
    if estado == "lobby":

        return redirect(

            url_for(

                "multiplayer.lobby",

                codigo=codigo

            )

        )


    # Se ainda estiver jogando.
    if estado == "jogando":

        return redirect(

            url_for(

                "multiplayer.jogo",

                codigo=codigo

            )

        )


    return render_template(

        "multiplayer/resultado.html",

        codigo=codigo

    )