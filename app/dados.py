import json
from pathlib import Path

PASTA_DADOS = Path(__file__).resolve().parent.parent / "data"

# Mesmos IDs da tabela T_GS_CATEGORIA do banco Oracle
CATEGORIAS = {
    1: "Alimentos",
    2: "Roupas e agasalhos",
    3: "Higiene",
    4: "Voluntariado",
    5: "Material escolar",
}

URGENCIAS = ("BAIXA", "MEDIA", "ALTA")


def carregar_ongs():
    with open(PASTA_DADOS / "ongs.json", encoding="utf-8") as arquivo:
        return json.load(arquivo)
