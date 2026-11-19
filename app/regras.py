from app.texto import normalizar

PALAVRAS_CATEGORIA = {
    1: ["comida", "fome", "cesta", "aliment", "arroz", "feijao", "leite", "refeic", "comer", "marmita", "mercado", "lactose"],
    2: ["roupa", "agasalho", "casaco", "cobertor", "coberta", "frio", "calcado", "sapato", "tenis", "uniforme", "blusa", "jaqueta"],
    3: ["higiene", "sabonete", "absorvente", "fralda", "escova", "creme dental", "shampoo", "banho", "papel higienico"],
    4: ["voluntari", "reforco", "aula", "professor", "acompanha", "visita", "companhia", "reparo", "mutirao", "tarefa de casa", "leitura"],
    5: ["caderno", "lapis", "mochila", "material escolar", "livro", "caneta", "estojo"],
}

URGENCIA_BAIXA = ["nao e urgente", "sem pressa", "quando puder", "proximo mes", "mes que vem", "ano que vem", "futuramente"]
URGENCIA_ALTA = [
    "urgente", "hoje", "agora", "sem comer", "sem comida", "nada para comer", "nada pra comer", "fome",
    "bebe", "recem nascido", "recem-nascido", "gestante", "gravida", "na rua", "situacao de rua",
    "frio", "idoso", "idosa", "acamad", "perdeu tudo", "perdemos tudo", "despejad",
]

EMERGENCIAS = [
    (["violencia", "agred", "agrid", "apanh", "ameac", "me bate", "bate em mim", "abuso"],
     "Em caso de violencia, ligue 190 (Policia Militar) ou 180 (Central de Atendimento a Mulher)."),
    (["desmai", "nao respira", "sangr", "infarto", "convuls", "overdose", "muito mal"],
     "Em emergencia de saude, ligue 192 (SAMU)."),
    (["enchente", "alagamento", "desabamento", "deslizamento", "incendio", "fogo"],
     "Em enchente, deslizamento ou incendio, ligue 193 (Bombeiros) ou 199 (Defesa Civil)."),
    (["suicid", "me matar", "tirar minha vida", "nao aguento mais viver"],
     "Se voce esta pensando em tirar a propria vida, ligue 188 (CVV), gratuito e 24 horas."),
]


def classificar_categoria(texto):
    texto = normalizar(texto)
    pontos = {c: sum(p in texto for p in palavras) for c, palavras in PALAVRAS_CATEGORIA.items()}
    melhor = max(pontos, key=lambda c: (pontos[c], -c))
    return melhor if pontos[melhor] > 0 else 0


def classificar_urgencia(texto):
    texto = normalizar(texto)
    if any(p in texto for p in URGENCIA_BAIXA):
        return "BAIXA"
    if any(p in texto for p in URGENCIA_ALTA):
        return "ALTA"
    return "MEDIA"


def detectar_emergencia(texto):
    """Regra fixa, que nao depende do LLM: emergencia sempre recebe o numero do servico publico."""
    texto = normalizar(texto)
    return [orientacao for palavras, orientacao in EMERGENCIAS if any(p in texto for p in palavras)]
