"""Servidor local do dashboard do VagaBot.

O endpoint de busca nunca envia e-mail: ele apenas coleta e mostra vagas.
O envio agendado continua sendo feito por ``main.py``.
"""

from datetime import datetime
from pathlib import Path
from threading import Lock

from flask import Flask, jsonify, send_from_directory

from main import buscar_e_notificar

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")
_lock = Lock()
_estado = {"vagas": [], "atualizado_em": None, "erro": None}


def _montar_resposta(resultado: dict) -> dict:
    novas = {vaga.get("id") or vaga.get("url") for vaga in resultado["novas"]}
    vagas = []
    for vaga in resultado["filtradas"]:
        chave = vaga.get("id") or vaga.get("url")
        vagas.append({**vaga, "nova": chave in novas})
    return {
        "vagas": vagas,
        "total_coletadas": len(resultado["coletadas"]),
        "total_novas": len(resultado["novas"]),
        "atualizado_em": datetime.now().isoformat(timespec="seconds"),
    }


def _buscar() -> dict:
    with _lock:
        try:
            # A tela mostra também os scores abaixo do limiar de e-mail.
            _estado.update(_montar_resposta(buscar_e_notificar(enviar=False, minimo=0)))
            _estado["erro"] = None
        except Exception as erro:
            _estado["erro"] = "Não foi possível atualizar as vagas agora. Tente novamente."
            print(f"[Dashboard] Erro na busca: {erro}")
        return _estado.copy()


@app.get("/api/vagas")
def vagas():
    return jsonify(_estado)


@app.post("/api/buscar")
def buscar():
    return jsonify(_buscar())


@app.get("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 5000))
    host = "0.0.0.0"
    print(f"[Dashboard] Disponível em http://{host}:{port}")
    app.run(host=host, port=port, debug=False)
