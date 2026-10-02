import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from api import buscar_info_medicamento, formatar_info


# --- Resposta simulada da API OpenFDA ---
MOCK_RESPONSE = {
    "results": [
        {
            "openfda": {
                "brand_name": ["Aspirin"],
                "generic_name": ["ASPIRIN"],
                "manufacturer_name": ["Bayer"],
                "route": ["ORAL"],
            },
            "indications_and_usage": ["Used to reduce fever and relieve mild to moderate pain."],
            "warnings": ["Do not use in children under 12 years of age."],
        }
    ]
}


def test_buscar_info_medicamento_sucesso():
    """Testa consulta bem-sucedida à API com resposta mockada."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = MOCK_RESPONSE

    with patch("api.requests.get", return_value=mock_resp):
        resultado = buscar_info_medicamento("Aspirin")

    assert resultado is not None
    assert resultado["nome"] == "Aspirin"
    assert "ASPIRIN" in resultado["nomes_genericos"]
    assert "Bayer" in resultado["fabricante"]


def test_buscar_info_medicamento_nao_encontrado():
    """Testa quando a API não retorna resultados."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"results": []}

    with patch("api.requests.get", return_value=mock_resp):
        resultado = buscar_info_medicamento("MedicamentoInexistente")

    assert resultado is None


def test_buscar_info_medicamento_erro_conexao():
    """Testa tratamento de erro de conexão."""
    import requests as req

    with patch("api.requests.get", side_effect=req.exceptions.ConnectionError):
        resultado = buscar_info_medicamento("Aspirin")

    assert resultado is not None
    assert "erro" in resultado
    assert "internet" in resultado["erro"].lower()


def test_buscar_info_medicamento_timeout():
    """Testa tratamento de timeout."""
    import requests as req

    with patch("api.requests.get", side_effect=req.exceptions.Timeout):
        resultado = buscar_info_medicamento("Aspirin")

    assert resultado is not None
    assert "erro" in resultado
    assert "esgotado" in resultado["erro"].lower()


def test_formatar_info_com_dados():
    """Testa formatação da resposta da API."""
    info = {
        "nome": "Aspirin",
        "nomes_genericos": ["ASPIRIN"],
        "fabricante": ["Bayer"],
        "via_administracao": ["ORAL"],
        "indicacoes": ["Used to reduce fever."],
        "advertencias": ["Do not use in children."],
    }
    texto = formatar_info(info)
    assert "ASPIRIN" in texto
    assert "Bayer" in texto
    assert "ORAL" in texto


def test_formatar_info_com_erro():
    """Testa formatação quando há erro."""
    info = {"erro": "Sem conexão com a internet."}
    texto = formatar_info(info)
    assert "Erro" in texto
    assert "internet" in texto
