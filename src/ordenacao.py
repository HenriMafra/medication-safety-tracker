def ordenar_por_horario(medicamentos):
    """Retorna uma nova lista de medicamentos ordenada por horário (HH:MM)."""
    return sorted(medicamentos, key=lambda medicamento: medicamento["horario"])
