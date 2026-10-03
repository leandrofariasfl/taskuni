from . import _armazenamento as arm

_NOME = "conteudos"
_dados = arm.carregar(_NOME)

def salvar():
    arm.gravar(_NOME, _dados)

def adicionar(disciplina_id, titulo, **extras):
    item = {
        "id": arm.proximo_id(_dados),
        "disciplina_id": disciplina_id,
        "titulo": titulo,
        **extras,
    }
    _dados.append(item)
    salvar()
    return item

def listar():
    return list(_dados)

def listar_por_disciplina(disciplina_id):
    return [c for c in _dados if c["disciplina_id"] == disciplina_id]

def buscar(id):
    return next((i for i in _dados if i["id"] == id), None)

def atualizar(id, **campos):
    item = buscar(id)
    if item is None:
        return None
    campos.pop("id", None)
    item.update(campos)
    salvar()
    return item

def remover(id):
    item = buscar(id)
    if item is None:
        return False
    _dados.remove(item)
    salvar()
    return True

def remover_por_disciplina(disciplina_id):
    """Útil ao apagar uma disciplina: remove os conteúdos dela."""
    _dados[:] = [c for c in _dados if c["disciplina_id"] != disciplina_id]
    salvar()