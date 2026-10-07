
def menu_disciplinas():
    opcoes = {
        "1": adicionar_disciplina,
        "2": listar_disciplinas,
        "3": atualizar_disciplina,
        "4": remover_disciplina,
    }
    while True:
        print("\n--- Disciplinas ---")
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


def adicionar_disciplina():
    nome = input("Nome da disciplina: ").strip()
    professor = input("Professor (opcional): ").strip()
    item = disp.adicionar(nome, professor=professor or None)
    print("Disciplina adicionada:", item)


def listar_disciplinas():
    disciplinas = disp.listar()
    if not disciplinas:
        print("Nenhuma disciplina cadastrada.")
        return
    for d in disciplinas:
        print(d)


def atualizar_disciplina():
    id_texto = input("ID da disciplina: ").strip()
    if not id_texto.isdigit():
        print("ID inválido.")
        return

    nome = input("Novo nome (deixe vazio para manter): ").strip()
    campos = {}
    if nome:
        campos["nome"] = nome

    item = disp.atualizar(int(id_texto), **campos)
    if item is None:
        print("Disciplina não encontrada.")
    else:
        print("Disciplina atualizada:", item)


def remover_disciplina():
    id_texto = input("ID da disciplina: ").strip()
    if not id_texto.isdigit():
        print("ID inválido.")
        return

    sucesso = disp.remover(int(id_texto))
    print("Disciplina removida." if sucesso else "Disciplina não encontrada.")
