import csv
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from exportar import exportar_csv


def test_exportar_csv_cria_arquivo(tmp_path):
    medicamentos = [
        {"nome": "Losartana", "horario": "08:00", "doses_por_dia": 1},
        {"nome": "Omeprazol", "horario": "07:30", "doses_por_dia": 2},
    ]
    caminho = tmp_path / "saida.csv"
    total = exportar_csv(medicamentos, str(caminho))
    assert total == 2
    with open(caminho, encoding="utf-8") as arquivo:
        linhas = list(csv.DictReader(arquivo))
    assert linhas[0]["nome"] == "Losartana"
    assert linhas[1]["doses_por_dia"] == "2"


def test_exportar_csv_lista_vazia(tmp_path):
    caminho = tmp_path / "vazio.csv"
    assert exportar_csv([], str(caminho)) == 0
