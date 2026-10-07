"""Interface de terminal para conteúdos."""

from ..academico import conteudos as dominio


def _ler_id(pergunta):
    texto = input(pergunta).strip()

    if not texto.isdigit():
        print("ID inválido.")
        return None

    return int(texto)


def _mostrar_erros(erros):
    for erro in erros:
        print(" -", erro)


def menu_conteudos():
    opcoes = {
        "1": adicionar_conteudo,
        "2": listar_conteudos,
        "3": atualizar_conteudo,
        "4": remover_conteudo,
    }

    while True:
        print("\n--- Conteúdos ---")
        print("1 - Adicionar")
        print("2 - Listar")
        print("3 - Atualizar")
        print("4 - Remover")
        print("0 - Voltar")

        escolha = input("Escolha uma opção: ").strip()

        if escolha == "0":
            return

        acao = opcoes.get(escolha)

        if acao is None:
            print("Opção inválida.")
            continue

        acao()


def adicionar_conteudo():
    disciplina_id = _ler_id("ID da disciplina: ")

    if disciplina_id is None:
        return

    titulo = input("Título do conteúdo: ").strip()

    conteudo, erros = dominio.adicionar_conteudo(
        disciplina_id,
        titulo,
    )

    if erros:
        _mostrar_erros(erros)
        return

    print("Conteúdo adicionado:", conteudo)


def listar_conteudos():
    conteudos = dominio.listar_conteudos()

    if not conteudos:
        print("Nenhum conteúdo cadastrado.")
        return

    for conteudo in conteudos:
        print(conteudo)


def atualizar_conteudo():
    conteudo_id = _ler_id("ID do conteúdo: ")

    if conteudo_id is None:
        return

    titulo = input("Novo título: ").strip()

    conteudo, erros = dominio.atualizar_conteudo(
        conteudo_id,
        titulo,
    )

    if erros:
        _mostrar_erros(erros)
        return

    print("Conteúdo atualizado:", conteudo)


def remover_conteudo():
    conteudo_id = _ler_id("ID do conteúdo: ")

    if conteudo_id is None:
        return

    sucesso, erros = dominio.remover_conteudo(conteudo_id)

    if erros:
        _mostrar_erros(erros)
        return

    if sucesso:
        print("Conteúdo removido.")