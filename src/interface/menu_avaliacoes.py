"""Interface de terminal para avaliações."""

from ..academico import avaliacoes as dominio
from ..academico import disciplinas as dominio_disciplinas


def _ler_id(pergunta):
    texto = input(pergunta).strip()

    if not texto.isdigit():
        print("[ERRO] ID inválido.")
        return None

    return int(texto)


def _ler_nota(pergunta):
    texto = input(pergunta).strip().replace(",", ".")

    try:
        return float(texto)
    except ValueError:
        print("[ERRO] Nota inválida.")
        return None


def _mostrar_erros(erros):
    print("[ERRO] Não foi possível concluir a operação:")

    for erro in erros:
        print(" -", erro)


def _mostrar_disciplinas():
    disciplinas = dominio_disciplinas.listar_disciplinas()

    if not disciplinas:
        print("[AVISO] Nenhuma disciplina cadastrada.")
        return []

    print("Disciplinas cadastradas:")

    for disciplina in disciplinas:
        print(f"  [{disciplina['id']}] {disciplina['nome']}")

    return disciplinas


def _nome_disciplina(disciplina_id):
    disciplina = dominio_disciplinas.buscar_disciplina(disciplina_id)

    if disciplina is None:
        return "Disciplina desconhecida"

    return disciplina["nome"]


def _formatar(avaliacao):
    total = dominio.calcular_nota_unidade(avaliacao)

    return (
        f"[{avaliacao['id']}] "
        f"{_nome_disciplina(avaliacao['disciplina_id'])} | "
        f"UP{avaliacao['unidade']} | "
        f"ME: {avaliacao['me']:.1f}/2 | "
        f"Principal: {avaliacao['principal']:.1f}/8 | "
        f"Total: {total:.1f}/10"
    )


def menu_avaliacoes():
    opcoes = {
        "1": registrar_avaliacao,
        "2": listar_avaliacoes,
        "3": atualizar_avaliacao,
        "4": remover_avaliacao,
        "5": mostrar_media,
    }

    while True:
        print("\n------------------------")
        print("       AVALIAÇÕES")
        print("------------------------\n")

        print("1 - Registrar notas")
        print("2 - Listar notas")
        print("3 - Atualizar notas")
        print("4 - Remover registro")
        print("5 - Ver média da disciplina")
        print("0 - Voltar")

        escolha = input("\nEscolha uma opção: ").strip()

        if escolha == "0":
            return

        acao = opcoes.get(escolha)

        if acao is None:
            print("\n[ERRO] Opção inválida.")
            continue

        acao()


def registrar_avaliacao():
    disciplinas = _mostrar_disciplinas()

    if not disciplinas:
        return

    disciplina_id = _ler_id("ID da disciplina: ")

    if disciplina_id is None:
        return

    unidade = _ler_id("Unidade (1 ou 2): ")

    if unidade is None:
        return

    me = _ler_nota("Nota da ME (0 a 2): ")

    if me is None:
        return

    principal = _ler_nota("Nota principal (0 a 8): ")

    if principal is None:
        return

    avaliacao, erros = dominio.registrar_avaliacao(
        disciplina_id,
        unidade,
        me,
        principal,
    )

    if erros:
        _mostrar_erros(erros)
        return

    print("[OK] Avaliação registrada com sucesso.")
    print(_formatar(avaliacao))


def listar_avaliacoes():
    avaliacoes = dominio.listar_avaliacoes()

    if not avaliacoes:
        print("[AVISO] Nenhuma avaliação registrada.")
        return

    for avaliacao in avaliacoes:
        print(_formatar(avaliacao))


def atualizar_avaliacao():
    avaliacao_id = _ler_id("ID da avaliação: ")

    if avaliacao_id is None:
        return

    avaliacao = dominio.buscar_avaliacao(avaliacao_id)

    if avaliacao is None:
        print("[ERRO] Avaliação não encontrada.")
        return

    print(_formatar(avaliacao))

    me = _ler_nota("Nova nota da ME (0 a 2): ")

    if me is None:
        return

    principal = _ler_nota("Nova nota principal (0 a 8): ")

    if principal is None:
        return

    atualizada, erros = dominio.atualizar_avaliacao(
        avaliacao_id,
        me,
        principal,
    )

    if erros:
        _mostrar_erros(erros)
        return

    print("[OK] Avaliação atualizada com sucesso.")
    print(_formatar(atualizada))


def remover_avaliacao():
    avaliacao_id = _ler_id("ID da avaliação: ")

    if avaliacao_id is None:
        return

    sucesso, erros = dominio.remover_avaliacao(avaliacao_id)

    if erros:
        _mostrar_erros(erros)
        return

    if sucesso:
        print("[OK] Avaliação removida com sucesso.")


def mostrar_media():
    disciplinas = _mostrar_disciplinas()

    if not disciplinas:
        return

    disciplina_id = _ler_id("ID da disciplina: ")

    if disciplina_id is None:
        return

    media = dominio.calcular_media_geral(disciplina_id)

    if media is None:
        print(
            "[AVISO] Ainda não há notas das duas unidades "
            "para calcular a média geral."
        )
        return

    print(f"[OK] Média geral da disciplina: {media:.1f}")