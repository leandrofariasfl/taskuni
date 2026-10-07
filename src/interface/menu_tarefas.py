"""Menu de tarefas: entradas, mensagens e ligação entre domínio e persistência."""
from ..sistema import analise_tarefas as prioridade
from ..academico import tarefas as dominio
from ..persistencia import disciplinas as repo_disciplinas
from ..persistencia import tarefas as repo_tarefas

ROTULOS_FAIXA = {
    "alta": "ALTA atenção",
    "media": "MÉDIA atenção",
    "baixa": "BAIXA atenção",
}


def menu_tarefas():
    opcoes = {
        "1": adicionar_tarefa,
        "2": listar_tarefas,
        "3": mostrar_prioridades,
        "4": mostrar_alertas,
        "5": editar_tarefa,
        "6": concluir_tarefa,
        "7": reabrir_tarefa,
    }
    while True:
        print("\n--- Tarefas ---")
        print("1 - Adicionar")
        print("2 - Listar")
        print("3 - Prioridades")
        print("4 - Alertas (atrasadas e próximas)")
        print("5 - Editar")
        print("6 - Concluir")
        print("7 - Reabrir")
        print("0 - Voltar")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == "0":
            return

        acao = opcoes.get(escolha)
        if acao is None:
            print("Opção inválida.")
            continue
        acao()


def _converter_id(texto):
    """Converte o texto em ID (inteiro positivo); None se for inválido."""
    try:
        numero = int(texto)
    except ValueError:
        return None
    if numero <= 0:
        return None
    return numero


def _ler_id(pergunta):
    id_lido = _converter_id(input(pergunta).strip())
    if id_lido is None:
        print("ID inválido.")
    return id_lido


def _escolher(pergunta, opcoes):
    """Mostra opções numeradas; devolve a escolhida ou None se inválida ou vazia."""
    print(pergunta)
    for numero, opcao in enumerate(opcoes, start=1):
        print(f"  {numero} - {opcao}")
    texto = input("Opção: ").strip()
    if texto == "":
        return None
    if texto.isdigit() and 1 <= int(texto) <= len(opcoes):
        return opcoes[int(texto) - 1]
    print("Opção inválida.")
    return None


def _mostrar_erros(erros):
    print("Não foi possível concluir a operação:")
    for erro in erros:
        print(" -", erro)


def _mostrar_disciplinas(disciplinas):
    print("Disciplinas cadastradas:")
    for disciplina in disciplinas:
        print(f"  [{disciplina['id']}] {disciplina['nome']}")


def _nome_disciplina(disciplina_id, disciplinas):
    for disciplina in disciplinas:
        if disciplina["id"] == disciplina_id:
            return disciplina["nome"]
    return "disciplina desconhecida"


def _formatar(tarefa, disciplinas):
    if tarefa.get("tipo") == "pessoal":
        origem = "pessoal"
    elif tarefa.get("disciplina_id") is None:
        origem = "acadêmica"
    else:
        origem = _nome_disciplina(tarefa["disciplina_id"], disciplinas)

    texto = (
        f"[{tarefa.get('id', '?')}] {tarefa.get('titulo', '?')} | {origem} | "
        f"prazo {tarefa.get('prazo', '?')} | "
        f"importância {tarefa.get('importancia', '?')} | "
        f"{tarefa.get('status', '?')}"
    )
    if prioridade.esta_atrasada(tarefa):
        texto += "  ** ATRASADA **"
    return texto


def _pedir_tarefa():
    """Pergunta o ID e devolve a tarefa correspondente, ou None."""
    id_tarefa = _ler_id("ID da tarefa: ")
    if id_tarefa is None:
        return None
    tarefa = repo_tarefas.buscar(id_tarefa)
    if tarefa is None:
        print("Tarefa não encontrada.")
    return tarefa


def adicionar_tarefa():
    disciplinas = repo_disciplinas.listar()

    titulo = input("Título: ").strip()
    descricao = input("Descrição: ").strip()

    tipo = _escolher("Tipo da tarefa:", dominio.TIPOS)
    if tipo is None:
        print("Cadastro cancelado.")
        return

    disciplina_id = None
    if tipo == "academica":
        if disciplinas:
            _mostrar_disciplinas(disciplinas)
            
            vincular = _escolher(
            "Deseja vincular a tarefa a uma disciplina?",
            ("sim", "nao"),
            )

            if vincular is None:
                print("Cadastro cancelado.")
                return

            if vincular == "sim":
                disciplina_id = _ler_id("ID da disciplina: ")
                if disciplina_id is None:
                    return
        else:
            print("Nenhuma disciplina cadastrada. A tarefa será criada sem disciplina.")

    prazo = input("Prazo (AAAA-MM-DD): ").strip()

    importancia = _escolher("Importância:", dominio.IMPORTANCIAS)
    if importancia is None:
        print("Cadastro cancelado.")
        return

    tarefa, erros = dominio.criar_tarefa(
        titulo, descricao, tipo, disciplina_id, prazo, importancia, disciplinas
    )
    if erros:
        _mostrar_erros(erros)
        return

    salva = repo_tarefas.adicionar(**tarefa)
    print("Tarefa adicionada:", _formatar(salva, disciplinas))


