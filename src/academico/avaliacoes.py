"""Regras de negócio relacionadas às avaliações."""

from ..persistencia import avaliacoes as repo_avaliacoes
from ..persistencia import disciplinas as repo_disciplinas

UNIDADES = (1, 2)


def _numero_valido(valor):
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def _disciplina_existe(disciplina_id):
    return repo_disciplinas.buscar(disciplina_id) is not None


def _registro_existente(disciplina_id, unidade):
    for avaliacao in repo_avaliacoes.listar():
        if (
            avaliacao.get("disciplina_id") == disciplina_id
            and avaliacao.get("unidade") == unidade
        ):
            return avaliacao

    return None


def validar_avaliacao(disciplina_id, unidade, me, principal):
    erros = []

    if not _disciplina_existe(disciplina_id):
        erros.append("Disciplina não encontrada.")

    if unidade not in UNIDADES:
        erros.append("Unidade inválida. Use 1 ou 2.")

    if not _numero_valido(me):
        erros.append("A nota da ME deve ser numérica.")
    elif not 0 <= me <= 2:
        erros.append("A nota da ME deve estar entre 0 e 2.")

    if not _numero_valido(principal):
        erros.append("A nota principal deve ser numérica.")
    elif not 0 <= principal <= 8:
        erros.append("A nota principal deve estar entre 0 e 8.")

    return erros


def registrar_avaliacao(disciplina_id, unidade, me, principal):
    erros = validar_avaliacao(
        disciplina_id,
        unidade,
        me,
        principal,
    )

    if erros:
        return None, erros

    if _registro_existente(disciplina_id, unidade) is not None:
        return None, [
            f"Já existe um registro da UP{unidade} para essa disciplina."
        ]

    avaliacao = repo_avaliacoes.adicionar(
        disciplina_id,
        f"UP{unidade}",
        unidade=unidade,
        me=me,
        principal=principal,
    )

    return avaliacao, []


def listar_avaliacoes():
    return repo_avaliacoes.listar()


def listar_por_disciplina(disciplina_id):
    return [
        avaliacao
        for avaliacao in repo_avaliacoes.listar()
        if avaliacao.get("disciplina_id") == disciplina_id
    ]


def buscar_avaliacao(avaliacao_id):
    return repo_avaliacoes.buscar(avaliacao_id)


def atualizar_avaliacao(avaliacao_id, me, principal):
    avaliacao = repo_avaliacoes.buscar(avaliacao_id)

    if avaliacao is None:
        return None, ["Avaliação não encontrada."]

    erros = validar_avaliacao(
        avaliacao["disciplina_id"],
        avaliacao["unidade"],
        me,
        principal,
    )

    if erros:
        return None, erros

    atualizada = repo_avaliacoes.atualizar(
        avaliacao_id,
        me=me,
        principal=principal,
    )

    return atualizada, []


def remover_avaliacao(avaliacao_id):
    if repo_avaliacoes.buscar(avaliacao_id) is None:
        return False, ["Avaliação não encontrada."]

    repo_avaliacoes.remover(avaliacao_id)

    return True, []


def calcular_nota_unidade(avaliacao):
    return avaliacao.get("me", 0) + avaliacao.get("principal", 0)

def calcular_media_geral(disciplina_id):
    avaliacoes = listar_por_disciplina(disciplina_id)

    up1 = None
    up2 = None

    for avaliacao in avaliacoes:
        if avaliacao.get("unidade") == 1:
            up1 = calcular_nota_unidade(avaliacao)

        elif avaliacao.get("unidade") == 2:
            up2 = calcular_nota_unidade(avaliacao)

    if up1 is None or up2 is None:
        return None

    return (up1 + up2) / 2