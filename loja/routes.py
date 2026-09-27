import secrets

from flask import (
    Blueprint,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from flask_login import (
    current_user,
    login_required,
)

from sqlalchemy.exc import (
    IntegrityError,
)

from models import (
    db,
    Usuario,
)

from .catalogo import (
    TIPOS,
    TIPOS_LABEL,
    ITENS,
    obter_item,
    itens_por_tipo,
)

from .models import (
    CompraCosmetico,
    PersonalizacaoPerfil,
)

from .services import (
    SLOT_POR_TIPO,
    equipado_por_tipo,
    ids_comprados,
    personalizacao_publica,
    usuario_possui_item,
)


loja_bp = Blueprint(
    "loja",
    __name__,
    url_prefix="/loja"
)


# ============================================================
# CSRF
# ============================================================

def gerar_csrf_token():

    token = session.get(
        "_loja_csrf_token"
    )

    if not token:

        token = (
            secrets.token_urlsafe(
                32
            )
        )

        session[
            "_loja_csrf_token"
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
            "_loja_csrf_token",
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
# CONTEXTO GLOBAL
# ============================================================

@loja_bp.app_context_processor
def contexto_loja():

    return {

        "loja_csrf_token":
            gerar_csrf_token,

        "loja_personalizacao":
            personalizacao_publica,

        "loja_tipos_label":
            TIPOS_LABEL,

    }


# ============================================================
# LOJA
# ============================================================

@loja_bp.route(
    "/"
)
@login_required
def index():

    comprados = (
        ids_comprados(
            current_user.id
        )
    )

    equipados = (
        equipado_por_tipo(
            current_user.id
        )
    )

    return render_template(
        "loja/index.html",

        catalogo=
            itens_por_tipo(),

        tipos=
            TIPOS,

        tipos_label=
            TIPOS_LABEL,

        comprados=
            comprados,

        equipados=
            equipados
    )


# ============================================================
# INVENTÁRIO
# ============================================================

@loja_bp.route(
    "/inventario"
)
@login_required
def inventario():

    comprados = (
        ids_comprados(
            current_user.id
        )
    )

    itens = [

        item

        for item in ITENS

        if item["id"]
        in comprados
    ]

    equipados = (
        equipado_por_tipo(
            current_user.id
        )
    )

    return render_template(
        "loja/inventario.html",

        itens=
            itens,

        tipos_label=
            TIPOS_LABEL,

        equipados=
            equipados
    )


# ============================================================
# COMPRAR
# ============================================================

@loja_bp.route(
    "/comprar/<item_id>",
    methods=[
        "POST"
    ]
)
@login_required
def comprar(
    item_id
):

    validar_csrf()


    item = obter_item(
        item_id
    )

    if not item:

        abort(
            404
        )


    if usuario_possui_item(
        current_user.id,
        item["id"]
    ):

        flash(
            "Você já possui este item."
        )

        return redirect(
            url_for(
                "loja.index"
            )
        )


    usuario = (
        db.session.get(
            Usuario,
            current_user.id
        )
    )

    if not usuario:

        abort(
            404
        )


    moedas = int(
        usuario.moedas
        or 0
    )


    if moedas < item["preco"]:

        flash(
            (
                "Moedas insuficientes. "
                f"Você possui {moedas} moedas "
                f"e este item custa "
                f"{item['preco']}."
            )
        )

        return redirect(
            url_for(
                "loja.index"
            )
        )


    try:

        usuario.moedas = (
            moedas
            -
            item["preco"]
        )


        compra = CompraCosmetico(

            usuario_id=
                usuario.id,

            item_id=
                item["id"]

        )


        db.session.add(
            compra
        )


        # Garante que o registro de
        # personalização exista.
        PersonalizacaoPerfil.obter(
            usuario.id,
            criar=True
        )


        db.session.commit()


    except IntegrityError:

        db.session.rollback()

        flash(
            "Este item já está no seu inventário."
        )

        return redirect(
            url_for(
                "loja.index"
            )
        )


    except Exception:

        db.session.rollback()

        raise


    flash(
        (
            f"{item['icone']} "
            f"{item['nome']} comprado! "
            f"Saldo: {usuario.moedas} moedas."
        )
    )


    return redirect(
        url_for(
            "loja.index"
        )
    )


# ============================================================
# EQUIPAR
# ============================================================

@loja_bp.route(
    "/equipar/<item_id>",
    methods=[
        "POST"
    ]
)
@login_required
def equipar(
    item_id
):

    validar_csrf()


    item = obter_item(
        item_id
    )

    if not item:

        abort(
            404
        )


    if not usuario_possui_item(
        current_user.id,
        item["id"]
    ):

        abort(
            403
        )


    campo = SLOT_POR_TIPO.get(
        item["tipo"]
    )

    if not campo:

        abort(
            400
        )


    personalizacao = (
        PersonalizacaoPerfil.obter(
            current_user.id,
            criar=True
        )
    )


    setattr(
        personalizacao,
        campo,
        item["id"]
    )


    db.session.commit()


    flash(
        (
            f"{item['icone']} "
            f"{item['nome']} equipado."
        )
    )


    return redirect(
        request.form.get(
            "voltar"
        )
        or
        url_for(
            "loja.inventario"
        )
    )


# ============================================================
# DESEQUIPAR
# ============================================================

@loja_bp.route(
    "/desequipar/<tipo>",
    methods=[
        "POST"
    ]
)
@login_required
def desequipar(
    tipo
):

    validar_csrf()


    campo = SLOT_POR_TIPO.get(
        tipo
    )

    if not campo:

        abort(
            404
        )


    personalizacao = (
        PersonalizacaoPerfil.obter(
            current_user.id,
            criar=True
        )
    )


    setattr(
        personalizacao,
        campo,
        None
    )


    db.session.commit()


    flash(
        (
            f"{TIPOS_LABEL.get(tipo, tipo)}: "
            "item removido."
        )
    )


    return redirect(
        request.form.get(
            "voltar"
        )
        or
        url_for(
            "loja.inventario"
        )
    )


# ============================================================
# API PÚBLICA PARA INTEGRAÇÕES
# ============================================================

@loja_bp.route(
    "/api/personalizacao/<int:usuario_id>"
)
@login_required
def api_personalizacao(
    usuario_id
):

    usuario = (
        db.session.get(
            Usuario,
            usuario_id
        )
    )

    if not usuario:

        abort(
            404
        )


    dados = (
        personalizacao_publica(
            usuario_id
        )
    )


    def serializar(item):

        if not item:
            return None

        return {
            "id":
                item["id"],

            "tipo":
                item["tipo"],

            "nome":
                item["nome"],

            "icone":
                item["icone"],

            "raridade":
                item["raridade"],

            "valor":
                item["valor"],
        }


    return jsonify({

        tipo:
            serializar(item)

        for tipo, item
        in dados.items()

    })