def listar_tarefas():
    tarefas = repo_tarefas.listar()
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return

    filtro = _escolher("Mostrar quais tarefas?", ("todas", "pendente", "concluida"))
    if filtro is None:
        return
    status = None if filtro == "todas" else filtro

    encontradas = dominio.filtrar_tarefas(tarefas, status=status)
    if not encontradas:
        print("Nenhuma tarefa encontrada com esse filtro.")
        return

    disciplinas = repo_disciplinas.listar()
    for tarefa in dominio.ordenar_por_prazo(encontradas):
        print(_formatar(tarefa, disciplinas))


def mostrar_prioridades():
    itens = prioridade.ordenar_por_prioridade(repo_tarefas.listar())
    if not itens:
        print("Nenhuma tarefa pendente.")
        return

    disciplinas = repo_disciplinas.listar()
    for tarefa, info in itens:
        rotulo = ROTULOS_FAIXA[info["faixa"]]
        print(f"[{rotulo} | {info['pontuacao']} pts] {_formatar(tarefa, disciplinas)}")


def mostrar_alertas():
    tarefas = repo_tarefas.listar()
    disciplinas = repo_disciplinas.listar()

    atrasadas = prioridade.listar_atrasadas(tarefas)
    proximas = prioridade.listar_proximas(tarefas)

    print("\nTarefas atrasadas:")
    if atrasadas:
        for tarefa in dominio.ordenar_por_prazo(atrasadas):
            print(" ", _formatar(tarefa, disciplinas))
    else:
        print("  Nenhuma.")

    print("\nTarefas próximas (hoje até 7 dias):")
    if proximas:
        for tarefa in dominio.ordenar_por_prazo(proximas):
            print(" ", _formatar(tarefa, disciplinas))
    else:
        print("  Nenhuma.")


def editar_tarefa():
    tarefa = _pedir_tarefa()
    if tarefa is None:
        return

    disciplinas = repo_disciplinas.listar()
    print("Deixe em branco para manter o valor atual.")
    alteracoes = {}

    titulo = input(f"Título [{tarefa.get('titulo')}]: ").strip()
    if titulo:
        alteracoes["titulo"] = titulo

    descricao = input(f"Descrição [{tarefa.get('descricao')}]: ").strip()
    if descricao:
        alteracoes["descricao"] = descricao

    prazo = input(f"Prazo [{tarefa.get('prazo')}] (AAAA-MM-DD): ").strip()
    if prazo:
        alteracoes["prazo"] = prazo

    importancia = _escolher(
        f"Importância [{tarefa.get('importancia')}] (Enter mantém):",
        dominio.IMPORTANCIAS,
    )
    if importancia is not None:
        alteracoes["importancia"] = importancia

    if tarefa.get("tipo") == "academica":
        if disciplinas:
            _mostrar_disciplinas(disciplinas)

            print("Disciplina:")
            print("  Enter - manter atual")
            print("  0 - remover vínculo")
            print("  ID - vincular/trocar disciplina")

            texto_id = input(
                f"Disciplina atual [{tarefa.get('disciplina_id')}]: "
            ).strip()

            if texto_id == "0":
                alteracoes["disciplina_id"] = None

            elif texto_id:
                novo_id = _converter_id(texto_id)

                if novo_id is None:
                    print("ID inválido.")
                    return

                alteracoes["disciplina_id"] = novo_id

        else:
            print("Nenhuma disciplina cadastrada.")

    if not alteracoes:
        print("Nada foi alterado.")
        return

    campos, erros = dominio.editar_tarefa(tarefa, alteracoes, disciplinas)
    if erros:
        _mostrar_erros(erros)
        return

    atualizada = repo_tarefas.atualizar(tarefa["id"], **campos)
    print("Tarefa atualizada:", _formatar(atualizada, disciplinas))


def _mudar_status(novo_status, mensagem_sucesso):
    tarefa = _pedir_tarefa()
    if tarefa is None:
        return

    campos, erros = dominio.alterar_status(tarefa, novo_status)
    if erros:
        _mostrar_erros(erros)
        return

    atualizada = repo_tarefas.atualizar(tarefa["id"], **campos)
    print(mensagem_sucesso, _formatar(atualizada, repo_disciplinas.listar()))


def concluir_tarefa():
    _mudar_status("concluida", "Tarefa concluída:")


def reabrir_tarefa():
    _mudar_status("pendente", "Tarefa reaberta:")