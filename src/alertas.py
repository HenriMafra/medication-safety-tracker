def proximo_medicamento(medicamentos, hora_atual):
    """Retorna o proximo medicamento a tomar a partir de hora_atual (HH:MM).

    Se nao houver horario posterior no dia, retorna o primeiro do dia seguinte.
    Retorna None se a lista estiver vazia.
    """
    if not medicamentos:
        return None

    ordenados = sorted(medicamentos, key=lambda medicamento: medicamento["horario"])
    for medicamento in ordenados:
        if medicamento["horario"] >= hora_atual:
            return medicamento

    return ordenados[0]
