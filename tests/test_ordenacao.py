import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ordenacao import ordenar_por_horario


def test_ordenar_por_horario():
    medicamentos = [
        {"nome": "B", "horario": "20:00", "doses_por_dia": 1},
        {"nome": "A", "horario": "06:00", "doses_por_dia": 1},
    ]
    ordenado = ordenar_por_horario(medicamentos)
    assert [m["nome"] for m in ordenado] == ["A", "B"]


def test_ordenar_nao_altera_lista_original():
    medicamentos = [{"nome": "B", "horario": "20:00", "doses_por_dia": 1}]
    ordenar_por_horario(medicamentos)
    assert medicamentos[0]["nome"] == "B"
