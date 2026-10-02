import csv

def exportar_csv(medicamentos, caminho):
    """Exporta a lista de medicamentos para um arquivo CSV.
    Retorna a quantidade de medicamentos exportados.
    """
    campos = ["nome", "horario", "doses_por_dia"]

    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()

        for medicamento in medicamentos:
            escritor.writerow({campo: medicamento.get(campo, "") for campo in campos})

    return len(medicamentos)
