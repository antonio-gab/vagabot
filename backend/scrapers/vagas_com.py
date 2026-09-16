"""
Scraper do Vagas.com.br via RSS por categoria.
"""

import hashlib
import re

import requests

from scrapers.rss import parse_feed

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
            resposta = requests.get(url, timeout=15, headers={"User-Agent": "vagabot/1.0"})
            resposta.raise_for_status()
            entries = parse_feed(resposta.content)
            for entry in entries:
                link = entry.get("link", "")
                titulo = entry.get("title", "")
                vagas.append({
                    "id": f"vagas_{hashlib.sha256((link or titulo).encode()).hexdigest()[:16]}",
                    "titulo": titulo,
                    "empresa": entry.get("author", ""),
                    "url": link,
                    "descricao": re.sub(r"<[^>]+>", " ", entry.get("summary", "")).strip(),
                    "data": entry.get("published", ""),
                    "fonte": "Vagas.com.br",
                    "area": cat,
                    "local": "Não informado",
                    "labels": [],
                })
        except Exception as e:
            print(f"[Vagas.com.br] Erro na categoria {cat}: {e}")
    return vagas
