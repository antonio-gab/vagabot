"""
Scraper do LinkedIn via RSS de busca salva.

O LinkedIn permite exportar buscas salvas como RSS.
A URL é configurada via variável de ambiente LINKEDIN_RSS_URL
para não ficar hardcoded no código.

Como gerar a URL RSS:
  1. Acesse linkedin.com/jobs/search
  2. Filtre: "estágio TI Brasília" (ou o que quiser)
  3. Clique no sino para salvar a busca
  4. Vá em "Buscas salvas" → copie o link RSS
  5. Cole em LINKEDIN_RSS_URL no .env ou nas variáveis do Railway
"""

import hashlib
import os
import re
import requests
from scrapers.rss import parse_feed

HEADERS = {"User-Agent": "vagabot/1.0 (monitoramento de vagas)"}

# Lê a URL do ambiente — sem ela, este scraper é pulado silenciosamente
RSS_URL = os.getenv("LINKEDIN_RSS_URL", "").strip()


def buscar_vagas() -> list[dict]:
    if not RSS_URL:
        # Não imprime erro — simplesmente não está configurado ainda
        return []

    vagas = []
    try:
        r = requests.get(RSS_URL, timeout=12, headers=HEADERS)
        r.raise_for_status()
        for entry in parse_feed(r.content):
            link  = entry.get("link", "")
            titulo = entry.get("title", "")
            vagas.append({
                "id":       f"linkedin_{hashlib.sha256((link or titulo).encode()).hexdigest()[:16]}",
                "titulo":   titulo,
                "empresa":  entry.get("author", ""),
                "url":      link,
                "descricao": re.sub(r"<[^>]+>", " ", entry.get("summary", "")).strip(),
                "data":     entry.get("published", ""),
                "fonte":    "LinkedIn",
                "area":     "",
                "local":    "Não informado",
                "labels":   [],
            })
        print(f"[LinkedIn] {len(vagas)} vagas coletadas")
    except requests.HTTPError as e:
        if e.response is not None:
            print(f"[LinkedIn] HTTP {e.response.status_code} — verifique LINKEDIN_RSS_URL")
    except Exception as e:
        print(f"[LinkedIn] {e}")

    return vagas
