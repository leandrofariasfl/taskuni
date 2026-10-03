import json
import os
import tempfile
from pathlib import Path

PASTA_DADOS = Path(__file__).resolve().parent.parent / "dados"

def caminho(nome):
    PASTA_DADOS.mkdir(exist_ok=True)
    return PASTA_DADOS / f"{nome}.json"

def carregar(nome):
    arq = caminho(nome)
    if not arq.exists():
        return []
    try:
        with arq.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        arq.rename(arq.with_suffix(".corrompido.json"))
        return []

def gravar(nome, dados):
    arq = caminho(nome)
    fd, tmp = tempfile.mkstemp(dir=arq.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        os.replace(tmp, arq)
    except Exception:
        os.unlink(tmp)
        raise

def proximo_id(dados):
    return max((i["id"] for i in dados), default=0) + 1