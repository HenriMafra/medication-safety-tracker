import json
import os
from datetime import datetime
from typing import Any

try:
    import supabase_repository
except ImportError:
    from . import supabase_repository

ARQUIVO = "dados.json"


def modo_armazenamento() -> str:
    modo = os.getenv("CUIDAMED_STORAGE", "").strip().lower()
    if modo in {"local", "json"}:
        return "local"
    if modo == "supabase":
        return "supabase"
    if supabase_repository.supabase_configurado():
        return "supabase"
    return "local"


def usando_supabase() -> bool:
    return modo_armazenamento() == "supabase"


def carregar_dados():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_dados(medicamentos):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(medicamentos, f, ensure_ascii=False, indent=2)


def _validar_medicamento(nome, horario, doses_por_dia) -> dict[str, Any]:
    if not nome or not nome.strip():
        raise ValueError("Nome do medicamento não pode ser vazio.")

    try:
        doses = int(doses_por_dia)
    except (TypeError, ValueError):
        raise ValueError("Doses por dia deve ser um número inteiro.")

    if doses <= 0:
        raise ValueError("Doses por dia deve ser maior que zero.")

    try:
        datetime.strptime(horario, "%H:%M")
    except ValueError:
        raise ValueError("Horário inválido. Use o formato HH:MM.")

    return {
        "nome": nome.strip(),
        "horario": horario,
        "doses_por_dia": doses,
    }


def adicionar(nome, horario, doses_por_dia):
    medicamento = _validar_medicamento(nome, horario, doses_por_dia)

    if usando_supabase():
        return supabase_repository.adicionar_medicamento(medicamento)

    medicamentos = carregar_dados()
    medicamentos.append(medicamento)
    salvar_dados(medicamentos)
    return medicamento


def listar():
    if usando_supabase():
        return supabase_repository.listar_medicamentos()
    return carregar_dados()


def remover(nome):
    if usando_supabase():
        removido = supabase_repository.remover_medicamento(nome)
        if not removido:
            raise ValueError(f"Medicamento '{nome}' não encontrado.")
        return removido

    medicamentos = carregar_dados()
    encontrado = [m for m in medicamentos if m["nome"].lower() == nome.lower()]
    if not encontrado:
        raise ValueError(f"Medicamento '{nome}' não encontrado.")
    atualizados = [m for m in medicamentos if m["nome"].lower() != nome.lower()]
    salvar_dados(atualizados)
    return encontrado[0]


def buscar(nome):
    if usando_supabase():
        return supabase_repository.buscar_medicamentos(nome)

    medicamentos = carregar_dados()
    resultado = [m for m in medicamentos if nome.lower() in m["nome"].lower()]
    return resultado


def atualizar(nome_atual, novo_nome, novo_horario, novas_doses):
    novos_dados = _validar_medicamento(novo_nome, novo_horario, novas_doses)

    if usando_supabase():
        atualizado = supabase_repository.atualizar_medicamento(nome_atual, novos_dados)
        if not atualizado:
            raise ValueError(f"Medicamento '{nome_atual}' não encontrado.")
        return atualizado

    medicamentos = carregar_dados()
    for indice, medicamento in enumerate(medicamentos):
        if medicamento["nome"].lower() == nome_atual.lower():
            medicamentos[indice] = novos_dados
            salvar_dados(medicamentos)
            return novos_dados

    raise ValueError(f"Medicamento '{nome_atual}' não encontrado.")
