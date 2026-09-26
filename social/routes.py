import html
import secrets
from datetime import datetime
from io import BytesIO

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)

from flask_login import (
    current_user,
    login_required,
)

from PIL import (
    Image,
    ImageOps,
    UnidentifiedImageError,
)

from sqlalchemy import (
    and_,
    or_,
)

from curriculum import CURRICULO

from models import (
    db,
    Usuario,
    ProgressoAssunto,
    ProgressoEtapa,
)

from .models import (
    Amizade,
    PerfilUsuario,
)

from .presence import (
    esta_online,
)


# ============================================================
# BLUEPRINT
# ============================================================

social_bp = Blueprint(
    "social",
    __name__,
    url_prefix="/social"
)


# ============================================================
# CONFIGURAÇÕES
# ============================================================

MAX_FOTO_BYTES = (
    3 * 1024 * 1024
)

VISIBILIDADES = {
    "todos",
    "amigos",
    "privado",
}


# ============================================================
# CSRF
# ============================================================

def gerar_csrf_token():

    token = session.get(
        "_social_csrf_token"
    )


    if not token:

        token = (
            secrets.token_urlsafe(
                32
            )
        )


        session[
            "_social_csrf_token"
        ] = token


    return token


def validar_csrf():

    enviado = (
        request.form.get(
            "_csrf_token",
            ""
        )
    )


    esperado = (
        session.get(
            "_social_csrf_token",
            ""
        )
    )


    if (
        not enviado
        or
        not esperado
        or
        not secrets.compare_digest(
            enviado,
            esperado
        )
    ):

        abort(
            400
        )


# ============================================================
# RELAÇÃO ENTRE USUÁRIOS
# ============================================================

def obter_relacao(
    usuario_a_id,
    usuario_b_id
):

    usuario_a_id = int(
        usuario_a_id
    )


    usuario_b_id = int(
        usuario_b_id
    )


    return (
        Amizade.query

        .filter(

            or_(

                and_(
                    Amizade.solicitante_id
                    ==
                    usuario_a_id,

                    Amizade.destinatario_id
                    ==
                    usuario_b_id,
                ),

                and_(
                    Amizade.solicitante_id
                    ==
                    usuario_b_id,

                    Amizade.destinatario_id
                    ==
                    usuario_a_id,
                )

            )

        )

        .order_by(
            Amizade.id.desc()
        )

        .first()
    )


def sao_amigos(
    usuario_a_id,
    usuario_b_id
):

    relacao = obter_relacao(
        usuario_a_id,
        usuario_b_id
    )


    return bool(

        relacao

        and

        relacao.status
        ==
        "aceita"
    )


# ============================================================
# AMIGOS DO USUÁRIO
# ============================================================

def ids_amigos(
    usuario_id
):

    relacoes = (

        Amizade.query

        .filter(

            Amizade.status
            ==
            "aceita",

            or_(

                Amizade.solicitante_id
                ==
                usuario_id,

                Amizade.destinatario_id
                ==
                usuario_id

            )

        )

        .all()
    )


    resultado = []


    for relacao in relacoes:

        if (
            relacao.solicitante_id
            ==
            usuario_id
        ):

            resultado.append(
                relacao.destinatario_id
            )

        else:

            resultado.append(
                relacao.solicitante_id
            )


    return resultado


# ============================================================
# ESTATÍSTICAS
# ============================================================

def total_assuntos_curriculo():

    total = 0


    for ano in CURRICULO.values():

        for tema in (
            ano
            .get(
                "temas",
                {}
            )
            .values()
        ):

            total += len(
                tema.get(
                    "assuntos",
                    {}
                )
            )


    return total


