"""Prioridade, atraso e proximidade de prazo das tarefas pendentes.

Prioridade = pontos de importância + pontos de urgência (PROJECT_CONTEXT.md, seção 8).
Nada é salvo: tudo é calculado a partir dos dados. O parâmetro `hoje` existe
para testes; quando omitido, usa a data do computador.
"""
from datetime import date

from .tarefas import texto_para_data

PONTOS_IMPORTANCIA = {"baixa": 1, "media": 2, "alta": 3}
DIAS_PROXIMA = 7


def _data_de_hoje(hoje):
    return hoje if hoje is not None else date.today()


def dias_ate_prazo(tarefa, hoje=None):
    """Dias até o prazo (negativo se já venceu); None se o prazo for inválido."""
    prazo = texto_para_data(tarefa.get("prazo"))
    if prazo is None:
        return None
    return (prazo - _data_de_hoje(hoje)).days


def esta_atrasada(tarefa, hoje=None):
    if tarefa.get("status") != "pendente":
        return False
    dias = dias_ate_prazo(tarefa, hoje)
    return dias is not None and dias < 0


def esta_proxima(tarefa, hoje=None):
    """Pendente e com prazo entre hoje e os próximos 7 dias, inclusive."""
    if tarefa.get("status") != "pendente":
        return False
    dias = dias_ate_prazo(tarefa, hoje)
    return dias is not None and 0 <= dias <= DIAS_PROXIMA


def calcular_urgencia(dias):
    if dias < 0:
        return 5
    if dias <= 1:
        return 4
    if dias <= 3:
        return 3
    if dias <= DIAS_PROXIMA:
        return 2
    return 1


def classificar_pontuacao(pontuacao):
    if pontuacao >= 6:
        return "alta"
    if pontuacao >= 4:
        return "media"
    return "baixa"


def calcular_prioridade(tarefa, hoje=None):
    """Devolve os pontos e a faixa da tarefa, ou None se não for pendente."""
    if tarefa.get("status") != "pendente":
        return None

    dias = dias_ate_prazo(tarefa, hoje)
    pontos_importancia = PONTOS_IMPORTANCIA.get(tarefa.get("importancia"))
    if dias is None or pontos_importancia is None:
        return None

    urgencia = calcular_urgencia(dias)
    pontuacao = pontos_importancia + urgencia
    return {
        "importancia": pontos_importancia,
        "urgencia": urgencia,
        "pontuacao": pontuacao,
        "faixa": classificar_pontuacao(pontuacao),
    }


def _chave_prioridade(item):
    # maior pontuação primeiro; em empate, prazo mais próximo
    tarefa, prioridade = item
    return (-prioridade["pontuacao"], tarefa["prazo"], tarefa.get("id", 0))


def ordenar_por_prioridade(tarefas, hoje=None):
    """Devolve pares (tarefa, prioridade) das pendentes, da mais urgente à menos."""
    itens = []
    for tarefa in tarefas:
        prioridade = calcular_prioridade(tarefa, hoje)
        if prioridade is not None:
            itens.append((tarefa, prioridade))
    itens.sort(key=_chave_prioridade)
    return itens


def listar_atrasadas(tarefas, hoje=None):
    return [t for t in tarefas if esta_atrasada(t, hoje)]


def listar_proximas(tarefas, hoje=None):
    return [t for t in tarefas if esta_proxima(t, hoje)]