from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from app.dados import CATEGORIAS
from app.triagem import base_ongs, modo_configurado, triar

app = FastAPI(
    title="CitizenTech - Triagem de pedidos de ajuda com IA",
    description="Classifica o pedido com IA generativa (Gemini) e sugere ONGs por RAG basico.",
    version="1.0.0",
)


class Pedido(BaseModel):
    texto: str = Field(..., max_length=2000, examples=["Estou desempregada e sem comida em casa para meus 3 filhos, moro em Sao Paulo."])


@app.post("/triagem")
def triagem(pedido: Pedido):
    try:
        return triar(pedido.texto)
    except ValueError as erro:
        raise HTTPException(status_code=422, detail=str(erro))


@app.get("/ongs")
def listar_ongs():
    return [{"id_ong": o["id_ong"], "nome": o["nome"], "cidade": o["cidade"]} for o in base_ongs().ongs]


@app.get("/categorias")
def listar_categorias():
    return [{"id_categoria": i, "nome": n} for i, n in CATEGORIAS.items()]


@app.get("/health")
def health():
    return {"status": "ok", "modo": modo_configurado()}


@app.get("/", response_class=HTMLResponse)
def pagina_demo():
    return """<!doctype html>
<html lang="pt-br"><head><meta charset="utf-8"><title>Triagem CitizenTech</title>
<style>
body{font-family:system-ui,sans-serif;max-width:720px;margin:32px auto;padding:0 16px;color:#1f2933}
textarea{width:100%;height:110px;font-size:15px;padding:8px}
button{margin-top:8px;padding:8px 16px;font-size:15px;cursor:pointer}
.card{border:1px solid #d9e2ec;border-radius:8px;padding:12px 16px;margin-top:16px}
.alerta{background:#fde8e8;border-color:#f8b4b4}
</style></head><body>
<h1>Pedido de ajuda</h1>
<p>Descreva do que voce precisa. Dados pessoais sao removidos antes de irem para a IA.</p>
<textarea id="texto"></textarea><br><button onclick="enviar()">Enviar</button>
<div id="saida"></div>
<script>
async function enviar(){
  const saida=document.getElementById('saida'); saida.textContent='Analisando...';
  const r=await fetch('/triagem',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({texto:document.getElementById('texto').value})});
  const d=await r.json();
  if(!r.ok){saida.innerHTML='<div class="card alerta">'+(d.detail||'Erro')+'</div>';return;}
  const ongs=d.ongs_sugeridas.map(o=>'<li>'+o.nome+' ('+o.cidade+')</li>').join('')||'<li>Nenhuma</li>';
  saida.innerHTML='<div class="card'+(d.emergencia?' alerta':'')+'"><p>'+d.mensagem+'</p>'+
    '<p><b>Categoria:</b> '+(d.categoria?d.categoria.nome:'fora do escopo')+' | <b>Urgencia:</b> '+d.urgencia+'</p>'+
    '<p><b>ONGs sugeridas:</b></p><ul>'+ongs+'</ul>'+
    '<p><small>Modo: '+d.modo+(d.aviso?' - '+d.aviso:'')+' | Dados removidos: '+(d.dados_pessoais_removidos.join(', ')||'nenhum')+'</small></p></div>';
}
</script></body></html>"""
