"""
Configuração do Gunicorn para produção (Railway).

Gunicorn faz fork de múltiplos workers — o scheduler do bot
deve rodar em apenas UM deles. O hook post_fork garante isso.
"""

import os

# ── Servidor ──────────────────────────────────────────────────────────────────
bind    = f"0.0.0.0:{os.getenv('PORT', '5000')}"
workers = 1        # 1 worker = scheduler roda uma vez só, sem conflito
threads = 4        # 4 threads por worker para aguentar requisições simultâneas
timeout = 120      # tempo máximo por requisição (busca pode demorar)

# ── Logs ──────────────────────────────────────────────────────────────────────
accesslog = "-"   # stdout
errorlog  = "-"   # stderr
loglevel  = "info"

# ── Hooks ─────────────────────────────────────────────────────────────────────
def post_fork(server, worker):
    """Iniciado uma vez no worker — aqui o scheduler começa."""
    import app as dashboard
    dashboard.iniciar_se_necessario()
