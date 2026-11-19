import re

PADROES = [
    ("EMAIL", re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")),
    ("CPF", re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")),
    ("CEP", re.compile(r"\b\d{5}-\d{3}\b")),
    ("TELEFONE", re.compile(r"(\(?\b\d{2}\)?\s?)?\b9?\d{4}[-\s]?\d{4}\b")),
    ("ENDERECO", re.compile(r"\b(rua|avenida|av\.|travessa|alameda|estrada)\s+[^,.;\n\d]{2,40}?,?\s*(n[ºo°.]?\s*)?\d+", re.IGNORECASE)),
    ("NOME", re.compile(r"(?:(?<=[Mm]eu nome [ée] )|(?<=[Mm]e chamo ))[A-ZÀ-Ú][\wÀ-ú]+(\s+[A-ZÀ-Ú][\wÀ-ú]+){0,3}")),
]


def anonimizar(texto):
    """Troca dados pessoais por marcadores antes de o texto sair do servidor."""
    removidos = []
    for tipo, padrao in PADROES:
        texto, quantidade = padrao.subn(f"[{tipo}]", texto)
        if quantidade:
            removidos.append(tipo)
    return texto, removidos
