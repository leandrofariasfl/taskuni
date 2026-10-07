"""Interface de terminal para disciplinas."""

from ..academico import disciplinas as dominio


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


def menu_disciplinas():
    opcoes = {
        "1": adicionar_disciplina,
        "2": listar_disciplinas,
        "3": atualizar_disciplina,
        "4": remover_disciplina,
    }

    while True:
        print("\n------------------------")
        print("      DISCIPLINAS")
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


def adicionar_disciplina():
    nome = input("Nome da disciplina: ").strip()
    professor = input("Professor (opcional): ").strip()

    disciplina, erros = dominio.adicionar_disciplina(
        nome,
        professor,
    )

    if erros:
        _mostrar_erros(erros)
        return

    print("[OK] Disciplina adicionada com sucesso.")


def listar_disciplinas():
    disciplinas = dominio.listar_disciplinas()

    if not disciplinas:
        print("[AVISO] Nenhuma disciplina cadastrada.")
        return

    for disciplina in disciplinas:
        professor = disciplina.get("professor") or "Não informado"

        print(
            f"[{disciplina['id']}] "
            f"{disciplina['nome']} | "
            f"Professor: {professor}"
        )


def atualizar_disciplina():
    disciplina_id = _ler_id("ID da disciplina: ")

    if disciplina_id is None:
        return

    nome = input("Novo nome (Enter mantém): ").strip()

    disciplina, erros = dominio.atualizar_disciplina(
        disciplina_id,
        nome=nome if nome else None,
    )

    if erros:
        _mostrar_erros(erros)
        return

    print("[OK] Disciplina atualizada com sucesso.")


def remover_disciplina():
    disciplina_id = _ler_id("ID da disciplina: ")

    if disciplina_id is None:
        return

    sucesso, erros = dominio.remover_disciplina(disciplina_id)

    if erros:
        _mostrar_erros(erros)
        return

    if sucesso:
        print("[OK] Disciplina removida com sucesso.")