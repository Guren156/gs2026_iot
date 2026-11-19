"""Roda os casos de teste e gera o relatorio em evidencias/avaliacao_<modo>.md

Uso: python -m avaliacao.avaliar --modo simulado
     python -m avaliacao.avaliar --modo gemini --pausa 5
"""
import argparse
import json
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from app.triagem import base_ongs, triar

RAIZ = Path(__file__).resolve().parent.parent


def percentual(acertos, total):
    return f"{acertos}/{total} ({100 * acertos / total:.0f}%)" if total else "-"


def avaliar(modo, pausa):
    casos = json.loads((RAIZ / "avaliacao" / "casos_teste.json").read_text(encoding="utf-8"))
    linhas = []
    contagem = {k: [0, 0] for k in ("categoria", "urgencia", "ongs", "rag", "emergencia", "privacidade", "invalido", "id_valido")}
    tempos = []
    modos_usados = set()

    def marcar(chave, ok):
        contagem[chave][0] += ok
        contagem[chave][1] += 1
        return "ok" if ok else "ERRO"

    for caso in casos:
        if caso.get("erro_esperado"):
            try:
                triar(caso["texto"], modo=modo)
                status = marcar("invalido", False)
            except ValueError:
                status = marcar("invalido", True)
            linhas.append(f'| {caso["id"]} | {caso["tipo"]} | entrada rejeitada: {status} | | | | |')
            continue

        inicio = time.perf_counter()
        r = triar(caso["texto"], modo=modo)
        tempos.append(time.perf_counter() - inicio)
        modos_usados.add(r["modo"] + (" (fallback)" if r["aviso"] else ""))

        id_cat = r["categoria"]["id_categoria"] if r["categoria"] else 0
        ids = [o["id_ong"] for o in r["ongs_sugeridas"]]
        st_cat = marcar("categoria", id_cat in caso["categorias"])
        st_urg = marcar("urgencia", r["urgencia"] == caso["urgencia"]) if caso["urgencia"] else "-"
        st_ong = marcar("ongs", any(i in caso["ongs_aceitas"] for i in ids)) if caso["ongs_aceitas"] else (
            marcar("ongs", not ids))
        st_emg = marcar("emergencia", r["emergencia"] == caso["emergencia"])
        marcar("id_valido", all(i in {o["id_ong"] for o in base_ongs().ongs} for i in ids))
        if caso["ongs_aceitas"]:
            rag = base_ongs().buscar(r["texto_enviado_ao_modelo"], caso["categorias"][0], 3)
            marcar("rag", any(o["id_ong"] in caso["ongs_aceitas"] for o in rag))
        if caso.get("dados_pessoais"):
            marcar("privacidade", set(caso["dados_pessoais"]) <= set(r["dados_pessoais_removidos"]))

        linhas.append(
            f'| {caso["id"]} | {caso["tipo"]} | {r["categoria"]["nome"] if r["categoria"] else "fora do escopo"} ({st_cat}) '
            f'| {r["urgencia"]} ({st_urg}) | {ids} ({st_ong}) | {st_emg} | {r["resumo"]} |'
        )
        if pausa:
            time.sleep(pausa)

    resumo = [
        f"# Avaliacao - modo {modo}",
        "",
        f"Modo efetivamente usado: {', '.join(sorted(modos_usados))}",
        f"Casos: {len(casos)} | tempo medio por pedido: {sum(tempos) / len(tempos):.2f}s",
        "",
        "| Metrica | Resultado |",
        "|---|---|",
        f'| Categoria correta | {percentual(*contagem["categoria"])} |',
        f'| Urgencia correta (pedidos no escopo) | {percentual(*contagem["urgencia"])} |',
        f'| ONG adequada entre as sugeridas (fora do escopo: nenhuma sugerida) | {percentual(*contagem["ongs"])} |',
        f'| RAG isolado: ONG adequada no top-3 com a categoria esperada | {percentual(*contagem["rag"])} |',
        f'| Emergencia detectada corretamente | {percentual(*contagem["emergencia"])} |',
        f'| Dados pessoais removidos | {percentual(*contagem["privacidade"])} |',
        f'| Somente ONGs reais sugeridas | {percentual(*contagem["id_valido"])} |',
        f'| Entrada invalida rejeitada | {percentual(*contagem["invalido"])} |',
        "",
        "| Caso | Tipo | Categoria | Urgencia | ONGs | Emergencia | Resumo |",
        "|---|---|---|---|---|---|---|",
        *linhas,
    ]
    destino = RAIZ / "evidencias" / f"avaliacao_{modo}.md"
    destino.parent.mkdir(exist_ok=True)
    destino.write_text("\n".join(resumo) + "\n", encoding="utf-8")
    print("\n".join(resumo[:16]))
    print(f"\nRelatorio completo em {destino}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--modo", choices=["simulado", "gemini"], default="simulado")
    parser.add_argument("--pausa", type=float, default=0, help="segundos entre pedidos (limite do plano gratuito)")
    args = parser.parse_args()
    avaliar(args.modo, args.pausa)
