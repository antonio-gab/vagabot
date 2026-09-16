"""
Scraper do LinkedIn via RSS de busca salva.

Como gerar a URL RSS:
1. Acesse linkedin.com/jobs/search e filtre as vagas que quer
2. Salve a busca (ícone de sino)
3. Acesse suas buscas salvas e copie o link RSS

Cole a URL abaixo em RSS_URL.
"""

import feedparser

# Substitua pela sua URL RSS do LinkedIn
RSS_URL = ""

def buscar_vagas() -> list[dict]:
    if not RSS_URL:
        print("[LinkedIn] RSS_URL não configurado em linkedin_rss.py")
        return []
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
                "fonte": "LinkedIn",
                "area": "",
            })
    except Exception as e:
        print(f"[LinkedIn] Erro: {e}")
    return vagas
