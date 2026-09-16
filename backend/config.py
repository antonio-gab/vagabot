# ── Configurações do VagaBot ──────────────────────────────────────────────────
# Edite este arquivo com seu perfil real antes de rodar o bot.

import os
from dotenv import load_dotenv

load_dotenv()

# Credenciais Gmail
GMAIL_USER = os.getenv("GMAIL_USER", "seu@gmail.com")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")
DESTINATARIO = os.getenv("DESTINATARIO", GMAIL_USER)

# Frequência
INTERVALO_HORAS = int(os.getenv("INTERVALO_HORAS", 6))

# Match mínimo para notificar (0–100)
MATCH_MINIMO = int(os.getenv("MATCH_MINIMO", 70))

# Perfil do usuário
PERFIL = {
    "nome": "Antonio Gabriel Vieira Paiva",
    "area": "Desenvolvimento / TI",
    "nivel": "Estágio",           # Estágio | Júnior | Pleno | Sênior
    "localizacao": "Brasília",
    "skills": [
        "Python", "SQL", "Power BI", "Excel", "Git", "JavaScript",
    ],
    "palavras_chave": [
        "estágio", "estagio", "desenvolvimento", "TI", "tecnologia",
        "Python", "banco de dados", "Brasília",
    ],
}
