"""Menu principal do TASKUNI."""

from .menu_disciplinas import menu_disciplinas
from .menu_conteudos import menu_conteudos
from .menu_tarefas import menu_tarefas
from .menu_sessoes import menu_sessoes


def executar():
    opcoes = {
        "1": menu_disciplinas,
        "2": menu_conteudos,
        "3": menu_tarefas,
        "4": menu_sessoes,
    }

    while True:
        print("\n=== TASKUNI ===")
        print("1 - Disciplinas")
        print("2 - Conteúdos")
        print("3 - Tarefas")
        print("4 - Registrar Sessões de estudo")
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