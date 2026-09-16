"""
Scraper do LinkedIn via RSS de busca salva.

Como gerar a URL RSS:
1. Acesse linkedin.com/jobs/search e filtre as vagas que quer
2. Salve a busca (ícone de sino)
3. Acesse suas buscas salvas e copie o link RSS

Cole a URL abaixo em RSS_URL.
"""

import hashlib
import re

import requests

from scrapers.rss import parse_feed

# Substitua pela sua URL RSS do LinkedIn
RSS_URL = ""

def buscar_vagas() -> list[dict]:
    if not RSS_URL:
        print("[LinkedIn] RSS_URL não configurado em linkedin_rss.py")
        return []
    vagas = []
    try:
        resposta = requests.get(RSS_URL, timeout=15, headers={"User-Agent": "vagabot/1.0"})
        resposta.raise_for_status()
        for entry in parse_feed(resposta.content):
            link = entry.get("link", "")
            titulo = entry.get("title", "")
            vagas.append({
                "id": f"linkedin_{hashlib.sha256((link or titulo).encode()).hexdigest()[:16]}",
                "titulo": titulo,
                "empresa": "",
                "url": link,
                "descricao": re.sub(r"<[^>]+>", " ", entry.get("summary", "")).strip(),
                "data": entry.get("published", ""),
                "fonte": "LinkedIn",
                "area": "",
                "local": "Não informado",
                "labels": [],
            })
    except Exception as e:
        print(f"[LinkedIn] Erro: {e}")
    return vagas
