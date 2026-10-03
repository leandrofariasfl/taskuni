from . import _armazenamento as arm

_NOME = "disciplinas"
_dados = arm.carregar(_NOME)   # carregado uma vez, quando o módulo é importado

def salvar():
    arm.gravar(_NOME, _dados)

def adicionar(nome, **extras):
    item = {"id": arm.proximo_id(_dados), "nome": nome, **extras}
    _dados.append(item)
    salvar()
    return item

def listar():
    return list(_dados) # cópia da lista, evita alterações externas

def buscar(id):
    return next((i for i in _dados if i["id"] == id), None)

def atualizar(id, **campos):
    item = buscar(id)
    if item is None:
        return None
    campos.pop("id", None)       # impede alterar o id
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