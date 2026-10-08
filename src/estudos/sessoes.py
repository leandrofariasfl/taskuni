"""Regras de negócio relacionadas às sessões de estudo."""

from ..persistencia import sessoes_estudo as repo_sessoes
from ..persistencia import disciplinas as repo_disciplinas


def adicionar_sessao(disciplina_id, assunto, horas, data):
    assunto = assunto.strip()
    data = data.strip()

    if repo_disciplinas.buscar(disciplina_id) is None:
        return None, ["Disciplina não encontrada."]

    if not assunto:
        return None, ["O assunto é obrigatório."]

    if not isinstance(horas, (int, float)) or isinstance(horas, bool) or horas <= 0:
        return None, ["A duração em horas deve ser maior que zero."]

    if not data:
        return None, ["A data é obrigatória."]

    sessao = repo_sessoes.adicionar(
        int(horas * 60),
        disciplina_id=disciplina_id,
        assunto=assunto,
        data=data,
    )

    return sessao, []


def listar_sessoes(disciplina_id=None):
    if disciplina_id is None:
        return repo_sessoes.listar()

    return [
        sessao
        for sessao in repo_sessoes.listar()
        if sessao.get("disciplina_id") == disciplina_id
    ]


def buscar_sessao(sessao_id):
    return repo_sessoes.buscar(sessao_id)


def remover_sessao(sessao_id):
    if repo_sessoes.buscar(sessao_id) is None:
        return False, ["Sessão não encontrada."]

    repo_sessoes.remover(sessao_id)

    return True, []
