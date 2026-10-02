def total_doses_diarias(medicamentos):
    """Soma o total de doses por dia de todos os medicamentos."""
    return sum(int(medicamento["doses_por_dia"]) for medicamento in medicamentos)


def contar_medicamentos(medicamentos):
    """Retorna a quantidade de medicamentos cadastrados."""
    return len(medicamentos)
