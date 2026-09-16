"""
VagaBot — ponto de entrada.
Agenda buscas automáticas e envia notificações por Gmail.
"""

import json
import os
import schedule
import time

from config import INTERVALO_HORAS, MATCH_MINIMO, PERFIL
from matcher import filtrar_vagas
from notifier import enviar_email

from scrapers.gupy import buscar_vagas as gupy_vagas
from scrapers.vagas_com import buscar_vagas as vagas_com_vagas
from scrapers.programathor import buscar_vagas as programathor_vagas
from scrapers.ciee import buscar_vagas as ciee_vagas
from scrapers.linkedin_rss import buscar_vagas as linkedin_vagas

VISTAS_PATH = os.path.join(os.path.dirname(__file__), "vagas_vistas.json")


def carregar_vistas() -> set:
    try:
        with open(VISTAS_PATH) as f:
            return set(json.load(f))
    except Exception:
        return set()


def salvar_vistas(vistas: set) -> None:
    with open(VISTAS_PATH, "w") as f:
        json.dump(list(vistas), f)


def buscar_e_notificar() -> None:
    print(f"\n[VagaBot] Iniciando busca... (match mínimo: {MATCH_MINIMO}%)")

    # Coleta de todas as fontes
    todas = []
    todas += gupy_vagas()
    todas += vagas_com_vagas()
    todas += programathor_vagas()
    todas += ciee_vagas()
    todas += linkedin_vagas()

    print(f"[VagaBot] {len(todas)} vagas brutas coletadas.")

    # Filtrar por match
    filtradas = filtrar_vagas(todas, minimo=MATCH_MINIMO)
    print(f"[VagaBot] {len(filtradas)} vagas acima de {MATCH_MINIMO}% de match.")

    # Remover vagas já vistas
    vistas = carregar_vistas()
    novas = [v for v in filtradas if v["url"] not in vistas]
    print(f"[VagaBot] {len(novas)} vagas novas (ainda não enviadas).")

    if novas:
        enviar_email(novas)
        vistas.update(v["url"] for v in novas)
        salvar_vistas(vistas)
    else:
        print("[VagaBot] Nenhuma vaga nova. Nenhum e-mail enviado.")


if __name__ == "__main__":
    print(f"🤖 VagaBot iniciado — buscando a cada {INTERVALO_HORAS}h")
    print(f"   Perfil: {PERFIL['nome']} · {PERFIL['area']} · {PERFIL['nivel']}")

    # Roda imediatamente ao iniciar
    buscar_e_notificar()

    # Agenda buscas periódicas
    schedule.every(INTERVALO_HORAS).hours.do(buscar_e_notificar)

    while True:
        schedule.run_pending()
        time.sleep(60)
