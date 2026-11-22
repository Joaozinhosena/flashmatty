import csv
from pathlib import Path

from models import db
from .models import QuestaoBanco, AlternativaQuestao


def _bool(valor, padrao=False):
    if valor is None or str(valor).strip() == "":
        return padrao

    return str(valor).strip().casefold() in {
        "1",
        "true",
        "sim",
        "s",
        "yes"
    }


def importar_csv(caminho):
    """
    Importa/atualiza questões por código.

    O arquivo deve usar UTF-8 com cabeçalho igual ao
    questoes_professores_modelo.csv.
    """

    caminho = Path(caminho)

    total = 0

    with caminho.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:

        leitor = csv.DictReader(
            arquivo
        )

        for linha in leitor:

            codigo = (
                linha.get("codigo", "")
                .strip()
            )

            if not codigo:
                continue

            questao = (
                QuestaoBanco.query
                .filter_by(
                    codigo=codigo
                )
                .first()
            )

            if questao is None:
                questao = QuestaoBanco(
                    codigo=codigo
                )

                db.session.add(
                    questao
                )

            questao.ano = (
                linha.get("ano", "")
                .strip()
            )

            questao.tema = (
                linha.get("tema", "")
                .strip()
            )

            questao.assunto = (
                linha.get("assunto", "")
                .strip()
            )

            questao.etapa = (
                linha.get("etapa", "")
                .strip()
                or None
            )

            questao.tipo = (
                linha.get("tipo", "")
                .strip()
            )

            questao.tipo_ui = (
                linha.get(
                    "tipo_ui",
                    "multipla_escolha"
                ).strip()
                or "multipla_escolha"
            )

            questao.enunciado = (
                linha.get("enunciado", "")
                .strip()
            )

            questao.resposta_correta = (
                linha.get(
                    "resposta_correta",
                    ""
                )
                .strip()
            )

            questao.explicacao = (
                linha.get(
                    "explicacao",
                    ""
                )
                .strip()
                or None
            )

            questao.instrucao = (
                linha.get(
                    "instrucao",
                    ""
                )
                .strip()
                or None
            )

            questao.habilidade_bncc = (
                linha.get(
                    "habilidade_bncc",
                    ""
                )
                .strip()
                or None
            )

            try:
                questao.dificuldade = int(
                    linha.get(
                        "dificuldade",
                        2
                    )
                    or 2
                )
            except ValueError:
                questao.dificuldade = 2

            questao.autor = (
                linha.get("autor", "")
                .strip()
                or None
            )

            questao.instituicao = (
                linha.get(
                    "instituicao",
                    ""
                )
                .strip()
                or None
            )

            questao.fonte = (
                linha.get("fonte", "")
                .strip()
                or None
            )

            questao.licenca = (
                linha.get("licenca", "")
                .strip()
                or None
            )

            questao.revisada = _bool(
                linha.get("revisada"),
                False
            )

            questao.ativa = _bool(
                linha.get("ativa"),
                True
            )

            db.session.flush()

            AlternativaQuestao.query.filter_by(
                questao_id=questao.id
            ).delete()

            for numero in range(1, 7):

                valor = (
                    linha.get(
                        f"alternativa_{numero}_valor",
                        ""
                    )
                    .strip()
                )

                texto = (
                    linha.get(
                        f"alternativa_{numero}_texto",
                        ""
                    )
                    .strip()
                )

                if not valor and not texto:
                    continue

                if not valor:
                    valor = texto

                if not texto:
                    texto = valor

                db.session.add(
                    AlternativaQuestao(
                        questao_id=questao.id,
                        valor=valor,
                        texto=texto,
                        ordem=numero
                    )
                )

            total += 1

    db.session.commit()

    return total
