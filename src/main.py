from api import buscar_info_medicamento, formatar_info
from medicamentos import adicionar, atualizar, buscar, listar, modo_armazenamento, remover

VERSAO = "2.0.0"


def exibir_menu():
    print("\n" + "=" * 50)
    print(f"  CuidaMed v{VERSAO} - Gerenciador de Medicamentos")
    print(f"  Armazenamento: {modo_armazenamento()}")
    print("=" * 50)
    print("  1. Adicionar medicamento")
    print("  2. Listar medicamentos")
    print("  3. Buscar medicamento")
    print("  4. Remover medicamento")
    print("  5. Consultar informacoes do medicamento (OpenFDA)")
    print("  6. Atualizar medicamento")
    print("  0. Sair")
    print("=" * 50)


def pedir_doses():
    while True:
        try:
            return int(input("  Doses por dia: ").strip())
        except ValueError:
            print("  Digite um numero inteiro valido.")


def adicionar_medicamento_cli():
    nome = input("  Nome do medicamento: ").strip()
    horario = input("  Horario inicial (HH:MM): ").strip()
    doses = pedir_doses()

    try:
        adicionar(nome, horario, doses)
        print(f"\n  '{nome}' adicionado com sucesso.")
    except (RuntimeError, ValueError) as erro:
        print(f"\n  Erro ao adicionar: {erro}")


def listar_medicamentos_cli():
    try:
        medicamentos = listar()
    except RuntimeError as erro:
        print(f"\n  Erro ao listar: {erro}")
        return

    if not medicamentos:
        print("\n  Nenhum medicamento cadastrado.")
        return

    print("\n  Medicamentos cadastrados:")
    for medicamento in medicamentos:
        print(
            "  - "
            f"{medicamento['nome']} | "
            f"{medicamento['horario']} | "
            f"{medicamento['doses_por_dia']}x/dia"
        )


def buscar_medicamento_cli():
    termo = input("  Digite o nome ou parte dele: ").strip()
    try:
        encontrados = buscar(termo)
    except RuntimeError as erro:
        print(f"\n  Erro ao buscar: {erro}")
        return

    if not encontrados:
        print("\n  Nenhum medicamento encontrado.")
        return

    print(f"\n  {len(encontrados)} resultado(s) encontrado(s):")
    for medicamento in encontrados:
        print(
            "  - "
            f"{medicamento['nome']} | "
            f"{medicamento['horario']} | "
            f"{medicamento['doses_por_dia']}x/dia"
        )


def remover_medicamento_cli():
    nome = input("  Nome do medicamento para remover: ").strip()

    try:
        remover(nome)
        print(f"\n  '{nome}' removido com sucesso.")
    except (RuntimeError, ValueError) as erro:
        print(f"\n  Erro ao remover: {erro}")


def consultar_api_cli():
    nome = input("  Nome do medicamento para consultar (ex: Aspirin): ").strip()
    if not nome:
        print("\n  Informe um nome para consulta.")
        return

    print("\n  Consultando OpenFDA...")
    info = buscar_info_medicamento(nome)
    if info:
        print(formatar_info(info))
    else:
        print(f"\n  Nenhuma informacao encontrada para '{nome}' na base OpenFDA.")


def atualizar_medicamento_cli():
    nome_atual = input("  Nome atual do medicamento: ").strip()
    novo_nome = input("  Novo nome: ").strip()
    novo_horario = input("  Novo horario inicial (HH:MM): ").strip()
    novas_doses = pedir_doses()

    try:
        atualizar(nome_atual, novo_nome, novo_horario, novas_doses)
        print(f"\n  '{nome_atual}' atualizado com sucesso.")
    except (RuntimeError, ValueError) as erro:
        print(f"\n  Erro ao atualizar: {erro}")


def main():
    while True:
        exibir_menu()
        opcao = input("  Escolha uma opcao: ").strip()

        if opcao == "1":
            adicionar_medicamento_cli()
        elif opcao == "2":
            listar_medicamentos_cli()
        elif opcao == "3":
            buscar_medicamento_cli()
        elif opcao == "4":
            remover_medicamento_cli()
        elif opcao == "5":
            consultar_api_cli()
        elif opcao == "6":
            atualizar_medicamento_cli()
        elif opcao == "0":
            print("\n  Encerrando CuidaMed. Ate logo!\n")
            break
        else:
            print("\n  Opcao invalida. Tente novamente.")


if __name__ == "__main__":
    main()
