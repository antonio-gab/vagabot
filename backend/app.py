"""
VagaBot — servidor web + agendador em processo único.

Em produção (Railway) o gunicorn sobe este arquivo como módulo WSGI.
O agendador do bot roda em uma thread separada iniciada no startup.

Endpoints:
  GET  /          → dashboard HTML
  GET  /api/vagas → vagas em cache (não dispara nova busca)
  POST /api/buscar → dispara busca real e devolve resultado
  GET  /api/status → healthcheck para o Railway
"""

import os
import threading
from datetime import datetime
from pathlib import Path

import schedule
import time

from flask import Flask, jsonify, send_from_directory

# ── Caminhos ──────────────────────────────────────────────────────────────────
BASE_DIR     = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

# ── Flask ─────────────────────────────────────────────────────────────────────
app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")

# ── Estado compartilhado entre threads ───────────────────────────────────────
_lock   = threading.Lock()
_estado = {
    "vagas":           [],
    "total_coletadas": 0,
    "total_novas":     0,
    "atualizado_em":   None,
    "erro":            None,
}


# ── Importação lazy do bot (evita import circular) ────────────────────────────
def _importar_bot():
    from main import buscar_e_notificar
    return buscar_e_notificar


def _montar_resposta(resultado: dict) -> dict:
    novas = {v.get("id") or v.get("url") for v in resultado["novas"]}
    vagas = []
    for v in resultado["filtradas"]:
        chave = v.get("id") or v.get("url")
        vagas.append({**v, "nova": chave in novas})
    return {
        "vagas":           vagas,
        "total_coletadas": len(resultado["coletadas"]),
        "total_novas":     len(resultado["novas"]),
        "atualizado_em":   datetime.now().isoformat(timespec="seconds"),
        "erro":            None,
    }


def _executar_busca(enviar_email: bool = False) -> dict:
    """Roda a busca e atualiza o estado global. Thread-safe."""
    with _lock:
        try:
            buscar_e_notificar = _importar_bot()
            # Dashboard mostra todas as vagas (minimo=0)
            # E-mail segue o MATCH_MINIMO do config.py
            resultado = buscar_e_notificar(enviar=enviar_email, minimo=0)
            _estado.update(_montar_resposta(resultado))
        except Exception as e:
            _estado["erro"] = "Erro interno na busca. Verifique os logs do servidor."
            print(f"[App] Erro na busca: {e}")
        return _estado.copy()


# ── Agendador (roda em thread separada) ──────────────────────────────────────
def _loop_agendador():
    from config import INTERVALO_HORAS
    print(f"[Scheduler] Bot agendado a cada {INTERVALO_HORAS}h.")

    # Primeira busca ao iniciar (com envio de e-mail ativado)
    _executar_busca(enviar_email=True)

    # Agendamento periódico
    schedule.every(INTERVALO_HORAS).hours.do(lambda: _executar_busca(enviar_email=True))

    while True:
        schedule.run_pending()
        time.sleep(60)


def _iniciar_agendador():
    """Inicia o scheduler em daemon thread — morre junto com o processo principal."""
    t = threading.Thread(target=_loop_agendador, daemon=True, name="vagabot-scheduler")
    t.start()
    print("[App] Agendador iniciado em background.")


# ── Rotas ─────────────────────────────────────────────────────────────────────
@app.get("/api/status")
def status():
    """Healthcheck — Railway usa isso para saber se o app está saudável."""
    return jsonify({
        "status":        "ok",
        "atualizado_em": _estado.get("atualizado_em"),
        "total_vagas":   len(_estado.get("vagas", [])),
    })


@app.get("/api/vagas")
def vagas():
    """Retorna vagas em cache — não dispara nova busca."""
    return jsonify(_estado)


@app.post("/api/buscar")
def buscar():
    """Dispara busca manual (sem enviar e-mail) e retorna resultado."""
    return jsonify(_executar_busca(enviar_email=False))


@app.get("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


# ── Startup ───────────────────────────────────────────────────────────────────
# Iniciado uma vez só — gunicorn pode criar vários workers,
# mas o scheduler só deve rodar em um deles.
_SCHEDULER_INICIADO = False

def iniciar_se_necessario():
    global _SCHEDULER_INICIADO
    if not _SCHEDULER_INICIADO:
        _SCHEDULER_INICIADO = True
        _iniciar_agendador()


# Gunicorn chama este hook ao fazer fork do worker
try:
    from gunicorn.arbiter import Arbiter  # noqa: F401
    # Em produção com gunicorn, usamos post_fork via config
except ImportError:
    pass  # Ambiente de desenvolvimento — ok


# ── Desenvolvimento local ─────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"[App] Iniciando em modo desenvolvimento — http://0.0.0.0:{port}")
    iniciar_se_necessario()
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
