"""Regras de negócio relacionadas às sessões de estudo."""

from datetime import datetime, date

from ..persistencia import sessoes_estudo as repo_sessoes
from ..persistencia import disciplinas as repo_disciplinas


TIPOS = ("academica", "pessoal")


def _id_valido(valor):
    return (
        isinstance(valor, int)
        and not isinstance(valor, bool)
        and valor > 0
    )


def _data_valida(texto):
    if not isinstance(texto, str):
        return None

    try:
        data_convertida = datetime.strptime(
            texto,
            "%Y-%m-%d",
        ).date()
    except ValueError:
        return None

    if data_convertida.strftime("%Y-%m-%d") != texto:
        return None

    return data_convertida


def adicionar_sessao(
    tipo,
    disciplina_id,
    assunto,
    duracao_min,
    data,
):

    tipo = tipo.strip().lower() if isinstance(tipo, str) else tipo
    assunto = assunto.strip() if isinstance(assunto, str) else ""
    data = data.strip() if isinstance(data, str) else ""

    if tipo not in TIPOS:
        return None, ["Tipo inválido. Use academica ou pessoal."]

    if not assunto:
        return None, ["O assunto é obrigatório."]

    if (
        not isinstance(duracao_min, int)
        or isinstance(duracao_min, bool)
        or duracao_min <= 0
    ):
        return None, [
            "A duração deve ser informada em minutos e ser maior que zero."
        ]

    data_convertida = _data_valida(data)

    if data_convertida is None:
        return None, ["Data inválida. Use o formato AAAA-MM-DD."]

    if data_convertida > date.today():
        return None, ["A data da sessão não pode ser futura."]

    if tipo == "pessoal":
        if disciplina_id is not None:
            return None, ["Sessão pessoal não pode ter disciplina."]

    if tipo == "academica" and disciplina_id is not None:
        if not _id_valido(disciplina_id):
            return None, ["ID de disciplina inválido."]

        if repo_disciplinas.buscar(disciplina_id) is None:
            return None, ["Disciplina não encontrada."]

    sessao = repo_sessoes.adicionar(
        duracao_min,
        tipo=tipo,
        disciplina_id=disciplina_id,
        assunto=assunto,
        data=data,
    )

    return sessao, []


def listar_sessoes(tipo=None, disciplina_id=None):
    sessoes = repo_sessoes.listar()

    if tipo is not None:
        sessoes = [
            sessao
            for sessao in sessoes
            if sessao.get("tipo") == tipo
        ]

    if disciplina_id is not None:
        sessoes = [
            sessao
            for sessao in sessoes
            if sessao.get("disciplina_id") == disciplina_id
        ]

    return sessoes


def buscar_sessao(sessao_id):
    return repo_sessoes.buscar(sessao_id)


def listar_disciplinas():
    return repo_disciplinas.listar()


def remover_sessao(sessao_id):
    if repo_sessoes.buscar(sessao_id) is None:
        return False, ["Sessão não encontrada."]

    repo_sessoes.remover(sessao_id)

    return True, []