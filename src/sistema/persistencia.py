import json
import os


RAIZ_PROJETO = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

CAMINHO_DADOS = os.path.join(
    RAIZ_PROJETO,
    "data",
    "taskuni.json"
)


def criar_estrutura_inicial():
    """Cria e retorna a estrutura inicial de dados do TASKUNI."""
    return {
        "disciplinas": [],
        "conteudos": [],
        "tarefas": [],
        "avaliacoes": [],
        "sessoes_estudo": [],
        "metas": []
    }


def validar_estrutura_dados(dados):
    """Verifica se os dados possuem a estrutura mínima esperada."""

    if not isinstance(dados, dict):
        return False

    estrutura_padrao = criar_estrutura_inicial()

    for chave in estrutura_padrao:
        if chave not in dados:
            return False

        if not isinstance(dados[chave], list):
            return False

    return True


def garantir_diretorio_dados():
    """Garante que o diretório utilizado para armazenar os dados exista."""

    diretorio = os.path.dirname(CAMINHO_DADOS)

    if not os.path.exists(diretorio):
        os.makedirs(diretorio)


def salvar_dados(dados):
    """Salva os dados atuais do TASKUNI no arquivo JSON."""

    if not validar_estrutura_dados(dados):
        raise ValueError("Estrutura de dados inválida.")

    garantir_diretorio_dados()

    with open(CAMINHO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(
            dados,
            arquivo,
            indent=4,
            ensure_ascii=False
        )


def carregar_dados():
    """Carrega os dados salvos ou cria a estrutura inicial."""

    garantir_diretorio_dados()

    if not os.path.exists(CAMINHO_DADOS):
        dados = criar_estrutura_inicial()
        salvar_dados(dados)
        return dados

    try:
        with open(CAMINHO_DADOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

    except json.JSONDecodeError:
        dados = criar_estrutura_inicial()
        salvar_dados(dados)
        return dados

    if not validar_estrutura_dados(dados):
        dados = criar_estrutura_inicial()
        salvar_dados(dados)

    return dados