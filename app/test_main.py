import requests
import unittest
import json


class TestSum(unittest.TestCase):

    def test_api_consulta_dados_corretos(self):
        self.assertNotEqual(json.loads(requests.get('http://localhost:8000/predict/?lat=-22.8232257917&lng=-47.0758807513').json()).get('body'),
                            {"latitude": "-22.8232257917", "longitude": "-47.0758807513",
                                "predicao": "-1", "n_pequeno_varejista": "-1", "n_grandes_redes": "-1"},
                            "DEVERIA retornar 200, POIS os dados passados correspondem ao mapa de campinas")

    def test_api_consulta_dados_errados(self):
        self.assertEqual(json.loads(requests.get('http://localhost:8000/predict/?lat=-22.982356215&lng=-46.9112167395').json()).get('body'),
                         {"latitude": "-22.982356215", "longitude": "-46.9112167395",
                             "predicao": "-1", "n_pequeno_varejista": "-1", "n_grandes_redes": "-1"},
                         "DEVERIA retornar 401, POIS os dados passados não correspondem ao mapa de campinas")


if __name__ == '__main__':
    unittest.main()
