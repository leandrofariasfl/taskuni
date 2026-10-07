"""Regras das tarefas: validação, criação, edição, status e consultas.

As operações que podem falhar devolvem (resultado, erros).
"""
from datetime import datetime

TIPOS = ("academica", "pessoal")
IMPORTANCIAS = ("baixa", "media", "alta")
STATUS = ("pendente", "concluida")
CAMPOS_EDITAVEIS = (
    "titulo",
    "descricao",
    "tipo",
    "disciplina_id",
    "prazo",
    "importancia",
)


def texto_para_data(texto):
    """Converte 'AAAA-MM-DD' em date; devolve None se o texto for inválido."""
    if not isinstance(texto, str):
        return None
    try:
        data = datetime.strptime(texto, "%Y-%m-%d").date()
    except ValueError:
        return None
    # strptime aceita "2026-1-5"; o formato exigido tem zeros à esquerda
    if data.strftime("%Y-%m-%d") != texto:
        return None
    return data


def _texto_preenchido(valor):
    return isinstance(valor, str) and valor.strip() != ""


def _id_valido(valor):
    # bool é subtipo de int, por isso é excluído
    return isinstance(valor, int) and not isinstance(valor, bool) and valor > 0


def _disciplina_existe(disciplina_id, disciplinas):
    for disciplina in disciplinas:
        if disciplina.get("id") == disciplina_id:
            return True
    return False


def _normalizar(tarefa):
    """Devolve uma cópia da tarefa com os textos limpos."""
    nova = dict(tarefa)
    for campo in ("titulo", "descricao", "prazo"):
        if isinstance(nova.get(campo), str):
            nova[campo] = nova[campo].strip()
    for campo in ("tipo", "importancia", "status"):
        if isinstance(nova.get(campo), str):
            nova[campo] = nova[campo].strip().lower()
    return nova


def validar_tarefa(tarefa, disciplinas):
    """Devolve a lista de erros da tarefa (lista vazia se for válida)."""
    erros = []

    if not _texto_preenchido(tarefa.get("titulo")):
        erros.append("O título é obrigatório.")

    if not _texto_preenchido(tarefa.get("descricao")):
        erros.append("A descrição é obrigatória.")

    tipo = tarefa.get("tipo")
    disciplina_id = tarefa.get("disciplina_id")

    if tipo not in TIPOS:
        erros.append("Tipo inválido. Use: " + ", ".join(TIPOS) + ".")
    elif tipo == "pessoal":
        if disciplina_id is not None:
            erros.append("Tarefa pessoal não pode ter disciplina.")
    else:
        if disciplina_id is not None:
            if not _id_valido(disciplina_id):
                erros.append("ID de disciplina inválido.")
            elif not _disciplina_existe(disciplina_id, disciplinas):
                erros.append(f"A disciplina {disciplina_id} não existe.")

    if texto_para_data(tarefa.get("prazo")) is None:
        erros.append("Prazo inválido. Use o formato AAAA-MM-DD (ex.: 2026-10-05).")

    if tarefa.get("importancia") not in IMPORTANCIAS:
        erros.append("Importância inválida. Use: " + ", ".join(IMPORTANCIAS) + ".")

    if tarefa.get("status") not in STATUS:
        erros.append("Status inválido. Use: " + ", ".join(STATUS) + ".")

    return erros


def criar_tarefa(titulo, descricao, tipo, disciplina_id, prazo, importancia, disciplinas):
    """Monta uma tarefa pendente, ainda sem id (o id é gerado ao salvar)."""
    tarefa = _normalizar({
        "titulo": titulo,
        "descricao": descricao,
        "tipo": tipo,
        "disciplina_id": disciplina_id,
        "prazo": prazo,
        "importancia": importancia,
        "status": "pendente",
    })

    erros = validar_tarefa(tarefa, disciplinas)
    if erros:
        return None, erros
    return tarefa, []


def editar_tarefa(tarefa, alteracoes, disciplinas):
    """Valida as alterações sem modificar a tarefa original.

    Devolve apenas os campos a serem gravados.
    """
    erros = []
    for campo in alteracoes:
        if campo not in CAMPOS_EDITAVEIS:
            erros.append(f"O campo '{campo}' não pode ser editado.")
    if erros:
        return None, erros

    # valida a tarefa já com as alterações, para manter as regras entre campos
    nova = dict(tarefa)
    nova.update(alteracoes)
    nova = _normalizar(nova)

    erros = validar_tarefa(nova, disciplinas)
    if erros:
        return None, erros

    campos = {}
    for campo in alteracoes:
        campos[campo] = nova[campo]
    return campos, []


def alterar_status(tarefa, novo_status):
    """Valida a troca de status (concluir ou reabrir)."""
    if isinstance(novo_status, str):
        novo_status = novo_status.strip().lower()

    if novo_status not in STATUS:
        return None, ["Status inválido. Use: " + ", ".join(STATUS) + "."]

    if tarefa.get("status") == novo_status:
        return None, [f"A tarefa já está com o status '{novo_status}'."]

    return {"status": novo_status}, []


def filtrar_tarefas(tarefas, status=None, tipo=None, disciplina_id=None):
    """Mantém só as tarefas que atendem aos filtros informados (None ignora)."""
    resultado = []
    for tarefa in tarefas:
        if status is not None and tarefa.get("status") != status:
            continue
        if tipo is not None and tarefa.get("tipo") != tipo:
            continue
        if disciplina_id is not None and tarefa.get("disciplina_id") != disciplina_id:
            continue
        resultado.append(tarefa)
    return resultado


def _chave_prazo(tarefa):
    return (tarefa.get("prazo", ""), tarefa.get("id", 0))


def ordenar_por_prazo(tarefas):
    """Ordena do prazo mais próximo para o mais distante."""
    return sorted(tarefas, key=_chave_prazo)