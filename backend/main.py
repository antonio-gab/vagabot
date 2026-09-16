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
import tempfile
import time
from datetime import datetime

from config import (
    ATIVAR_GUPY,
    ATIVAR_PROGRAMATHOR,
    ATIVAR_VAGAS_COM,
    GITHUB_TOKEN,
    INTERVALO_HORAS,
    MATCH_MINIMO,
    PERFIL,
)
from matcher import filtrar_vagas, remover_duplicatas
from notifier import enviar_email

# Importa scrapers disponíveis
from scrapers.github_vagas import buscar_vagas as github_vagas
from scrapers.gupy import buscar_vagas as gupy_vagas
from scrapers.programathor import buscar_vagas as programathor_vagas
from scrapers.vagas_com import buscar_vagas as vagas_com_vagas

VISTAS_PATH = os.path.join(os.path.dirname(__file__), "vagas_vistas.json")


def carregar_vistas() -> set:
    try:
        with open(VISTAS_PATH, encoding="utf-8") as f:
            dados = json.load(f)
        if not isinstance(dados, list):
            raise ValueError("o arquivo não contém uma lista")
        return {str(chave) for chave in dados if chave}
    except FileNotFoundError:
        return set()
    except (json.JSONDecodeError, OSError, ValueError) as erro:
        print(f"[VagaBot] Não foi possível ler vagas_vistas.json ({erro}); começando sem histórico.")
        return set()


def salvar_vistas(vistas: set) -> None:
    diretorio = os.path.dirname(VISTAS_PATH)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=diretorio, delete=False) as arquivo:
        json.dump(sorted(vistas), arquivo, indent=2, ensure_ascii=False)
        arquivo.write("\n")
        temporario = arquivo.name
    os.replace(temporario, VISTAS_PATH)


def chave_vaga(vaga: dict) -> str:
    """Chave estável para não reenviar uma vaga mesmo se a URL faltar."""
    return str(vaga.get("id") or vaga.get("url") or "").strip()


def _coletar(nome: str, scraper) -> list[dict]:
    try:
        vagas = scraper()
        if not isinstance(vagas, list):
            raise TypeError("o scraper não retornou uma lista")
        print(f"[VagaBot] {nome}: {len(vagas)} vagas coletadas")
        return vagas
    except Exception as erro:
        print(f"[VagaBot] {nome}: falhou sem interromper as outras fontes ({erro})")
        return []


def buscar_e_notificar(enviar: bool = True) -> dict:
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    print(f"\n{'='*55}")
    print(f"[VagaBot] Iniciando busca — {agora}")
    print(f"[VagaBot] Match mínimo: {MATCH_MINIMO}%")
    print(f"{'='*55}")

    # ── Coleta ────────────────────────────────────────────────────────────────
    todas = []

    todas.extend(_coletar("GitHub", github_vagas))
    if ATIVAR_GUPY:
        todas.extend(_coletar("Gupy", gupy_vagas))
    if ATIVAR_VAGAS_COM:
        todas.extend(_coletar("Vagas.com.br", vagas_com_vagas))
    if ATIVAR_PROGRAMATHOR:
        todas.extend(_coletar("Programathor", programathor_vagas))

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
    novas = [v for v in filtradas if chave_vaga(v) and chave_vaga(v) not in vistas]
    print(f"\n[VagaBot] Novas (ainda não enviadas): {len(novas)}")

    # ── Notifica ──────────────────────────────────────────────────────────────
    if novas and enviar:
        enviou = enviar_email(novas)
        if enviou:
            vistas.update(chave_vaga(v) for v in novas)
            salvar_vistas(vistas)
    elif novas:
        print("[VagaBot] Modo sem e-mail: vagas não foram marcadas como enviadas.")
    else:
        print("[VagaBot] Nenhuma vaga nova — nenhum e-mail enviado.")

    print(f"\n[VagaBot] Busca concluída.")
    return {"coletadas": todas, "filtradas": filtradas, "novas": novas}


if __name__ == "__main__":
    print(f"\n🤖 VagaBot iniciado!")
    print(f"   Perfil : {PERFIL['nome']}")
    print(f"   Área   : {PERFIL['area']} · {PERFIL['nivel']}")
    print(f"   Local  : {PERFIL['localizacao']}")
    print(f"   Skills : {', '.join(PERFIL['skills'])}")
    print(f"   GitHub Token: {'configurado ✓' if GITHUB_TOKEN else 'não configurado (limite menor de requisições)'}")

    modo_unico = "--agora" in sys.argv
    sem_email = "--sem-email" in sys.argv

    buscar_e_notificar(enviar=not sem_email)

    if not modo_unico:
        print(f"\n[VagaBot] Próxima busca em {INTERVALO_HORAS}h. Pressione Ctrl+C para parar.")
        schedule.every(INTERVALO_HORAS).hours.do(buscar_e_notificar)
        while True:
            schedule.run_pending()
            time.sleep(60)
