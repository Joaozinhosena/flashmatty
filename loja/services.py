from .catalogo import (
    TIPOS,
    obter_item,
)

from .models import (
    CompraCosmetico,
    PersonalizacaoPerfil,
)


SLOT_POR_TIPO = {
    "titulo": "titulo_id",
    "fundo": "fundo_id",
    "moldura": "moldura_id",
    "badge": "badge_id",
    "nome": "nome_id",
    "card": "card_id",
    "efeito": "efeito_id",
}


def ids_comprados(
    usuario_id
):

    registros = (

        CompraCosmetico.query

        .filter_by(
            usuario_id=
                int(usuario_id)
        )

        .all()
    )

    return {
        registro.item_id
        for registro in registros
    }


def usuario_possui_item(
    usuario_id,
    item_id
):

    return (

        CompraCosmetico.query

        .filter_by(
            usuario_id=
                int(usuario_id),

            item_id=
                str(item_id)
        )

        .first()

        is not None
    )


def personalizacao_publica(
    usuario_id
):

    registro = (
        PersonalizacaoPerfil.obter(
            usuario_id,
            criar=False
        )
    )

    resultado = {
        tipo: None
        for tipo in TIPOS
    }

    if not registro:
        return resultado


    for tipo, campo in (
        SLOT_POR_TIPO.items()
    ):

        item_id = getattr(
            registro,
            campo,
            None
        )

        if not item_id:
            continue


        item = obter_item(
            item_id
        )


        if (
            item
            and
            item["tipo"] == tipo
        ):

            resultado[
                tipo
            ] = item


    return resultado


def equipado_por_tipo(
    usuario_id
):

    personalizacao = (
        personalizacao_publica(
            usuario_id
        )
    )

    return {

        tipo:
            (
                item["id"]
                if item
                else None
            )

        for tipo, item
        in personalizacao.items()

    }
