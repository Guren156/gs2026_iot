import os

from app.dados import CATEGORIAS
from app.llm import ClienteGemini, FalhaLLM
from app.privacidade import anonimizar
from app.rag import BaseONGs
from app.regras import classificar_categoria, classificar_urgencia, detectar_emergencia

_base = None
_cliente = None


def base_ongs():
    global _base
    if _base is None:
        _base = BaseONGs()
    return _base


def modo_configurado():
    modo = os.getenv("LLM_MODO", "auto").lower()
    if modo == "auto":
        return "gemini" if os.getenv("GEMINI_API_KEY") else "simulado"
    return modo


def _cliente_gemini():
    global _cliente
    if _cliente is None:
        _cliente = ClienteGemini()
    return _cliente


def _triagem_simulada(texto):
    id_categoria = classificar_categoria(texto)
    if id_categoria:
        mensagem = f"Encontramos ONGs que podem ajudar com {CATEGORIAS[id_categoria].lower()}. Seu pedido foi encaminhado para analise."
        resumo = f"Pedido de {CATEGORIAS[id_categoria].lower()}."
    else:
        mensagem = "Esse tipo de ajuda nao e oferecido pelas ONGs da plataforma. Procure o CRAS da sua regiao."
        resumo = "Pedido fora do escopo das ONGs da plataforma."
    return {
        "id_categoria": id_categoria,
        "urgencia": classificar_urgencia(texto),
        "resumo": resumo,
        "ids_ongs": [],
        "mensagem": mensagem,
        "justificativa": "Classificado por palavras-chave (modo simulado).",
    }


def triar(texto, modo=None):
    texto = (texto or "").strip()
    if len(texto) < 10:
        raise ValueError("Descreva o pedido com pelo menos 10 caracteres.")

    texto_seguro, removidos = anonimizar(texto)
    orientacoes = detectar_emergencia(texto_seguro)
    candidatos = base_ongs().buscar(texto_seguro, None, 5)

    modo = modo or modo_configurado()
    aviso = None
    resultado = None
    if modo == "gemini":
        try:
            resultado = _cliente_gemini().triar(texto_seguro, candidatos)
        except FalhaLLM as erro:
            aviso = f"{erro}. Usando o modo simulado."
            modo = "simulado"
    if resultado is None:
        resultado = _triagem_simulada(texto_seguro)

    id_categoria = resultado["id_categoria"]
    ongs = [o for o in candidatos if o["id_ong"] in resultado["ids_ongs"]]
    if id_categoria and not ongs:
        ongs = base_ongs().buscar(texto_seguro, id_categoria, 3)
    if not id_categoria:
        ongs = []

    urgencia = resultado["urgencia"]
    mensagem = resultado["mensagem"]
    if orientacoes:
        urgencia = "ALTA"
        mensagem = "ATENCAO: " + " ".join(orientacoes) + " " + mensagem

    return {
        "categoria": {"id_categoria": id_categoria, "nome": CATEGORIAS[id_categoria]} if id_categoria else None,
        "urgencia": urgencia,
        "resumo": resultado["resumo"],
        "fora_do_escopo": not id_categoria,
        "ongs_sugeridas": [{"id_ong": o["id_ong"], "nome": o["nome"], "cidade": o["cidade"]} for o in ongs],
        "mensagem": mensagem,
        "justificativa": resultado["justificativa"],
        "emergencia": bool(orientacoes),
        "orientacoes_emergencia": orientacoes,
        "dados_pessoais_removidos": removidos,
        "texto_enviado_ao_modelo": texto_seguro,
        "modo": modo,
        "aviso": aviso,
    }
