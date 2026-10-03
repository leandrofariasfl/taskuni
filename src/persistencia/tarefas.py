from . import _armazenamento as arm

_NOME = "tarefas"
_dados = arm.carregar(_NOME)

def salvar():
    arm.gravar(_NOME, _dados)

def adicionar(titulo, **extras):
    item = {"id": arm.proximo_id(_dados), "titulo": titulo, **extras}
    _dados.append(item)
    salvar()
    return item

def listar():
    return list(_dados)

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
