"""
Configurações do VagaBot.
Edite este arquivo com seu perfil antes de rodar o bot.
Valores sensíveis (senhas, tokens) ficam no .env — nunca no código.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Credenciais ───────────────────────────────────────────────────────────────
GMAIL_USER        = os.getenv("GMAIL_USER", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")
DESTINATARIO      = os.getenv("DESTINATARIO", GMAIL_USER)
GITHUB_TOKEN      = os.getenv("GITHUB_TOKEN", "")   # token para scraper GitHub

# ── Comportamento ─────────────────────────────────────────────────────────────
INTERVALO_HORAS = int(os.getenv("INTERVALO_HORAS", 6))
MATCH_MINIMO    = int(os.getenv("MATCH_MINIMO", 60))  # 0–100

# ── Perfil do usuário ─────────────────────────────────────────────────────────
PERFIL = {
    "nome":        "Antonio Gabriel Vieira Paiva",
    "area":        "Desenvolvimento / TI",
    "nivel":       "estágio",   # estágio | júnior | pleno | sênior
    "localizacao": "Brasília",

    # Skills que o usuário já tem — usadas para calcular compatibilidade
    "skills": [
        "Python", "SQL", "Power BI", "Excel", "Git", "JavaScript",
    ],

    # Palavras-chave extras que aumentam o score quando aparecem na vaga
    "palavras_chave": [
        "estágio", "estagio", "desenvolvimento", "TI", "tecnologia",
        "Python", "banco de dados", "Brasília", "dados", "análise",
    ],
}
