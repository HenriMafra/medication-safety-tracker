import os
from typing import Any, Optional

TABELA_MEDICAMENTOS = "medicamentos"
COLUNAS_MEDICAMENTOS = "id,nome,horario,doses_por_dia,created_at,updated_at"


class SupabaseConfigError(RuntimeError):
    """Erro de configuração do Supabase."""


def obter_configuracao() -> tuple[str, str]:
    url = os.getenv("SUPABASE_URL", "").strip()
    chave = (
        os.getenv("SUPABASE_KEY", "").strip()
        or os.getenv("SUPABASE_ANON_KEY", "").strip()
        or os.getenv("SUPABASE_PUBLISHABLE_KEY", "").strip()
    )

    if not url or not chave:
        raise SupabaseConfigError(
            "Configure SUPABASE_URL e SUPABASE_KEY para usar o banco Supabase."
        )

    return url, chave


def supabase_configurado() -> bool:
    try:
        obter_configuracao()
        return True
    except SupabaseConfigError:
        return False


def criar_cliente():
    from supabase import create_client

    url, chave = obter_configuracao()
    return create_client(url, chave)


def _normalizar_horario(valor: Any) -> str:
    texto = str(valor)
    if len(texto) >= 5:
        return texto[:5]
    return texto


def normalizar_medicamento(registro: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": registro.get("id"),
        "nome": registro["nome"],
        "horario": _normalizar_horario(registro["horario"]),
        "doses_por_dia": int(registro["doses_por_dia"]),
        "created_at": registro.get("created_at"),
        "updated_at": registro.get("updated_at"),
    }


def _dados_resposta(resposta) -> list[dict[str, Any]]:
    dados = getattr(resposta, "data", None)
    return dados or []


def _executar(consulta):
    try:
        return consulta.execute()
    except Exception as erro:
        raise RuntimeError(f"Erro ao acessar o Supabase: {erro}")


def listar_medicamentos(cliente=None) -> list[dict[str, Any]]:
    cliente = cliente or criar_cliente()
    resposta = _executar(
        cliente.table(TABELA_MEDICAMENTOS)
        .select(COLUNAS_MEDICAMENTOS)
        .order("nome")
    )
    return [normalizar_medicamento(item) for item in _dados_resposta(resposta)]


def adicionar_medicamento(medicamento: dict[str, Any], cliente=None) -> dict[str, Any]:
    cliente = cliente or criar_cliente()
    resposta = _executar(
        cliente.table(TABELA_MEDICAMENTOS)
        .insert(medicamento)
        .select(COLUNAS_MEDICAMENTOS)
    )
    dados = _dados_resposta(resposta)
    if not dados:
        raise RuntimeError("O Supabase não retornou o medicamento cadastrado.")
    return normalizar_medicamento(dados[0])


def buscar_medicamentos(termo: str, cliente=None) -> list[dict[str, Any]]:
    cliente = cliente or criar_cliente()
    resposta = _executar(
        cliente.table(TABELA_MEDICAMENTOS)
        .select(COLUNAS_MEDICAMENTOS)
        .ilike("nome", f"%{termo}%")
        .order("nome")
    )
    return [normalizar_medicamento(item) for item in _dados_resposta(resposta)]


def buscar_medicamento_exato(nome: str, cliente=None) -> Optional[dict[str, Any]]:
    cliente = cliente or criar_cliente()
    resposta = _executar(
        cliente.table(TABELA_MEDICAMENTOS)
        .select(COLUNAS_MEDICAMENTOS)
        .ilike("nome", nome)
        .limit(1)
    )
    dados = _dados_resposta(resposta)
    if not dados:
        return None
    return normalizar_medicamento(dados[0])


def remover_medicamento(nome: str, cliente=None) -> Optional[dict[str, Any]]:
    cliente = cliente or criar_cliente()
    medicamento = buscar_medicamento_exato(nome, cliente=cliente)
    if not medicamento:
        return None

    _executar(cliente.table(TABELA_MEDICAMENTOS).delete().eq("id", medicamento["id"]))
    return medicamento


def atualizar_medicamento(
    nome_atual: str,
    novos_dados: dict[str, Any],
    cliente=None,
) -> Optional[dict[str, Any]]:
    cliente = cliente or criar_cliente()
    medicamento = buscar_medicamento_exato(nome_atual, cliente=cliente)
    if not medicamento:
        return None

    resposta = _executar(
        cliente.table(TABELA_MEDICAMENTOS)
        .update(novos_dados)
        .eq("id", medicamento["id"])
        .select(COLUNAS_MEDICAMENTOS)
    )
    dados = _dados_resposta(resposta)
    if not dados:
        return None
    return normalizar_medicamento(dados[0])
