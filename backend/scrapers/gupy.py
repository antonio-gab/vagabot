"""
Scraper do Gupy via RSS.
O Gupy gera um RSS por empresa. Para adicionar novas empresas,
inclua o slug delas na lista EMPRESAS abaixo.
"""

import feedparser
from datetime import datetime

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

def buscar_vagas() -> list[dict]:
    vagas = []
    for empresa in EMPRESAS:
        url = f"https://{empresa}.gupy.io/jobs/feed.rss"
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                vagas.append({
                    "titulo": entry.get("title", ""),
                    "empresa": empresa.replace("-", " ").title(),
                    "url": entry.get("link", ""),
                    "descricao": entry.get("summary", ""),
                    "data": entry.get("published", ""),
                    "fonte": "Gupy",
                    "area": "",   # será preenchido pelo matcher
                })
        except Exception as e:
            print(f"[Gupy] Erro ao buscar {empresa}: {e}")
    return vagas