def estatisticas_usuario(
    usuario
):

    xp = (
        usuario.xp
        or 0
    )


    moedas = (
        usuario.moedas
        or 0
    )


    acertos = (
        usuario.acertos
        or 0
    )


    erros = (
        usuario.erros
        or 0
    )


    total_respostas = (
        acertos
        +
        erros
    )


    if total_respostas:

        precisao = round(

            acertos
            /
            total_respostas
            *
            100

        )

    else:

        precisao = 0


    nivel = max(

        1,

        (
            xp // 100
        )
        +
        1

    )


    etapas_concluidas = (

        ProgressoEtapa.query

        .filter_by(
            usuario_id=
                usuario.id,

            concluida=
                True
        )

        .count()
    )


    assuntos_concluidos = (

        ProgressoAssunto.query

        .filter_by(
            usuario_id=
                usuario.id,

            concluido=
                True
        )

        .count()
    )


    total_assuntos = (
        total_assuntos_curriculo()
    )


    if total_assuntos:

        progresso_geral = round(

            assuntos_concluidos
            /
            total_assuntos
            *
            100

        )

    else:

        progresso_geral = 0


    return {

        "xp":
            xp,

        "moedas":
            moedas,

        "acertos":
            acertos,

        "erros":
            erros,

        "precisao":
            precisao,

        "nivel":
            nivel,

        "etapas_concluidas":
            etapas_concluidas,

        "assuntos_concluidos":
            assuntos_concluidos,

        "total_assuntos":
            total_assuntos,

        "progresso_geral":
            progresso_geral
    }


# ============================================================
# PRIVACIDADE
# ============================================================

def pode_ver_progresso(
    alvo
):

    if (
        current_user.is_authenticated
        and
        current_user.id
        ==
        alvo.id
    ):

        return True


    perfil = (
        PerfilUsuario.obter(
            alvo.id,
            criar=True
        )
    )


    visibilidade = (

        perfil.visibilidade_progresso

        or

        "amigos"
    )


    if (
        visibilidade
        ==
        "todos"
    ):

        return True


    if (
        visibilidade
        ==
        "privado"
    ):

        return False


    return (

        current_user.is_authenticated

        and

        sao_amigos(
            current_user.id,
            alvo.id
        )

    )


# ============================================================
# ÚLTIMO ACESSO
# ============================================================

def formatar_ultimo_acesso(
    data
):

    if not data:

        return "Nunca"


    agora = datetime.utcnow()


    segundos = max(

        0,

        int(
            (
                agora
                -
                data
            )
            .total_seconds()
        )

    )


    if segundos < 60:

        return "Agora"


    minutos = (
        segundos // 60
    )


    if minutos < 60:

        return (
            f"Há {minutos} min"
        )


    horas = (
        minutos // 60
    )


    if horas < 24:

        return (
            f"Há {horas} h"
        )


    dias = (
        horas // 24
    )


    if dias < 7:

        if dias == 1:

            return "Há 1 dia"

        return (
            f"Há {dias} dias"
        )


    return data.strftime(
        "%d/%m/%Y %H:%M"
    )


# ============================================================
# PROCESSAR FOTO
# ============================================================

def processar_foto(
    arquivo
):

    dados = arquivo.read(
        MAX_FOTO_BYTES + 1
    )


    if (
        len(dados)
        >
        MAX_FOTO_BYTES
    ):

        raise ValueError(
            "A foto deve ter no máximo 3 MB."
        )


    if not dados:

        raise ValueError(
            "Selecione uma imagem válida."
        )


    try:

        imagem = Image.open(
            BytesIO(
                dados
            )
        )


        imagem = (
            ImageOps.exif_transpose(
                imagem
            )
        )


        imagem.load()


    except (
        UnidentifiedImageError,
        OSError
    ):

        raise ValueError(
            "O arquivo enviado não é uma imagem válida."
        )


    if (
        imagem.width < 50
        or
        imagem.height < 50
    ):

        raise ValueError(
            "A imagem é pequena demais."
        )


    imagem = imagem.convert(
        "RGB"
    )


    imagem = ImageOps.fit(

        imagem,

        (
            512,
            512
        ),

        method=
            Image.Resampling.LANCZOS
    )


    saida = BytesIO()


    imagem.save(

        saida,

        format=
            "WEBP",

        quality=
            86,

        method=
            6
    )


    return (
        saida.getvalue(),
        "image/webp"
    )


# ============================================================
# CONTEXTO GLOBAL
# ============================================================

