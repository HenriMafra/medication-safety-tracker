import os
import sys
from unittest.mock import MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import medicamentos as med
import supabase_repository as repo


def test_modo_armazenamento_usa_supabase_quando_configurado(monkeypatch):
    monkeypatch.delenv("CUIDAMED_STORAGE", raising=False)
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_KEY", "anon-key")

    assert med.modo_armazenamento() == "supabase"


def test_adicionar_medicamento_usa_repositorio_supabase(monkeypatch):
    monkeypatch.setenv("CUIDAMED_STORAGE", "supabase")
    adicionar_mock = MagicMock(
        return_value={
            "id": "1",
            "nome": "Aspirina",
            "horario": "08:00",
            "doses_por_dia": 1,
        }
    )
    monkeypatch.setattr(med.supabase_repository, "adicionar_medicamento", adicionar_mock)

    resultado = med.adicionar("Aspirina", "08:00", 1)

    adicionar_mock.assert_called_once_with(
        {"nome": "Aspirina", "horario": "08:00", "doses_por_dia": 1}
    )
    assert resultado["id"] == "1"


def test_atualizar_medicamento_usa_repositorio_supabase(monkeypatch):
    monkeypatch.setenv("CUIDAMED_STORAGE", "supabase")
    atualizar_mock = MagicMock(
        return_value={
            "id": "1",
            "nome": "Aspirina 100mg",
            "horario": "09:00",
            "doses_por_dia": 2,
        }
    )
    monkeypatch.setattr(med.supabase_repository, "atualizar_medicamento", atualizar_mock)

    resultado = med.atualizar("Aspirina", "Aspirina 100mg", "09:00", 2)

    atualizar_mock.assert_called_once_with(
        "Aspirina",
        {"nome": "Aspirina 100mg", "horario": "09:00", "doses_por_dia": 2},
    )
    assert resultado["nome"] == "Aspirina 100mg"


def test_normalizar_medicamento_do_supabase():
    resultado = repo.normalizar_medicamento(
        {
            "id": "1",
            "nome": "Ibuprofen",
            "horario": "08:30:00",
            "doses_por_dia": "2",
            "created_at": "2026-05-14T00:00:00Z",
            "updated_at": "2026-05-14T00:00:00Z",
        }
    )

    assert resultado["horario"] == "08:30"
    assert resultado["doses_por_dia"] == 2
