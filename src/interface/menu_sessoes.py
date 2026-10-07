"""Interface de terminal para sessões de estudos."""

from ..estudos import sessoes as dominio


def _ler_id(pergunta):
    texto = input(pergunta).strip()

    if not texto.isdigit():
        print("ID inválido.")
        return None

    return int(texto)


def _ler_horas(pergunta):
    texto = input(pergunta).strip().replace(",", ".")

    try:
        return float(texto)
    except ValueError:
        print("Duração inválida.")
        return None


def _mostrar_erros(erros):
    for erro in erros:
        print(" -", erro)


def menu_sessoes():
    opcoes = {
        "1": adicionar_sessao,
        "2": listar_sessoes,
        "3": remover_sessao,
    }

    while True:
        print("\n--- Sessões de Estudo ---")
        print("1 - Adicionar")
        print("2 - Listar")
        print("3 - Remover")
        print("0 - Voltar")

        escolha = input("Escolha uma opção: ").strip()

        if escolha == "0":
            return

        acao = opcoes.get(escolha)

        if acao is None:
            print("Opção inválida.")
            continue

        acao()


def adicionar_sessao():
    disciplina_id = _ler_id("ID da disciplina: ")

    if disciplina_id is None:
        return

    assunto = input("Assunto estudado: ").strip()
    horas = _ler_horas("Duração em horas: ")

    if horas is None:
        return

    data = input("Data (AAAA-MM-DD): ").strip()

    sessao, erros = dominio.adicionar_sessao(
        disciplina_id,
        assunto,
        horas,
        data,
    )

    if erros:
        _mostrar_erros(erros)
        return

    print("Sessão registrada:", sessao)


def listar_sessoes():
    sessoes = dominio.listar_sessoes()

    if not sessoes:
        print("Nenhuma sessão registrada.")
        return

    for sessao in sessoes:
        print(sessao)


def remover_sessao():
    sessao_id = _ler_id("ID da sessão: ")

    if sessao_id is None:
        return

    sucesso, erros = dominio.remover_sessao(sessao_id)

    if erros:
        _mostrar_erros(erros)
        return

    if sucesso:
        print("Sessão removida.")