@social_bp.app_context_processor
def contexto_social():

    pedidos = 0


    if (
        current_user.is_authenticated
    ):

        pedidos = (

            Amizade.query

            .filter_by(

                destinatario_id=
                    current_user.id,

                status=
                    "pendente"

            )

            .count()
        )


    return {

        "social_csrf_token":
            gerar_csrf_token,

        "social_pedidos_pendentes":
            pedidos,

        "social_esta_online":
            esta_online,

        "social_formatar_ultimo_acesso":
            formatar_ultimo_acesso
    }


# ============================================================
# FOTO DE PERFIL
# ============================================================

@social_bp.route(
    "/foto/<int:usuario_id>"
)
def foto_perfil(
    usuario_id
):

    usuario = db.session.get(
        Usuario,
        usuario_id
    )


    if not usuario:

        abort(
            404
        )


    perfil = (
        PerfilUsuario.obter(
            usuario_id,
            criar=False
        )
    )


    if (
        perfil
        and
        perfil.foto_dados
        and
        perfil.foto_mime
    ):

        return send_file(

            BytesIO(
                perfil.foto_dados
            ),

            mimetype=
                perfil.foto_mime,

            max_age=
                0
        )


    nome = (

        usuario.nome

        or

        usuario.username

        or

        "U"

    ).strip()


    partes = [

        parte

        for parte
        in nome.split()

        if parte
    ]


    if not partes:

        iniciais = "U"

    elif len(partes) == 1:

        iniciais = (
            partes[0][:2]
            .upper()
        )

    else:

        iniciais = (

            partes[0][0]
            +
            partes[-1][0]

        ).upper()


    iniciais = html.escape(
        iniciais
    )


    svg = f"""
    <svg
        xmlns="http://www.w3.org/2000/svg"
        width="512"
        height="512"
        viewBox="0 0 512 512"
    >

        <rect
            width="512"
            height="512"
            rx="256"
            fill="#4f46e5"
        />

        <text
            x="256"
            y="285"
            text-anchor="middle"
            font-size="170"
            font-family="Arial"
            font-weight="700"
            fill="white"
        >
            {iniciais}
        </text>

    </svg>
    """


    return send_file(

        BytesIO(
            svg.encode(
                "utf-8"
            )
        ),

        mimetype=
            "image/svg+xml",

        max_age=
            0
    )


# ============================================================
# PERFIL
# ============================================================

@social_bp.route(
    "/perfil/<username>"
)
@login_required
def perfil(
    username
):

    usuario = (

        Usuario.query

        .filter_by(
            username=
                username
        )

        .first_or_404()
    )


    perfil_usuario = (
        PerfilUsuario.obter(
            usuario.id,
            criar=True
        )
    )


    relacao = None


    if (
        usuario.id
        !=
        current_user.id
    ):

        relacao = obter_relacao(

            current_user.id,

            usuario.id

        )


    amigos = ids_amigos(
        usuario.id
    )


    mostrar_progresso = (
        pode_ver_progresso(
            usuario
        )
    )


    estatisticas = None


    if mostrar_progresso:

        estatisticas = (
            estatisticas_usuario(
                usuario
            )
        )


    db.session.commit()


    return render_template(

        "social/perfil.html",

        usuario=
            usuario,

        perfil_usuario=
            perfil_usuario,

        relacao=
            relacao,

        quantidade_amigos=
            len(amigos),

        mostrar_progresso=
            mostrar_progresso,

        estatisticas=
            estatisticas,

        online=
            esta_online(
                usuario.id
            )

    )


# ============================================================
# EDITAR PERFIL
# ============================================================

