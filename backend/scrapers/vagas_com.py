"""
Scraper do Vagas.com.br via RSS por categoria.
"""

import feedparser

CATEGORIAS = [
    "ti-telecom",
    "desenvolvimento",
    "estagio",
]

def buscar_vagas() -> list[dict]:
    vagas = []
    for cat in CATEGORIAS:
        url = f"https://www.vagas.com.br/vagas-de-{cat}.rss"
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                vagas.append({
                    "titulo": entry.get("title", ""),
                    "empresa": entry.get("author", ""),
                    "url": entry.get("link", ""),
                    "descricao": entry.get("summary", ""),
                    "data": entry.get("published", ""),
                    "fonte": "Vagas.com.br",
                    "area": cat,
                })
        except Exception as e:
            print(f"[Vagas.com.br] Erro na categoria {cat}: {e}")
    return vagas
