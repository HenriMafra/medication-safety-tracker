import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from alertas import proximo_medicamento


MEDICAMENTOS = [
    {"nome": "Manha", "horario": "08:00", "doses_por_dia": 1},
    {"nome": "Noite", "horario": "20:00", "doses_por_dia": 1},
]


def test_proximo_durante_o_dia():
    assert proximo_medicamento(MEDICAMENTOS, "10:00")["nome"] == "Noite"


def test_proximo_vira_o_dia():
    assert proximo_medicamento(MEDICAMENTOS, "22:00")["nome"] == "Manha"


def test_proximo_lista_vazia():
    assert proximo_medicamento([], "10:00") is None
