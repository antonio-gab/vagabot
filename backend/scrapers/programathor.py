"""
Scraper do Programathor via RSS.
"""

import hashlib
import re

import requests

from scrapers.rss import parse_feed

RSS_URL = "https://programathor.com.br/feed"

def buscar_vagas() -> list[dict]:
    vagas = []
    try:
        resposta = requests.get(RSS_URL, timeout=15, headers={"User-Agent": "vagabot/1.0"})
        resposta.raise_for_status()
        entries = parse_feed(resposta.content)
        for entry in entries:
            link = entry.get("link", "")
            titulo = entry.get("title", "")
            vagas.append({
                "id": f"programathor_{hashlib.sha256((link or titulo).encode()).hexdigest()[:16]}",
                "titulo": titulo,
                "empresa": "",
                "url": link,
                "descricao": re.sub(r"<[^>]+>", " ", entry.get("summary", "")).strip(),
                "data": entry.get("published", ""),
                "fonte": "Programathor",
                "area": "Desenvolvimento",
                "local": "Não informado",
                "labels": [],
            })
    except Exception as e:
        print(f"[Programathor] Erro: {e}")
    return vagas
