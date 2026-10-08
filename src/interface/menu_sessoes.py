"""Interface de terminal para sessões de estudo."""

from ..estudos import sessoes as dominio


def _converter_id(texto):
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
        print("[ERRO] ID inválido.")

    return id_lido


def _ler_minutos(pergunta):
    texto = input(pergunta).strip()

    if not texto.isdigit():
        print("[ERRO] Duração inválida.")
        return None

    minutos = int(texto)

    if minutos <= 0:
        print("[ERRO] A duração deve ser maior que zero.")
        return None

    return minutos


def _escolher(pergunta, opcoes):
    print(pergunta)

    for numero, opcao in enumerate(opcoes, start=1):
        print(f"  {numero} - {opcao}")

    texto = input("Opção: ").strip()

    if not texto.isdigit():
        print("[ERRO] Opção inválida.")
        return None

    numero = int(texto)

    if not 1 <= numero <= len(opcoes):
        print("[ERRO] Opção inválida.")
        return None

    return opcoes[numero - 1]


def _mostrar_erros(erros):
    print("[ERRO] Não foi possível concluir a operação:")

    for erro in erros:
        print(" -", erro)


def _mostrar_disciplinas(disciplinas):
    print("Disciplinas cadastradas:")

    for disciplina in disciplinas:
        print(
            f"  [{disciplina['id']}] "
            f"{disciplina['nome']}"
        )


def _nome_disciplina(disciplina_id, disciplinas):
    for disciplina in disciplinas:
        if disciplina["id"] == disciplina_id:
            return disciplina["nome"]

    return "Disciplina desconhecida"


def _formatar(sessao, disciplinas):
    tipo = sessao.get("tipo", "academica")

    if tipo == "pessoal":
        origem = "Pessoal"

    elif sessao.get("disciplina_id") is None:
        origem = "Acadêmica"

    else:
        origem = _nome_disciplina(
            sessao["disciplina_id"],
            disciplinas,
        )

    return (
        f"[{sessao.get('id', '?')}] "
        f"{sessao.get('assunto', '?')} | "
        f"{origem} | "
        f"{sessao.get('duracao_min', '?')} min | "
        f"{sessao.get('data', '?')}"
    )


def menu_sessoes():
    opcoes = {
        "1": adicionar_sessao,
        "2": listar_sessoes,
        "3": remover_sessao,
    }

    while True:
        print("\n------------------------")
        print("    SESSÕES DE ESTUDO")
        print("------------------------\n")

        print("1 - Registrar sessão")
        print("2 - Listar sessões")
        print("3 - Remover sessão")
        print("0 - Voltar")

        escolha = input("\nEscolha uma opção: ").strip()

        if escolha == "0":
            return

        acao = opcoes.get(escolha)

        if acao is None:
            print("\n[ERRO] Opção inválida.")
            continue

        acao()


def adicionar_sessao():
    tipo = _escolher(
        "Tipo da sessão:",
        dominio.TIPOS,
    )

    if tipo is None:
        return

    disciplinas = dominio.listar_disciplinas()
    disciplina_id = None

    if tipo == "academica":
        if disciplinas:
            _mostrar_disciplinas(disciplinas)

            vincular = _escolher(
                "Deseja vincular a sessão a uma disciplina?",
                ("sim", "nao"),
            )

            if vincular is None:
                return

            if vincular == "sim":
                disciplina_id = _ler_id(
                    "ID da disciplina: "
                )

                if disciplina_id is None:
                    return

        else:
            print(
                "[AVISO] Nenhuma disciplina cadastrada. "
                "A sessão será registrada sem disciplina."
            )

    assunto = input("Assunto estudado: ").strip()

    duracao_min = _ler_minutos(
        "Duração em minutos: "
    )

    if duracao_min is None:
        return

    data = input(
        "Data (AAAA-MM-DD): "
    ).strip()

    sessao, erros = dominio.adicionar_sessao(
        tipo,
        disciplina_id,
        assunto,
        duracao_min,
        data,
    )

    if erros:
        _mostrar_erros(erros)
        return

    print("[OK] Sessão registrada com sucesso.")
    print(
        _formatar(
            sessao,
            dominio.listar_disciplinas(),
        )
    )


def listar_sessoes():
    sessoes = dominio.listar_sessoes()

    if not sessoes:
        print("[AVISO] Nenhuma sessão registrada.")
        return

    disciplinas = dominio.listar_disciplinas()

    for sessao in sessoes:
        print(_formatar(sessao, disciplinas))


def remover_sessao():
    sessao_id = _ler_id("ID da sessão: ")

    if sessao_id is None:
        return

    sucesso, erros = dominio.remover_sessao(
        sessao_id
    )

    if erros:
        _mostrar_erros(erros)
        return

    if sucesso:
        print("[OK] Sessão removida com sucesso.")