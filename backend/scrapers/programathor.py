"""
Scraper do Programathor via RSS.

Feed principal: https://programathor.com.br/feed
Vagas focadas em desenvolvimento de software no Brasil.
"""

import hashlib
import re
import requests
from scrapers.rss import parse_feed

HEADERS = {"User-Agent": "vagabot/1.0 (monitoramento de vagas)"}

FEEDS = [
    "https://programathor.com.br/feed",
    "https://programathor.com.br/jobs.rss",
]


def buscar_vagas() -> list[dict]:
    vagas = []
    ids_vistos = set()

    for url in FEEDS:
        try:
            r = requests.get(url, timeout=12, headers=HEADERS)
            r.raise_for_status()
            for entry in parse_feed(r.content):
                link  = entry.get("link", "")
                titulo = entry.get("title", "")
                vid = hashlib.sha256((link or titulo).encode()).hexdigest()[:16]
                if vid in ids_vistos:
                    continue
                ids_vistos.add(vid)
                vagas.append({
                    "id":       f"programathor_{vid}",
                    "titulo":   titulo,
                    "empresa":  entry.get("author", ""),
                    "url":      link,
                    "descricao": re.sub(r"<[^>]+>", " ", entry.get("summary", "")).strip(),
                    "data":     entry.get("published", ""),
                    "fonte":    "Programathor",
                    "area":     "Desenvolvimento",
                    "local":    "Não informado",
                    "labels":   [],
                })
        except requests.HTTPError as e:
            if e.response is not None:
                print(f"[Programathor] {url}: HTTP {e.response.status_code}")
        except Exception as e:
            print(f"[Programathor] {url}: {e}")

    print(f"[Programathor] {len(vagas)} vagas coletadas")
    return vagas
