"""Regras de negócio relacionadas aos conteúdos acadêmicos."""

from ..persistencia import conteudos as repo_conteudos
from ..persistencia import disciplinas as repo_disciplinas


def adicionar_conteudo(disciplina_id, titulo):
    titulo = titulo.strip()

    if not titulo:
        return None, ["O título do conteúdo é obrigatório."]

    if repo_disciplinas.buscar(disciplina_id) is None:
        return None, ["Disciplina não encontrada."]

    conteudo = repo_conteudos.adicionar(
        disciplina_id,
        titulo,
    )

    return conteudo, []


def listar_conteudos(disciplina_id=None):
    if disciplina_id is None:
        return repo_conteudos.listar()

    return repo_conteudos.listar_por_disciplina(disciplina_id)


def buscar_conteudo(conteudo_id):
    return repo_conteudos.buscar(conteudo_id)


def atualizar_conteudo(conteudo_id, titulo):
    conteudo = repo_conteudos.buscar(conteudo_id)

    if conteudo is None:
        return None, ["Conteúdo não encontrado."]

    titulo = titulo.strip()

    if not titulo:
        return None, ["O título do conteúdo não pode ficar vazio."]

    atualizado = repo_conteudos.atualizar(
        conteudo_id,
        titulo=titulo,
    )

    return atualizado, []


def remover_conteudo(conteudo_id):
    if repo_conteudos.buscar(conteudo_id) is None:
        return False, ["Conteúdo não encontrado."]

    repo_conteudos.remover(conteudo_id)

    return True, []
