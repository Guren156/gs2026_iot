import pytest
from fastapi.testclient import TestClient

from app import triagem
from app.llm import ClienteGemini, FalhaLLM
from app.main import app
from app.privacidade import anonimizar
from app.rag import BaseONGs
from app.regras import detectar_emergencia


def test_anonimizar_remove_dados_pessoais():
    texto, removidos = anonimizar(
        "Meu nome e Joao Pereira, CPF 123.456.789-09, Rua das Flores, 120, tel (11) 91234-5678, joao@email.com"
    )
    assert set(removidos) == {"NOME", "CPF", "ENDERECO", "TELEFONE", "EMAIL"}
    for dado in ("Joao", "123.456", "Flores", "91234", "joao@"):
        assert dado not in texto


def test_morar_na_rua_nao_e_endereco():
    texto, removidos = anonimizar("Durmo na rua perto da praca e preciso de cobertor")
    assert removidos == []
    assert "cobertor" in texto


def test_emergencia_detectada_por_regra():
    assert detectar_emergencia("Meu marido me agride")
    assert detectar_emergencia("Nao aguento mais viver")
    assert detectar_emergencia("Preciso de um casaco") == []


def test_rag_filtra_categoria_e_ignora_ong_inativa():
    base = BaseONGs()
    resultado = base.buscar("preciso de fraldas para meu bebe", id_categoria=3, k=3)
    assert resultado[0]["id_ong"] == 8
    assert all(o["id_ong"] != 5 for o in base.buscar("acolhimento familia desabrigada", k=12))


def test_entrada_curta_rejeitada():
    with pytest.raises(ValueError):
        triagem.triar("oi", modo="simulado")


def test_validacao_descarta_ong_que_nao_veio_do_rag():
    dados = {"id_categoria": 1, "urgencia": "ALTA", "ids_ongs": [99, 1, 6]}
    validado = ClienteGemini._validar(dados, [{"id_ong": 1}, {"id_ong": 6}])
    assert validado["ids_ongs"] == [1, 6]


def test_validacao_recusa_categoria_invalida():
    with pytest.raises(FalhaLLM):
        ClienteGemini._validar({"id_categoria": 9, "urgencia": "ALTA"}, [])


class GeminiFalso:
    def __init__(self, resposta=None, erro=None):
        self.resposta, self.erro = resposta, erro

    def triar(self, texto, candidatos):
        if self.erro:
            raise self.erro
        return ClienteGemini._validar(dict(self.resposta), candidatos)


def test_usa_resposta_do_gemini(monkeypatch):
    resposta = {"id_categoria": 1, "urgencia": "ALTA", "resumo": "Familia sem alimentos.",
                "ids_ongs": [6, 1], "mensagem": "Procure estas ONGs.", "justificativa": "Fome."}
    monkeypatch.setattr(triagem, "_cliente_gemini", lambda: GeminiFalso(resposta))
    r = triagem.triar("Minha geladeira esta vazia desde ontem", modo="gemini")
    assert r["modo"] == "gemini"
    assert r["categoria"]["nome"] == "Alimentos"
    assert {o["id_ong"] for o in r["ongs_sugeridas"]} <= {1, 6}


def test_fallback_para_simulado_quando_gemini_falha(monkeypatch):
    monkeypatch.setattr(triagem, "_cliente_gemini", lambda: GeminiFalso(erro=FalhaLLM("Gemini retornou erro 429")))
    r = triagem.triar("Preciso de cesta basica para minha familia", modo="gemini")
    assert r["modo"] == "simulado"
    assert "429" in r["aviso"]
    assert r["categoria"]["id_categoria"] == 1


def test_emergencia_sobrepoe_resposta_do_modelo(monkeypatch):
    resposta = {"id_categoria": 2, "urgencia": "BAIXA", "resumo": "Pedido de roupas.",
                "ids_ongs": [], "mensagem": "Veja as ONGs.", "justificativa": "Roupas."}
    monkeypatch.setattr(triagem, "_cliente_gemini", lambda: GeminiFalso(resposta))
    r = triagem.triar("Meu marido me agride e preciso de roupas", modo="gemini")
    assert r["emergencia"] and r["urgencia"] == "ALTA"
    assert "190" in r["mensagem"]


def test_api(monkeypatch):
    monkeypatch.setenv("LLM_MODO", "simulado")
    cliente = TestClient(app)
    assert cliente.get("/health").json()["modo"] == "simulado"
    resposta = cliente.post("/triagem", json={"texto": "Preciso de cadernos e lapis para meu filho"})
    assert resposta.status_code == 200
    assert resposta.json()["categoria"]["id_categoria"] == 5
    assert cliente.post("/triagem", json={"texto": "oi"}).status_code == 422
