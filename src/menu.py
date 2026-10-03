"""Interface de terminal do TASKUNI: menus, entradas e mensagens.

Liga-se diretamente a persistencia.disciplinas/conteudos (únicos módulos
de domínio com lógica implementada até agora). Quando academico.disciplinas
e academico.conteudos existirem, os imports abaixo devem passar a apontar
para eles.
"""
from .persistencia import disciplinas as disp
from .persistencia import conteudos as cont


def executar():
    opcoes = {
        "1": menu_disciplinas,
        "2": menu_conteudos,
    }
    while True:
        print("\n=== TASKUNI ===")
        print("1 - Disciplinas")
        print("2 - Conteúdos")
        print("0 - Sair")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == "0":
            print("Até logo!")
            break

        acao = opcoes.get(escolha)
        if acao is None:
            print("Opção inválida.")
            continue
        acao()


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
