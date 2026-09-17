"""
Scraper do Vagas.com.br via RSS por categoria.

URLs no formato: https://www.vagas.com.br/vagas-de-{categoria}.rss
"""

import hashlib
import re
import requests
from scrapers.rss import parse_feed

HEADERS = {"User-Agent": "vagabot/1.0 (monitoramento de vagas)"}

CATEGORIAS = [
    ("ti-telecom",         "TI"),
    ("estagio",            "Estágio"),
    ("desenvolvimento-web", "Desenvolvimento"),
    ("banco-de-dados",     "Dados"),
    ("suporte-tecnico",    "Infraestrutura"),
    ("analista-sistemas",  "Desenvolvimento"),
]


def buscar_vagas() -> list[dict]:
    vagas = []
    for slug, area in CATEGORIAS:
        url = f"https://www.vagas.com.br/vagas-de-{slug}.rss"
        try:
            r = requests.get(url, timeout=12, headers=HEADERS)
            r.raise_for_status()
            for entry in parse_feed(r.content):
                link  = entry.get("link", "")
                titulo = entry.get("title", "")
                vagas.append({
                    "id":       f"vagas_{hashlib.sha256((link or titulo).encode()).hexdigest()[:16]}",
                    "titulo":   titulo,
                    "empresa":  entry.get("author", ""),
                    "url":      link,
                    "descricao": re.sub(r"<[^>]+>", " ", entry.get("summary", "")).strip(),
                    "data":     entry.get("published", ""),
                    "fonte":    "Vagas.com.br",
                    "area":     area,
                    "local":    "Não informado",
                    "labels":   [],
                })
        except requests.HTTPError as e:
            if e.response is not None:
                print(f"[Vagas.com.br] {slug}: HTTP {e.response.status_code}")
        except Exception as e:
            print(f"[Vagas.com.br] {slug}: {e}")
    print(f"[Vagas.com.br] {len(vagas)} vagas coletadas")
    return vagas
