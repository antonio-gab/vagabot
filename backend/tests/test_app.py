"""
Testes da API do dashboard (app.py).
Usa mocks para não fazer requisições reais nem enviar e-mails.
"""

import unittest
from unittest.mock import patch

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import app as dashboard


RESULTADO_MOCK = {
    "coletadas": [{"id": "gh_1", "titulo": "Vaga teste", "match": 75}],
    "filtradas": [{"id": "gh_1", "titulo": "Vaga teste", "match": 75}],
    "novas":     [{"id": "gh_1", "titulo": "Vaga teste", "match": 75}],
}


class DashboardApiTests(unittest.TestCase):

    def setUp(self):
        dashboard.app.config.update(TESTING=True)
        # Reseta estado entre testes
        dashboard._estado.update({
            "vagas": [], "total_coletadas": 0,
            "total_novas": 0, "atualizado_em": None, "erro": None,
        })
        self.client = dashboard.app.test_client()

    def test_status_retorna_ok(self):
        """GET /api/status deve retornar status ok."""
        r = self.client.get("/api/status")
        self.assertEqual(r.status_code, 200)
        dados = r.get_json()
        self.assertEqual(dados["status"], "ok")

    def test_vagas_retorna_estado_vazio_inicial(self):
        """GET /api/vagas devolve estado atual sem disparar busca."""
        r = self.client.get("/api/vagas")
        self.assertEqual(r.status_code, 200)
        dados = r.get_json()
        self.assertEqual(dados["vagas"], [])

    def test_buscar_chama_bot_sem_email_e_retorna_vagas(self):
        """POST /api/buscar nunca envia e-mail e devolve vagas formatadas."""
        with patch("app._importar_bot", return_value=lambda **kw: RESULTADO_MOCK):
            r = self.client.post("/api/buscar")
        self.assertEqual(r.status_code, 200)
        dados = r.get_json()
        self.assertEqual(dados["total_coletadas"], 1)
        self.assertEqual(len(dados["vagas"]), 1)
        self.assertTrue(dados["vagas"][0]["nova"])

    def test_buscar_marca_vaga_como_nova(self):
        """Vaga presente em 'novas' deve ter nova=True no retorno."""
        with patch("app._importar_bot", return_value=lambda **kw: RESULTADO_MOCK):
            r = self.client.post("/api/buscar")
        vaga = r.get_json()["vagas"][0]
        self.assertTrue(vaga["nova"])

    def test_indice_serve_frontend(self):
        """GET / deve devolver o index.html do frontend."""
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        # Verifica que é HTML
        self.assertIn(b"<!doctype html>", r.data.lower())
        r.close()


if __name__ == "__main__":
    unittest.main()
