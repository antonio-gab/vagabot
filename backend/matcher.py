"""
Calcula o score de compatibilidade entre uma vaga e o perfil do usuário.
Score de 0 a 100.
"""

from config import PERFIL


def calcular_match(vaga: dict) -> dict:
    """
    Retorna o score e as skills que faltam.
    """
    titulo = (vaga.get("titulo") or "").lower()
    descricao = (vaga.get("descricao") or "").lower()
    texto = titulo + " " + descricao

    skills_usuario = [s.lower() for s in PERFIL["skills"]]
    palavras_chave = [p.lower() for p in PERFIL["palavras_chave"]]

    # Skills presentes na vaga
    skills_match = [s for s in skills_usuario if s in texto]
    skills_faltando = [s for s in skills_usuario if s not in texto]

    # Score base: proporção de skills encontradas
    score = 0
    if skills_usuario:
        score = int((len(skills_match) / len(skills_usuario)) * 70)

    # Bônus por localização
    local = (vaga.get("local") or "").lower()
    if PERFIL["localizacao"].lower() in local or "remoto" in local:
        score += 15

    # Bônus por nível
    nivel = PERFIL["nivel"].lower()
    if nivel in texto or "estágio" in texto or "estagio" in texto:
        score += 10

    # Bônus por palavras-chave
    for p in palavras_chave:
        if p in texto:
            score += 1

    score = min(score, 100)

    return {
        **vaga,
        "match": score,
        "skills_match": skills_match,
        "skills_faltando": skills_faltando,
    }


def filtrar_vagas(vagas: list[dict], minimo: int = 70) -> list[dict]:
    """
    Retorna apenas vagas acima do score mínimo, ordenadas por score.
    """
    with_score = [calcular_match(v) for v in vagas]
    filtradas = [v for v in with_score if v["match"] >= minimo]
    return sorted(filtradas, key=lambda v: v["match"], reverse=True)
