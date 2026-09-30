from flask import (
    Blueprint,
)

from .services import (
    conquistas_perfil,
)


conquistas_bp = Blueprint(
    "conquistas",
    __name__,
    url_prefix="/conquistas"
)


@conquistas_bp.app_context_processor
def contexto_conquistas():

    return {
        "conquistas_perfil":
            conquistas_perfil,
    }
