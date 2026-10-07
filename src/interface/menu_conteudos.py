"""Interface de terminal para conteúdos."""

from ..academico import conteudos as dominio
from ..academico import disciplinas as dominio_disciplinas


def _ler_id(pergunta):
    texto = input(pergunta).strip()

    if not texto.isdigit():
        print("[ERRO] ID inválido.")
        return None

    return int(texto)


def _mostrar_erros(erros):
    print("[ERRO] Não foi possível concluir a operação:")

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
        print("\n------------------------")
        print("        CONTEÚDOS")
        print("------------------------\n")

        print("1 - Adicionar")
        print("2 - Listar")
        print("3 - Atualizar")
        print("4 - Remover")
        print("0 - Voltar")

        escolha = input("\nEscolha uma opção: ").strip()

        if escolha == "0":
            return

        acao = opcoes.get(escolha)

        if acao is None:
            print("\n[ERRO] Opção inválida.")
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

    print("[OK] Conteúdo adicionado com sucesso.")


def listar_conteudos():
    conteudos = dominio.listar_conteudos()

    if not conteudos:
        print("[AVISO] Nenhum conteúdo cadastrado.")
        return

    for conteudo in conteudos:
        nome_disciplina = _nome_disciplina(
            conteudo["disciplina_id"]
        )

        print(
            f"[{conteudo['id']}] "
            f"{conteudo['titulo']} | "
            f"Disciplina: {nome_disciplina}"
        )


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

    print("[OK] Conteúdo atualizado com sucesso.")


def remover_conteudo():
    conteudo_id = _ler_id("ID do conteúdo: ")

    if conteudo_id is None:
        return

    sucesso, erros = dominio.remover_conteudo(conteudo_id)

    if erros:
        _mostrar_erros(erros)
        return

    if sucesso:
        print("[OK] Conteúdo removido com sucesso.")

def _nome_disciplina(disciplina_id):
    disciplina = dominio_disciplinas.buscar_disciplina(disciplina_id)

    if disciplina is None:
        return "Disciplina desconhecida"

    return disciplina["nome"]