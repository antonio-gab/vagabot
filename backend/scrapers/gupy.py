"""
Scraper do Gupy via RSS.
O Gupy gera um RSS por empresa. Para adicionar novas empresas,
inclua o slug delas na lista EMPRESAS abaixo.
"""

import hashlib
import re

import requests

from scrapers.rss import parse_feed

# Slugs das empresas no Gupy (adicione mais conforme quiser)
EMPRESAS = [
    "stefanini",
    "totvs",
    "accenture",
    "capgemini",
    "serpro",
    "banco-do-brasil",
    "caixa-economica-federal",
    "embratel",
]

def _texto_limpo(texto: str) -> str:
    return re.sub(r"<[^>]+>", " ", texto or "").strip()


def buscar_vagas() -> list[dict]:
    vagas = []
    for empresa in EMPRESAS:
        url = f"https://{empresa}.gupy.io/jobs/feed.rss"
        try:
            resposta = requests.get(url, timeout=15, headers={"User-Agent": "vagabot/1.0"})
            resposta.raise_for_status()
            entries = parse_feed(resposta.content)
            for entry in entries:
                link = entry.get("link", "")
                titulo = entry.get("title", "")
                vagas.append({
                    "id": f"gupy_{hashlib.sha256((link or titulo).encode()).hexdigest()[:16]}",
                    "titulo": titulo,
                    "empresa": empresa.replace("-", " ").title(),
                    "url": link,
                    "descricao": _texto_limpo(entry.get("summary", "")),
                    "data": entry.get("published", ""),
                    "fonte": "Gupy",
                    "area": "",   # será preenchido pelo matcher
                    "local": "Não informado",
                    "labels": [],
                })
        except Exception as e:
            print(f"[Gupy] Erro ao buscar {empresa}: {e}")
    return vagas
