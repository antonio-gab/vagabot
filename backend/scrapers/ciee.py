"""
Scraper do CIEE via requests + BeautifulSoup.
⚠️  O CIEE não tem RSS — este scraper acessa a página de busca diretamente.
    Pode quebrar se o site mudar o layout. Verifique periodicamente.
"""

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://portal.ciee.org.br/vagas/estagio"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def buscar_vagas(cidade: str = "Brasília") -> list[dict]:
    """
    TODO: implementar scraping real.
    O CIEE usa JavaScript pesado — pode ser necessário Selenium ou Playwright.
    """
    print("[CIEE] Scraper ainda não implementado — requer análise da página.")
    return []
