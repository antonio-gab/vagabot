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


def _bool_env(nome: str, padrao: bool = True) -> bool:
    """Lê flags de ambiente sem transformar qualquer texto em verdadeiro."""
    valor = os.getenv(nome)
    if valor is None:
        return padrao
    return valor.strip().lower() in {"1", "true", "sim", "yes", "on"}

# ── Comportamento ─────────────────────────────────────────────────────────────
INTERVALO_HORAS = int(os.getenv("INTERVALO_HORAS", 6))
MATCH_MINIMO    = int(os.getenv("MATCH_MINIMO", 60))  # 0–100

# Fontes que já possuem scraper no projeto. CIEE continua desativado porque seu
# scraper é apenas um esqueleto; LinkedIn só entra quando RSS_URL for definido.
# As URLs RSS históricas dessas fontes não estão disponíveis atualmente. Elas
# permanecem opt-in para que possam ser reativadas quando URLs válidas forem
# configuradas, sem prejudicar a coleta padrão pelo GitHub.
ATIVAR_GUPY         = _bool_env("ATIVAR_GUPY", False)
ATIVAR_VAGAS_COM    = _bool_env("ATIVAR_VAGAS_COM", False)
ATIVAR_PROGRAMATHOR = _bool_env("ATIVAR_PROGRAMATHOR", False)

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