@social_bp.route(
    "/editar-perfil",
    methods=[
        "GET",
        "POST"
    ]
)
@login_required
def editar_perfil():

    perfil_usuario = (
        PerfilUsuario.obter(
            current_user.id,
            criar=True
        )
    )


    if (
        request.method
        ==
        "POST"
    ):

        validar_csrf()


        nome = (
            request.form.get(
                "nome",
                ""
            )
            .strip()
        )


        bio = (
            request.form.get(
                "bio",
                ""
            )
            .strip()
        )


        visibilidade = (
            request.form.get(
                "visibilidade_progresso",
                "amigos"
            )
            .strip()
        )


        if not nome:

            flash(
                "O nome não pode ficar vazio."
            )

            return redirect(
                url_for(
                    "social.editar_perfil"
                )
            )


        if (
            len(nome)
            >
            80
        ):

            flash(
                "O nome deve ter no máximo 80 caracteres."
            )

            return redirect(
                url_for(
                    "social.editar_perfil"
                )
            )


        if (
            len(bio)
            >
            160
        ):

            flash(
                "A bio deve ter no máximo 160 caracteres."
            )

            return redirect(
                url_for(
                    "social.editar_perfil"
                )
            )


        if (
            visibilidade
            not in
            VISIBILIDADES
        ):

            visibilidade = (
                "amigos"
            )


        current_user.nome = (
            nome
        )


        perfil_usuario.bio = (
            bio
        )


        perfil_usuario.visibilidade_progresso = (
            visibilidade
        )


        if (
            request.form.get(
                "remover_foto"
            )
            ==
            "1"
        ):

            perfil_usuario.foto_dados = (
                None
            )

            perfil_usuario.foto_mime = (
                None
            )


        arquivo = (
            request.files.get(
                "foto"
            )
        )


        if (
            arquivo
            and
            arquivo.filename
        ):

            try:

                dados_foto, mime = (
                    processar_foto(
                        arquivo
                    )
                )

            except ValueError as erro:

                flash(
                    str(
                        erro
                    )
                )

                return redirect(
                    url_for(
                        "social.editar_perfil"
                    )
                )


            perfil_usuario.foto_dados = (
                dados_foto
            )


            perfil_usuario.foto_mime = (
                mime
            )


        db.session.commit()


        flash(
            "Perfil atualizado. ✅"
        )


        return redirect(

            url_for(

                "social.perfil",

                username=
                    current_user.username

            )

        )


    return render_template(

        "social/editar_perfil.html",

        perfil_usuario=
            perfil_usuario

    )


# ============================================================
# BUSCAR USUÁRIOS
# ============================================================

@social_bp.route(
    "/usuarios"
)
@login_required
def buscar_usuarios():

    termo = (
        request.args.get(
            "q",
            ""
        )
        .strip()
    )


    usuarios = []


    if termo:

        padrao = (
            f"%{termo}%"
        )


        usuarios = (

            Usuario.query

            .filter(

                Usuario.id
                !=
                current_user.id,

                or_(

                    Usuario.username.ilike(
                        padrao
                    ),

                    Usuario.nome.ilike(
                        padrao
                    )

                )

            )

            .order_by(
                Usuario.nome.asc()
            )

            .limit(
                30
            )

            .all()
        )


    relacoes = {}


    for usuario in usuarios:

        relacoes[
            usuario.id
        ] = obter_relacao(

            current_user.id,

            usuario.id

        )


    return render_template(

        "social/buscar_usuarios.html",

        termo=
            termo,

        usuarios=
            usuarios,

        relacoes=
            relacoes

    )


# ============================================================
# AMIGOS
# ============================================================

@social_bp.route(
    "/amigos"
)
@login_required
def amigos():

    ids = ids_amigos(
        current_user.id
    )


    lista_amigos = []


    if ids:

        lista_amigos = (

            Usuario.query

            .filter(
                Usuario.id.in_(
                    ids
                )
            )

            .order_by(
                Usuario.nome.asc()
            )

            .all()
        )


    recebidos = (

        Amizade.query

        .filter_by(

            destinatario_id=
                current_user.id,

            status=
                "pendente"

        )

        .order_by(
            Amizade.criado_em.desc()
        )

        .all()
    )


    enviados = (

        Amizade.query

        .filter_by(

            solicitante_id=
                current_user.id,

            status=
                "pendente"

        )

        .order_by(
            Amizade.criado_em.desc()
        )

        .all()
    )


    usuarios_recebidos = {}


    for relacao in recebidos:

        usuarios_recebidos[
            relacao.id
        ] = db.session.get(
            Usuario,
            relacao.solicitante_id
        )


    usuarios_enviados = {}


    for relacao in enviados:

        usuarios_enviados[
            relacao.id
        ] = db.session.get(
            Usuario,
            relacao.destinatario_id
        )


    return render_template(

        "social/amigos.html",

        amigos=
            lista_amigos,

        recebidos=
            recebidos,

        enviados=
            enviados,

        usuarios_recebidos=
            usuarios_recebidos,

        usuarios_enviados=
            usuarios_enviados

    )


