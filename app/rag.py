import math
from collections import Counter

from app.dados import CATEGORIAS, carregar_ongs
from app.texto import normalizar, tokenizar


class BaseONGs:
    """RAG basico: indice TF-IDF sobre a descricao das ONGs ativas."""

    def __init__(self, ongs=None):
        self.ongs = [o for o in (ongs or carregar_ongs()) if o["ativa"]]
        documentos = [tokenizar(self._texto_documento(o)) for o in self.ongs]
        total = len(documentos)
        frequencia = Counter(t for doc in documentos for t in set(doc))
        self.idf = {t: math.log((1 + total) / (1 + f)) + 1 for t, f in frequencia.items()}
        self.vetores = [self._vetor(doc) for doc in documentos]

    @staticmethod
    def _texto_documento(ong):
        categorias = " ".join(CATEGORIAS[c] for c in ong["categorias"])
        return f'{ong["nome"]} {ong["descricao"]} {categorias}'

    def _vetor(self, tokens):
        contagem = Counter(tokens)
        vetor = {t: q * self.idf.get(t, 0) for t, q in contagem.items()}
        norma = math.sqrt(sum(v * v for v in vetor.values())) or 1
        return {t: v / norma for t, v in vetor.items()}

    def buscar(self, consulta, id_categoria=None, k=3):
        vetor_consulta = self._vetor(tokenizar(consulta))
        consulta_normalizada = normalizar(consulta)
        resultados = []
        for ong, vetor in zip(self.ongs, self.vetores):
            if id_categoria and id_categoria not in ong["categorias"]:
                continue
            score = sum(p * vetor.get(t, 0) for t, p in vetor_consulta.items())
            if normalizar(ong["cidade"]) in consulta_normalizada:
                score += 0.1
            resultados.append((score, ong))
        resultados.sort(key=lambda r: (-r[0], r[1]["id_ong"]))
        return [
            {
                "id_ong": ong["id_ong"],
                "nome": ong["nome"],
                "cidade": ong["cidade"],
                "descricao": ong["descricao"],
                "score": round(score, 3),
            }
            for score, ong in resultados[:k]
        ]
