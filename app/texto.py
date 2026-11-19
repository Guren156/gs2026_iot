import re
import unicodedata

STOPWORDS = {
    "a", "o", "as", "os", "um", "uma", "uns", "umas", "de", "da", "do", "das", "dos",
    "em", "na", "no", "nas", "nos", "por", "para", "pra", "com", "sem", "que", "e",
    "ou", "se", "eu", "meu", "minha", "meus", "minhas", "ele", "ela", "eles", "elas",
    "nos", "nossa", "nosso", "voce", "voces", "esta", "estou", "estamos", "tem", "tenho",
    "temos", "ter", "ser", "sou", "muito", "muita", "mais", "mas", "como", "quando",
    "ja", "nao", "sim", "isso", "esse", "essa", "este", "aqui", "la", "ao", "aos",
    "precisa", "preciso", "precisamos", "precisando", "ajuda", "ajudar", "alguem",
    "algum", "alguma", "favor", "gostaria", "queria", "quero", "pode", "podem",
}


def normalizar(texto):
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return sem_acento.lower()


def tokenizar(texto):
    palavras = re.findall(r"[a-z]+", normalizar(texto))
    tokens = []
    for palavra in palavras:
        if len(palavra) < 3 or palavra in STOPWORDS:
            continue
        if len(palavra) > 4 and palavra.endswith("s"):
            palavra = palavra[:-1]
        tokens.append(palavra)
    return tokens
