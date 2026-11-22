import json
import sys
from pathlib import Path

from app import app
from models import db
from atividades.models import QuestaoBanco, AlternativaQuestao


if len(sys.argv) < 2:
    print("Uso: python importar_lote_real_im.py questoes_reais_im_30.json")
    raise SystemExit(1)

dados = json.loads(
    Path(sys.argv[1]).read_text(encoding="utf-8")
)

with app.app_context():

    total = 0

    for item in dados.get("questoes", []):

        codigo = item["codigo"]

        q = (
            QuestaoBanco.query
            .filter_by(codigo=codigo)
            .first()
        )

        if q is None:
            q = QuestaoBanco(codigo=codigo)
            db.session.add(q)

        q.ano = item["ano"]
        q.tema = item["tema"]
        q.assunto = item["assunto"]
        q.etapa = str(item["etapa"])
        q.tipo = item["tipo"]
        q.tipo_ui = item["tipo_ui"]
        q.enunciado = item["enunciado"]
        q.resposta_correta = str(item["resposta_correta"])
        q.explicacao = item.get("explicacao") or None
        q.instrucao = item.get("instrucao") or None
        q.habilidade_bncc = None
        q.dificuldade = int(item.get("dificuldade", 2))
        q.autor = item.get("autor")
        q.instituicao = item.get("instituicao")
        q.fonte = (
            item.get("fonte", "")
            + " | "
            + item.get("fonte_referencia", "")
        ).strip(" |")
        q.licenca = item.get("licenca")
        q.revisada = True
        q.ativa = True

        db.session.flush()

        AlternativaQuestao.query.filter_by(
            questao_id=q.id
        ).delete(
            synchronize_session=False
        )

        for ordem, alt in enumerate(
            item.get("alternativas", []),
            start=1
        ):
            db.session.add(
                AlternativaQuestao(
                    questao_id=q.id,
                    valor=str(alt["valor"]),
                    texto=str(alt["texto"]),
                    ordem=ordem
                )
            )

        total += 1

    db.session.commit()

print(
    f"{total} questões com fonte real foram importadas."
)