# ============================================================
# ENVIAR AMIZADE
# ============================================================

@social_bp.route(
    "/amizade/enviar/<int:usuario_id>",
    methods=[
        "POST"
    ]
)
@login_required
def enviar_amizade(
    usuario_id
):

    validar_csrf()


    if (
        usuario_id
        ==
        current_user.id
    ):

        abort(
            400
        )


    alvo = db.session.get(
        Usuario,
        usuario_id
    )


    if not alvo:

        abort(
            404
        )


    relacao = obter_relacao(

        current_user.id,

        alvo.id

    )


    if relacao:

        if (
            relacao.status
            ==
            "aceita"
        ):

            flash(
                "Vocês já são amigos."
            )


        elif (
            relacao.status
            ==
            "pendente"
        ):

            flash(
                "Já existe uma solicitação pendente."
            )


        else:

            relacao.solicitante_id = (
                current_user.id
            )


            relacao.destinatario_id = (
                alvo.id
            )


            relacao.status = (
                "pendente"
            )


            db.session.commit()


            flash(
                f"Solicitação enviada para {alvo.nome}. ✅"
            )


    else:

        relacao = Amizade(

            solicitante_id=
                current_user.id,

            destinatario_id=
                alvo.id,

            status=
                "pendente"

        )


        db.session.add(
            relacao
        )


        db.session.commit()


        flash(
            f"Solicitação enviada para {alvo.nome}. ✅"
        )


    return redirect(

        request.referrer

        or

        url_for(
            "social.perfil",
            username=
                alvo.username
        )

    )


# ============================================================
# ACEITAR AMIZADE
# ============================================================

@social_bp.route(
    "/amizade/aceitar/<int:amizade_id>",
    methods=[
        "POST"
    ]
)
@login_required
def aceitar_amizade(
    amizade_id
):

    validar_csrf()


    relacao = db.session.get(
        Amizade,
        amizade_id
    )


    if (
        not relacao
        or
        relacao.destinatario_id
        !=
        current_user.id
        or
        relacao.status
        !=
        "pendente"
    ):

        abort(
            404
        )


    relacao.status = (
        "aceita"
    )


    db.session.commit()


    flash(
        "Solicitação aceita. 🎉"
    )


    return redirect(

        request.referrer

        or

        url_for(
            "social.amigos"
        )

    )


# ============================================================
# RECUSAR AMIZADE
# ============================================================

@social_bp.route(
    "/amizade/recusar/<int:amizade_id>",
    methods=[
        "POST"
    ]
)
@login_required
def recusar_amizade(
    amizade_id
):

    validar_csrf()


    relacao = db.session.get(
        Amizade,
        amizade_id
    )


    if (
        not relacao
        or
        relacao.destinatario_id
        !=
        current_user.id
        or
        relacao.status
        !=
        "pendente"
    ):

        abort(
            404
        )


    relacao.status = (
        "recusada"
    )


    db.session.commit()


    flash(
        "Solicitação recusada."
    )


    return redirect(

        request.referrer

        or

        url_for(
            "social.amigos"
        )

    )


# ============================================================
# REMOVER AMIGO
# ============================================================

@social_bp.route(
    "/amizade/remover/<int:usuario_id>",
    methods=[
        "POST"
    ]
)
@login_required
def remover_amigo(
    usuario_id
):

    validar_csrf()


    relacao = obter_relacao(

        current_user.id,

        usuario_id

    )


    if (
        not relacao
        or
        relacao.status
        !=
        "aceita"
    ):

        abort(
            404
        )


    db.session.delete(
        relacao
    )


    db.session.commit()


    flash(
        "Amigo removido."
    )


    return redirect(

        request.referrer

        or

        url_for(
            "social.amigos"
        )

    )