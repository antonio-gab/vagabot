"""
Configurações do VagaBot.
Valores sensíveis ficam no .env — nunca no código.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Credenciais ───────────────────────────────────────────────────────────────
GMAIL_USER         = os.getenv("GMAIL_USER", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")
DESTINATARIO       = os.getenv("DESTINATARIO", GMAIL_USER)
GITHUB_TOKEN       = os.getenv("GITHUB_TOKEN", "")

# ── Comportamento ─────────────────────────────────────────────────────────────
INTERVALO_HORAS = int(os.getenv("INTERVALO_HORAS", 6))
MATCH_MINIMO    = int(os.getenv("MATCH_MINIMO", 60))

# ── Fontes ativas ─────────────────────────────────────────────────────────────
# Todas ativas por padrão — desative no .env se quiser (ATIVAR_GUPY=false)
ATIVAR_GUPY         = os.getenv("ATIVAR_GUPY",         "true").lower() == "true"
ATIVAR_VAGAS_COM    = os.getenv("ATIVAR_VAGAS_COM",    "true").lower() == "true"
ATIVAR_PROGRAMATHOR = os.getenv("ATIVAR_PROGRAMATHOR", "true").lower() == "true"
ATIVAR_LINKEDIN     = os.getenv("ATIVAR_LINKEDIN",     "true").lower() == "true"

# ── Perfil do usuário ─────────────────────────────────────────────────────────
PERFIL = {
    "nome":        "Antonio Gabriel Vieira Paiva",
    "area":        "Desenvolvimento / TI",
    "nivel":       "estágio",
    "localizacao": "Brasília",

    "skills": [
        "Python", "SQL", "Power BI", "Excel", "Git", "JavaScript",
    ],

    "palavras_chave": [
        "estágio", "estagio", "desenvolvimento", "TI", "tecnologia",
        "Python", "banco de dados", "Brasília", "dados", "análise",
        "junior", "júnior", "suporte", "web",
    ],
}
