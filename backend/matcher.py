"""
Calcula o score de compatibilidade entre uma vaga e o perfil do usuário.
Score de 0 a 100.

Fórmula:
  - Até 60 pts: skills do perfil encontradas na descrição/título da vaga
  - Até 20 pts: bônus de localização (Brasília ou Remoto)
  - Até 15 pts: bônus de nível (Estagiário/Júnior)
  - Até  5 pts: palavras-chave extras encontradas
"""

import unicodedata

from config import PERFIL


def _normalizar(texto: str) -> str:
    texto = str(texto or "").lower()
    return "".join(
        caractere for caractere in unicodedata.normalize("NFD", texto)
        if unicodedata.category(caractere) != "Mn"
    )


def calcular_match(vaga: dict) -> dict:
    titulo    = _normalizar(vaga.get("titulo", ""))
    descricao = _normalizar(vaga.get("descricao", ""))
    labels    = [_normalizar(l) for l in vaga.get("labels", [])]
    texto     = titulo + " " + descricao + " " + " ".join(labels)

    skills_usuario = [s.lower() for s in PERFIL["skills"]]
    palavras_chave = [p.lower() for p in PERFIL["palavras_chave"]]

    # ── Skills (0–60 pts) ────────────────────────────────────────────────────
    skills_match   = [s for s in skills_usuario if s in texto]
    skills_faltando = [s for s in skills_usuario if s not in texto]
    score_skills = int((len(skills_match) / len(skills_usuario)) * 60) if skills_usuario else 0

    # ── Localização (0–20 pts) ───────────────────────────────────────────────
    local = _normalizar(vaga.get("local", ""))
    loc_perfil = _normalizar(PERFIL["localizacao"])
    score_local = 0
    if loc_perfil in local or loc_perfil in texto:
        score_local = 20
    elif "remoto" in local or "remoto" in texto:
        score_local = 15
    elif "hibrido" in local or "hibrido" in texto:
        score_local = 10

    # ── Nível (0–15 pts) ─────────────────────────────────────────────────────
    nivel_perfil = _normalizar(PERFIL["nivel"])
    score_nivel = 0
    nivel_sinonimos = {
        "estágio": ["estágio", "estagio", "estagiário", "estagiario", "intern"],
        "júnior":  ["júnior", "junior", "jr"],
        "pleno":   ["pleno", "mid", "mid-level"],
        "sênior":  ["sênior", "senior", "sr"],
    }
    sinonimos = nivel_sinonimos.get(nivel_perfil, [nivel_perfil])
    if any(s in texto for s in sinonimos):
        score_nivel = 15

    # ── Palavras-chave extras (0–5 pts) ──────────────────────────────────────
    matches_kw = sum(1 for p in palavras_chave if p in texto)
    score_kw = min(matches_kw, 5)

    score_final = min(score_skills + score_local + score_nivel + score_kw, 100)

    return {
        **vaga,
        "match":           score_final,
        "skills_match":    skills_match,
        "skills_faltando": skills_faltando,
        "score_detalhe": {
            "skills":       score_skills,
            "localizacao":  score_local,
            "nivel":        score_nivel,
            "palavras_chave": score_kw,
        },
    }


def filtrar_vagas(vagas: list[dict], minimo: int = 70) -> list[dict]:
    """Filtra e ordena vagas por score de compatibilidade."""
    com_score = [calcular_match(v) for v in vagas]
    filtradas = [v for v in com_score if v["match"] >= minimo]
    return sorted(filtradas, key=lambda v: v["match"], reverse=True)


def remover_duplicatas(vagas: list[dict]) -> list[dict]:
    """Remove vagas com o mesmo ID ou mesma URL."""
    vistos_ids  = set()
    vistos_urls = set()
    unicas = []
    for v in vagas:
        vid = str(v.get("id", "")).strip()
        vurl = str(v.get("url", "")).strip()
        if vid and vid in vistos_ids:
            continue
        if vurl and vurl in vistos_urls:
            continue
        vistos_ids.add(vid)
        vistos_urls.add(vurl)
        unicas.append(v)
    return unicas
