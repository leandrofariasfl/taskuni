
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
    disciplina_id_texto = input("ID da disciplina: ").strip()
    if not disciplina_id_texto.isdigit():
        print("ID inválido.")
        return

    titulo = input("Título do conteúdo: ").strip()
    item = cont.adicionar(int(disciplina_id_texto), titulo)
    print("Conteúdo adicionado:", item)


def listar_conteudos():
    conteudos = cont.listar()
    if not conteudos:
        print("Nenhum conteúdo cadastrado.")
        return
    for c in conteudos:
        print(c)


def atualizar_conteudo():
    id_texto = input("ID do conteúdo: ").strip()
    if not id_texto.isdigit():
        print("ID inválido.")
        return

    titulo = input("Novo título (deixe vazio para manter): ").strip()
    campos = {}
    if titulo:
        campos["titulo"] = titulo

    item = cont.atualizar(int(id_texto), **campos)
    if item is None:
        print("Conteúdo não encontrado.")
    else:
        print("Conteúdo atualizado:", item)


def remover_conteudo():
    id_texto = input("ID do conteúdo: ").strip()
    if not id_texto.isdigit():
        print("ID inválido.")
        return

    sucesso = cont.remover(int(id_texto))
    print("Conteúdo removido." if sucesso else "Conteúdo não encontrado.")
