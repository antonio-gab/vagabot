"""
Scraper do Gupy via RSS.

Cada empresa que usa o Gupy tem um feed RSS no formato:
  https://{slug}.gupy.io/jobs/feed.rss

Empresas em Brasília e grandes contratantes de estágio/júnior em TI.
Para adicionar mais: inclua o slug na lista EMPRESAS abaixo.
"""

import hashlib
import re
import requests
from scrapers.rss import parse_feed

HEADERS = {"User-Agent": "vagabot/1.0 (monitoramento de vagas)"}

EMPRESAS = [
    # ── Tecnologia / TI ───────────────────────────────────────────────────────
    "totvs",
    "stefanini",
    "accenture",
    "capgemini",
    "nttdata",
    "ci-t",
    "tivit",
    "unisys",
    "dxc-technology",
    "softplan",
    "sonda",
    "atos",
    "wipro",
    "cognizant",
    "indra",
    "eldorado",

    # ── Startups / Fintechs ───────────────────────────────────────────────────
    "nubank",
    "ifood",
    "stone",
    "pagseguro",
    "dock",
    "neon",
    "creditas",
    "loft",
    "gympass",
    "vtex",

    # ── Empresas de Brasília / setor público-privado ──────────────────────────
    "serpro",
    "embratel",
    "claro",
    "vivo",
    "oi",

    # ── Bancos e financeiras ──────────────────────────────────────────────────
    "banco-do-brasil",
    "caixa-economica-federal",
    "itau",
    "bradesco",
    "santander",
    "btgpactual",
    "xp-inc",

    # ── Grandes contratantes de estágio ───────────────────────────────────────
    "ambev",
    "vale",
    "petrobras",
    "bosch",
    "siemens",
    "ibm",
    "dell",
    "hp",
]


def _limpar_html(texto: str) -> str:
    return re.sub(r"<[^>]+>", " ", texto or "").strip()


def buscar_vagas() -> list[dict]:
    vagas = []
    for empresa in EMPRESAS:
        url = f"https://{empresa}.gupy.io/jobs/feed.rss"
        try:
            r = requests.get(url, timeout=12, headers=HEADERS)
            r.raise_for_status()
            for entry in parse_feed(r.content):
                link  = entry.get("link", "")
                titulo = entry.get("title", "")
                vagas.append({
                    "id":       f"gupy_{hashlib.sha256((link or titulo).encode()).hexdigest()[:16]}",
                    "titulo":   titulo,
                    "empresa":  empresa.replace("-", " ").title(),
                    "url":      link,
                    "descricao": _limpar_html(entry.get("summary", "")),
                    "data":     entry.get("published", ""),
                    "fonte":    "Gupy",
                    "area":     "",
                    "local":    "Não informado",
                    "labels":   [],
                })
        except requests.HTTPError as e:
            # 404 = empresa não usa Gupy ou slug errado — silencioso
            if e.response is not None and e.response.status_code != 404:
                print(f"[Gupy] {empresa}: HTTP {e.response.status_code}")
        except Exception as e:
            print(f"[Gupy] {empresa}: {e}")
    print(f"[Gupy] {len(vagas)} vagas coletadas de {len(EMPRESAS)} empresas")
    return vagas
