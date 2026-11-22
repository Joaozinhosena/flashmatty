import sys

from app import app
from models import db
from atividades.models import QuestaoBanco


with app.app_context():

    antigas = (
        QuestaoBanco.query
        .filter(
            ~QuestaoBanco.codigo.like("IM-%")
        )
        .all()
    )

    print(
        f"{len(antigas)} questões antigas/não-IM encontradas."
    )

    if "--confirmar" not in sys.argv:
        print("")
        print("Nada foi alterado.")
        print(
            "Para desativar as antigas:"
        )
        print(
            "python .\\desativar_banco_gerado.py --confirmar"
        )
        raise SystemExit(0)

    for q in antigas:
        q.revisada = False
        q.ativa = False

    db.session.commit()

    print(
        f"{len(antigas)} questões antigas/não-IM desativadas."
    )
