import json
import os
import tempfile
import unittest
from unittest.mock import patch

import main
from matcher import calcular_match, remover_duplicatas


VAGA = {
    "id": "teste-1", "titulo": "Estágio em Python", "empresa": "Empresa Teste",
    "local": "Brasília", "descricao": "Python SQL Git desenvolvimento de dados",
    "url": "https://example.test/vaga/1", "fonte": "Teste", "labels": ["Estágio"],
    "data": "2026-09-15",
}


class FluxoVagaBotTests(unittest.TestCase):
    def test_match_normaliza_acentos_e_hibrido_na_descricao(self):
        vaga = {**VAGA, "local": "Não informado", "descricao": "Vaga híbrida em Brasilia para estagiário Python"}
        resultado = calcular_match(vaga)
        self.assertEqual(resultado["score_detalhe"]["localizacao"], 20)
        self.assertEqual(resultado["score_detalhe"]["nivel"], 15)

    def test_remove_duplicatas_por_id_e_url(self):
        self.assertEqual(len(remover_duplicatas([VAGA, {**VAGA, "url": "https://example.test/2"}, {**VAGA, "id": "teste-2"}])), 1)

    def test_fluxo_sem_email_nao_persiste_vagas(self):
        with tempfile.TemporaryDirectory() as diretorio, patch.object(main, "VISTAS_PATH", os.path.join(diretorio, "vistas.json")):
            with patch.object(main, "github_vagas", return_value=[VAGA]), patch.object(main, "ATIVAR_GUPY", False), patch.object(main, "ATIVAR_VAGAS_COM", False), patch.object(main, "ATIVAR_PROGRAMATHOR", False), patch.object(main, "MATCH_MINIMO", 0), patch.object(main, "enviar_email") as enviar:
                resultado = main.buscar_e_notificar(enviar=False)
            self.assertEqual(len(resultado["novas"]), 1)
            enviar.assert_not_called()
            self.assertFalse(os.path.exists(main.VISTAS_PATH))

    def test_persiste_apos_envio_confirmado(self):
        with tempfile.TemporaryDirectory() as diretorio, patch.object(main, "VISTAS_PATH", os.path.join(diretorio, "vistas.json")):
            with patch.object(main, "github_vagas", return_value=[VAGA]), patch.object(main, "ATIVAR_GUPY", False), patch.object(main, "ATIVAR_VAGAS_COM", False), patch.object(main, "ATIVAR_PROGRAMATHOR", False), patch.object(main, "MATCH_MINIMO", 0), patch.object(main, "enviar_email", return_value=True):
                main.buscar_e_notificar()
            with open(main.VISTAS_PATH, encoding="utf-8") as arquivo:
                self.assertEqual(json.load(arquivo), ["teste-1"])


if __name__ == "__main__":
    unittest.main()
