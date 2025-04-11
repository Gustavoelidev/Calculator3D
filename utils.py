import json
import os

CAMINHO_EMBALAGENS = "embalagens.json"

def carregar_embalagens():
    if not os.path.exists(CAMINHO_EMBALAGENS):
        return []
    with open(CAMINHO_EMBALAGENS, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_embalagens(lista):
    with open(CAMINHO_EMBALAGENS, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)
