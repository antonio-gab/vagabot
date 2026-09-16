"""
Scraper de vagas via GitHub Issues.

Repositórios brasileiros de vagas publicam oportunidades como issues abertas,
com labels indicando nível (Júnior, Estagiário), regime e tecnologias.

Estratégia de busca em duas camadas:
  1. Por nível: Estagiário, Júnior (mais relevantes)
  2. Por tecnologia: Python, JavaScript, SQL (captura vagas sem label de nível)

Repositórios monitorados:
  - frontendbr/vagas    → Front-end
  - backend-br/vagas    → Back-end
  - datascience-br/vagas → Dados, BI, ML
"""

import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

REPOS = [
    {"repo": "frontendbr/vagas",      "area": "Desenvolvimento"},
    {"repo": "backend-br/vagas",      "area": "Desenvolvimento"},
    {"repo": "datascience-br/vagas",  "area": "Dados"},
]

# Busca por nível preferencial
LABELS_NIVEL = ["Estagiário", "Júnior"]

# Busca por tecnologia (captura vagas que não têm label de nível)
LABELS_TECH = ["Python", "JavaScript", "SQL", "Git"]

# Descarta issues que são templates em branco
SPAM_PHRASES = [
    "informe a descrição da empresa",
    "informe a descrição da vaga",
    "nomedaempresa",
    "nome da empresa",
    "descreva aqui",
    "preencha aqui",
]


def _headers() -> dict:
    h = {"Accept": "application/vnd.github.v3+json", "User-Agent": "vagabot/1.0"}
    if GITHUB_TOKEN:
        h["Authorization"] = f"token {GITHUB_TOKEN}"
    return h


def _e_valida(body: str) -> bool:
    if not body or len(body.strip()) < 120:
        return False
    bl = body.lower().replace(" ", "")
    return not any(s.replace(" ", "") in bl for s in SPAM_PHRASES)


def _extrair_empresa(titulo: str) -> str:
    partes = titulo.split(" - ")
    return partes[-1].strip() if len(partes) >= 2 else ""


def _extrair_local(labels: list[str], titulo: str) -> str:
    locais = [l for l in labels if l in ("Remoto", "Híbrido", "Presencial")]
    if titulo.startswith("["):
        fim = titulo.find("]")
        if fim > 0:
            bracket = titulo[1:fim].strip()
            ignorar = {"alocação", "hiring", "vaga", "oportunidade", ""}
            if bracket.lower() not in ignorar and bracket not in ("Remoto", "Híbrido", "Presencial"):
                locais.insert(0, bracket)
    return " · ".join(locais) if locais else "Não informado"


def _buscar_com_label(repo: str, area: str, label: str) -> list[dict]:
    url = (
        f"https://api.github.com/repos/{repo}/issues"
        f"?state=open&labels={label}&per_page=30&sort=created&direction=desc"
    )
    try:
        r = requests.get(url, headers=_headers(), timeout=10)
        r.raise_for_status()
        vagas = []
        for issue in r.json():
            body = issue.get("body") or ""
            if not _e_valida(body):
                continue
            labels_nomes = [l["name"] for l in issue.get("labels", [])]
            titulo = issue.get("title", "").strip()
            vagas.append({
                "id":        f"gh_{repo.replace('/','_')}_{issue['number']}",
                "titulo":    titulo,
                "empresa":   _extrair_empresa(titulo),
                "local":     _extrair_local(labels_nomes, titulo),
                "descricao": body[:1000],
                "url":       issue.get("html_url", ""),
                "fonte":     f"GitHub/{repo.split('/')[0]}",
                "area":      area,
                "nivel":     label,
                "labels":    labels_nomes,
                "data":      issue.get("created_at", "")[:10],
            })
        return vagas
    except Exception as e:
        print(f"[GitHub] Erro em {repo} [{label}]: {e}")
        return []


def buscar_vagas() -> list[dict]:
    todas = []
    ids_vistos = set()

    for config in REPOS:
        repo, area = config["repo"], config["area"]
        count = 0

        # Camada 1: por nível
        for label in LABELS_NIVEL:
            for v in _buscar_com_label(repo, area, label):
                if v["id"] not in ids_vistos:
                    ids_vistos.add(v["id"])
                    todas.append(v)
                    count += 1

        # Camada 2: por tecnologia (complementar)
        for label in LABELS_TECH:
            for v in _buscar_com_label(repo, area, label):
                if v["id"] not in ids_vistos:
                    ids_vistos.add(v["id"])
                    todas.append(v)
                    count += 1

        print(f"[GitHub] {repo}: {count} vagas válidas")

    return todas
