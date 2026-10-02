import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from estatisticas import contar_medicamentos, total_doses_diarias

MEDICAMENTOS = [
    {"nome": "A", "horario": "08:00", "doses_por_dia": 1},
    {"nome": "B", "horario": "12:00", "doses_por_dia": 3},
]


def test_total_doses_diarias():
    assert total_doses_diarias(MEDICAMENTOS) == 4


def test_total_doses_diarias_vazio():
    assert total_doses_diarias([]) == 0


def test_contar_medicamentos():
    assert contar_medicamentos(MEDICAMENTOS) == 2
