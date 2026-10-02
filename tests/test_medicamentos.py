import pytest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import medicamentos as med

ARQUIVO_TESTE = "dados.json"


@pytest.fixture(autouse=True)
def limpar_dados(monkeypatch):
    monkeypatch.setenv("CUIDAMED_STORAGE", "local")
    if os.path.exists(ARQUIVO_TESTE):
        os.remove(ARQUIVO_TESTE)
    yield
    if os.path.exists(ARQUIVO_TESTE):
        os.remove(ARQUIVO_TESTE)


# --- Testes de adicionar ---

def test_adicionar_medicamento_valido():
    resultado = med.adicionar("Losartana", "08:00", 1)
    assert resultado["nome"] == "Losartana"
    assert resultado["horario"] == "08:00"
    assert resultado["doses_por_dia"] == 1


def test_adicionar_persiste_no_arquivo():
    med.adicionar("Omeprazol", "07:30", 1)
    dados = med.carregar_dados()
    assert len(dados) == 1
    assert dados[0]["nome"] == "Omeprazol"


def test_adicionar_multiplos_medicamentos():
    med.adicionar("Med A", "08:00", 1)
    med.adicionar("Med B", "12:00", 2)
    dados = med.carregar_dados()
    assert len(dados) == 2


def test_adicionar_nome_vazio_levanta_erro():
    with pytest.raises(ValueError, match="Nome do medicamento não pode ser vazio"):
        med.adicionar("", "08:00", 1)


def test_adicionar_nome_apenas_espacos_levanta_erro():
    with pytest.raises(ValueError):
        med.adicionar("   ", "08:00", 1)


def test_adicionar_horario_invalido_levanta_erro():
    with pytest.raises(ValueError, match="Horário inválido"):
        med.adicionar("Aspirina", "25:00", 1)


def test_adicionar_horario_formato_errado_levanta_erro():
    with pytest.raises(ValueError):
        med.adicionar("Aspirina", "8h00", 1)


def test_adicionar_doses_zero_levanta_erro():
    with pytest.raises(ValueError, match="Doses por dia deve ser maior que zero"):
        med.adicionar("Aspirina", "08:00", 0)


def test_adicionar_doses_negativas_levanta_erro():
    with pytest.raises(ValueError):
        med.adicionar("Aspirina", "08:00", -1)


# --- Testes de listar ---

def test_listar_vazio():
    resultado = med.listar()
    assert resultado == []


def test_listar_retorna_todos():
    med.adicionar("Med A", "08:00", 1)
    med.adicionar("Med B", "20:00", 2)
    resultado = med.listar()
    assert len(resultado) == 2


# --- Testes de remover ---

def test_remover_medicamento_existente():
    med.adicionar("Rivotril", "22:00", 1)
    removido = med.remover("Rivotril")
    assert removido["nome"] == "Rivotril"
    assert med.listar() == []


def test_remover_case_insensitive():
    med.adicionar("Losartana", "08:00", 1)
    removido = med.remover("losartana")
    assert removido["nome"] == "Losartana"


def test_remover_inexistente_levanta_erro():
    with pytest.raises(ValueError, match="não encontrado"):
        med.remover("MedicamentoFantasma")


def test_remover_nao_afeta_outros():
    med.adicionar("Med A", "08:00", 1)
    med.adicionar("Med B", "12:00", 1)
    med.remover("Med A")
    restantes = med.listar()
    assert len(restantes) == 1
    assert restantes[0]["nome"] == "Med B"


# --- Testes de buscar ---

def test_buscar_encontra_por_nome_exato():
    med.adicionar("Losartana", "08:00", 1)
    resultado = med.buscar("Losartana")
    assert len(resultado) == 1


def test_buscar_encontra_por_substring():
    med.adicionar("Losartana Potássica", "08:00", 1)
    resultado = med.buscar("Losartana")
    assert len(resultado) == 1


def test_buscar_case_insensitive():
    med.adicionar("Omeprazol", "07:30", 1)
    resultado = med.buscar("omeprazol")
    assert len(resultado) == 1


def test_buscar_sem_resultado():
    med.adicionar("Aspirina", "08:00", 1)
    resultado = med.buscar("Rivotril")
    assert resultado == []


def test_buscar_retorna_multiplos():
    med.adicionar("Losartana 25mg", "08:00", 1)
    med.adicionar("Losartana 50mg", "20:00", 1)
    resultado = med.buscar("Losartana")
    assert len(resultado) == 2


# --- Testes de atualizar ---

def test_atualizar_medicamento_existente():
    med.adicionar("Losartana", "08:00", 1)
    atualizado = med.atualizar("Losartana", "Losartana Potássica", "09:00", 2)
    dados = med.listar()

    assert atualizado["nome"] == "Losartana Potássica"
    assert atualizado["horario"] == "09:00"
    assert atualizado["doses_por_dia"] == 2
    assert dados[0]["nome"] == "Losartana Potássica"


def test_atualizar_medicamento_inexistente_levanta_erro():
    with pytest.raises(ValueError, match="não encontrado"):
        med.atualizar("MedicamentoFantasma", "Aspirina", "08:00", 1)
