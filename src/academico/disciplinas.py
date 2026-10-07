"""Regras de negócio relacionadas às disciplinas."""

from ..persistencia import disciplinas as repo_disciplinas
from ..persistencia import conteudos as repo_conteudos


def adicionar_disciplina(nome, professor=None):
    nome = nome.strip()

    if not nome:
        return None, ["O nome da disciplina é obrigatório."]

    professor = professor.strip() if isinstance(professor, str) else professor

    for disciplina in repo_disciplinas.listar():
        if disciplina.get("nome", "").lower() == nome.lower():
            return None, ["Já existe uma disciplina com esse nome."]

    disciplina = repo_disciplinas.adicionar(
        nome,
        professor=professor or None,
    )

    return disciplina, []


def listar_disciplinas():
    return repo_disciplinas.listar()


def buscar_disciplina(disciplina_id):
    return repo_disciplinas.buscar(disciplina_id)


def atualizar_disciplina(disciplina_id, nome=None, professor=None):
    disciplina = repo_disciplinas.buscar(disciplina_id)

    if disciplina is None:
        return None, ["Disciplina não encontrada."]

    campos = {}

    if nome is not None:
        nome = nome.strip()

        if not nome:
            return None, ["O nome da disciplina não pode ficar vazio."]

        for outra in repo_disciplinas.listar():
            if (
                outra["id"] != disciplina_id
                and outra.get("nome", "").lower() == nome.lower()
            ):
                return None, ["Já existe uma disciplina com esse nome."]

        campos["nome"] = nome

    if professor is not None:
        campos["professor"] = professor.strip() or None

    if not campos:
        return disciplina, []

    atualizada = repo_disciplinas.atualizar(disciplina_id, **campos)

    return atualizada, []


def remover_disciplina(disciplina_id):
    disciplina = repo_disciplinas.buscar(disciplina_id)

    if disciplina is None:
        return False, ["Disciplina não encontrada."]

    # Os conteúdos dependentes pertencem à disciplina.
    repo_conteudos.remover_por_disciplina(disciplina_id)

    repo_disciplinas.remover(disciplina_id)

    return True, []