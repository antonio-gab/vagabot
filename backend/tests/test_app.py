import unittest
from unittest.mock import patch

import app as dashboard


class DashboardApiTests(unittest.TestCase):
    def setUp(self):
        dashboard.app.config.update(TESTING=True)
        dashboard._estado.update({"vagas": [], "atualizado_em": None, "erro": None})
        self.client = dashboard.app.test_client()

    def test_indice_serve_dashboard(self):
        resposta = self.client.get("/")
        self.assertEqual(resposta.status_code, 200)
        self.assertIn(b"dashboard.jsx", resposta.data)
        resposta.close()

    @patch("app.buscar_e_notificar")
    def test_busca_nunca_envia_email_e_retorna_vagas(self, buscar):
        buscar.return_value = {
            "coletadas": [{"id": "1"}],
            "filtradas": [{"id": "1", "titulo": "Vaga de teste", "match": 75}],
            "novas": [{"id": "1"}],
        }
        resposta = self.client.post("/api/buscar")
        dados = resposta.get_json()
        buscar.assert_called_once_with(enviar=False, minimo=0)
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(dados["total_coletadas"], 1)
        self.assertTrue(dados["vagas"][0]["nova"])


if __name__ == "__main__":
    unittest.main()
