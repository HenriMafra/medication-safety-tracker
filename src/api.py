from typing import Optional

import requests

OPENFDA_URL = "https://api.fda.gov/drug/label.json"


def buscar_info_medicamento(nome: str) -> Optional[dict]:
    """
    Busca informações de um medicamento na API pública OpenFDA.
    Retorna um dicionário com informações ou None se não encontrar.
    """
    try:
        params = {
            "search": f'openfda.brand_name:"{nome}"',
            "limit": 1,
        }
        response = requests.get(OPENFDA_URL, params=params, timeout=5)

        if response.status_code == 200:
            data = response.json()
            resultados = data.get("results", [])
            if not resultados:
                return None

            resultado = resultados[0]
            openfda = resultado.get("openfda", {})

            info = {
                "nome": nome,
                "nomes_genericos": openfda.get("generic_name", ["Não informado"]),
                "fabricante": openfda.get("manufacturer_name", ["Não informado"]),
                "via_administracao": openfda.get("route", ["Não informado"]),
                "indicacoes": resultado.get("indications_and_usage", ["Não disponível"]),
                "advertencias": resultado.get("warnings", ["Não disponível"]),
            }
            return info

        return None

    except requests.exceptions.Timeout:
        return {"erro": "Tempo de conexão esgotado. Verifique sua internet."}
    except requests.exceptions.ConnectionError:
        return {"erro": "Sem conexão com a internet."}
    except Exception as e:
        return {"erro": f"Erro inesperado: {str(e)}"}


def formatar_info(info: dict) -> str:
    """
    Formata as informações do medicamento para exibição no terminal.
    """
    if "erro" in info:
        return f"\n  Erro: {info['erro']}\n"

    def pegar_primeiro(campo):
        valor = info.get(campo, ["Não informado"])
        if isinstance(valor, list) and valor:
            texto = valor[0]
            return texto[:300] + "..." if len(texto) > 300 else texto
        return str(valor)

    genericos = ", ".join(info.get("nomes_genericos", ["Não informado"]))
    fabricante = ", ".join(info.get("fabricante", ["Não informado"]))
    via = ", ".join(info.get("via_administracao", ["Não informado"]))

    linhas = [
        "",
        f"  Medicamento : {info['nome'].upper()}",
        f"  Nome genérico : {genericos}",
        f"  Fabricante    : {fabricante}",
        f"  Via           : {via}",
        "",
        "  Indicações:",
        f"  {pegar_primeiro('indicacoes')}",
        "",
        "  Advertências:",
        f"  {pegar_primeiro('advertencias')}",
        "",
    ]
    return "\n".join(linhas)
