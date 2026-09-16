"""
VagaBot — ponto de entrada.
Coleta vagas de todas as fontes, filtra por compatibilidade
e envia notificações por Gmail.

Uso:
    python main.py            # roda uma vez e agenda buscas a cada X horas
    python main.py --agora    # roda apenas uma vez e sai (bom para testes)
"""

import json
import os
import sys
import schedule
import time
from datetime import datetime

from config import INTERVALO_HORAS, MATCH_MINIMO, PERFIL, GITHUB_TOKEN
from matcher import filtrar_vagas, remover_duplicatas
from notifier import enviar_email

# Importa scrapers disponíveis
from scrapers.github_vagas import buscar_vagas as github_vagas

VISTAS_PATH = os.path.join(os.path.dirname(__file__), "vagas_vistas.json")


def carregar_vistas() -> set:
    try:
        with open(VISTAS_PATH) as f:
            return set(json.load(f))
    except Exception:
        return set()


def salvar_vistas(vistas: set) -> None:
    with open(VISTAS_PATH, "w") as f:
        json.dump(sorted(list(vistas)), f, indent=2)


def buscar_e_notificar() -> None:
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    print(f"\n{'='*55}")
    print(f"[VagaBot] Iniciando busca — {agora}")
    print(f"[VagaBot] Match mínimo: {MATCH_MINIMO}%")
    print(f"{'='*55}")

    # ── Coleta ────────────────────────────────────────────────────────────────
    todas = []

    # GitHub Issues (sempre disponível, sem restrições de rede)
    vagas_gh = github_vagas()
    todas.extend(vagas_gh)

    # RSS feeds (descomentar quando a rede permitir acesso externo)
    # from scrapers.gupy import buscar_vagas as gupy_vagas
    # from scrapers.vagas_com import buscar_vagas as vagas_com_vagas
    # from scrapers.programathor import buscar_vagas as programathor_vagas
    # todas.extend(gupy_vagas())
    # todas.extend(vagas_com_vagas())
    # todas.extend(programathor_vagas())

    print(f"[VagaBot] Total bruto: {len(todas)} vagas coletadas")

    # ── Deduplicação ──────────────────────────────────────────────────────────
    todas = remover_duplicatas(todas)
    print(f"[VagaBot] Após deduplicação: {len(todas)} vagas únicas")

    # ── Filtro por match ──────────────────────────────────────────────────────
    filtradas = filtrar_vagas(todas, minimo=MATCH_MINIMO)
    print(f"[VagaBot] Com match ≥ {MATCH_MINIMO}%: {len(filtradas)} vagas")

    if filtradas:
        print("\n  Top vagas encontradas:")
        for v in filtradas[:5]:
            print(f"  [{v['match']:3d}%] {v['titulo'][:60]} ({v['fonte']})")

    # ── Remove já vistas ──────────────────────────────────────────────────────
    vistas = carregar_vistas()
    novas = [v for v in filtradas if v.get("url", "") not in vistas]
    print(f"\n[VagaBot] Novas (ainda não enviadas): {len(novas)}")

    # ── Notifica ──────────────────────────────────────────────────────────────
    if novas:
        enviou = enviar_email(novas)
        if enviou:
            vistas.update(v["url"] for v in novas)
            salvar_vistas(vistas)
    else:
        print("[VagaBot] Nenhuma vaga nova — nenhum e-mail enviado.")

    print(f"\n[VagaBot] Busca concluída.")


if __name__ == "__main__":
    print(f"\n🤖 VagaBot iniciado!")
    print(f"   Perfil : {PERFIL['nome']}")
    print(f"   Área   : {PERFIL['area']} · {PERFIL['nivel']}")
    print(f"   Local  : {PERFIL['localizacao']}")
    print(f"   Skills : {', '.join(PERFIL['skills'])}")
    print(f"   GitHub Token: {'configurado ✓' if GITHUB_TOKEN else 'não configurado (limite menor de requisições)'}")

    modo_unico = "--agora" in sys.argv

    buscar_e_notificar()

    if not modo_unico:
        print(f"\n[VagaBot] Próxima busca em {INTERVALO_HORAS}h. Pressione Ctrl+C para parar.")
        schedule.every(INTERVALO_HORAS).hours.do(buscar_e_notificar)
        while True:
            schedule.run_pending()
            time.sleep(60)
