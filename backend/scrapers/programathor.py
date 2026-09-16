"""
Scraper do Programathor via RSS.
"""

import feedparser

RSS_URL = "https://programathor.com.br/feed"

def buscar_vagas() -> list[dict]:
    vagas = []
    try:
        feed = feedparser.parse(RSS_URL)
        for entry in feed.entries:
            vagas.append({
                "titulo": entry.get("title", ""),
                "empresa": "",
                "url": entry.get("link", ""),
                "descricao": entry.get("summary", ""),
                "data": entry.get("published", ""),
                "fonte": "Programathor",
                "area": "Desenvolvimento",
            })
    except Exception as e:
        print(f"[Programathor] Erro: {e}")
    return vagas
