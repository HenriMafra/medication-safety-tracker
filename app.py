import os

import streamlit as st

from src.api import buscar_info_medicamento
from src.medicamentos import adicionar, atualizar, buscar, listar, modo_armazenamento, remover


def aplicar_segredos_streamlit():
    for chave in (
        "SUPABASE_URL",
        "SUPABASE_KEY",
        "SUPABASE_ANON_KEY",
        "CUIDAMED_STORAGE",
    ):
        if os.getenv(chave):
            continue

        try:
            valor = st.secrets.get(chave)
        except Exception:
            valor = None

        if valor:
            os.environ[chave] = str(valor)


def carregar_medicamentos():
    try:
        return listar(), None
    except RuntimeError as erro:
        return [], str(erro)


def renderizar_lista(medicamentos):
    if not medicamentos:
        st.info("Nenhum medicamento cadastrado ainda.")
        return

    for medicamento in medicamentos:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        col1.write(f"**{medicamento['nome']}**")
        col2.write(medicamento["horario"])
        col3.write(f"{medicamento['doses_por_dia']}x por dia")

        if col4.button("🗑️", key=f"rem_{medicamento['nome']}"):
            try:
                remover(medicamento["nome"])
                st.success("Medicamento removido.")
                st.rerun()
            except (RuntimeError, ValueError) as erro:
                st.error(str(erro))


def renderizar_adicao():
    st.subheader("Adicionar medicamento")
    with st.form("form_adicionar"):
        nome = st.text_input("Nome do medicamento")
        horario = st.text_input("Horário (ex: 08:00)")
        doses = st.number_input("Doses por dia", min_value=1, max_value=10, value=1)
        enviado = st.form_submit_button("Adicionar")

    if enviado:
        try:
            adicionar(nome, horario, int(doses))
            st.success(f"'{nome}' adicionado com sucesso!")
            st.rerun()
        except (RuntimeError, ValueError) as erro:
            st.error(str(erro))


def renderizar_busca():
    st.subheader("Buscar medicamento")
    termo = st.text_input("Digite o nome ou parte do nome")
    if not termo:
        return

    try:
        encontrados = buscar(termo)
    except RuntimeError as erro:
        st.error(str(erro))
        return

    if encontrados:
        for medicamento in encontrados:
            st.write(
                f"**{medicamento['nome']}** — "
                f"{medicamento['horario']} — "
                f"{medicamento['doses_por_dia']}x/dia"
            )
    else:
        st.warning("Nenhum medicamento encontrado.")


def renderizar_atualizacao(medicamentos):
    st.subheader("Atualizar medicamento")
    if not medicamentos:
        st.info("Cadastre um medicamento antes de atualizar.")
        return

    nomes = [medicamento["nome"] for medicamento in medicamentos]
    nome_atual = st.selectbox("Medicamento", nomes)
    medicamento = next(item for item in medicamentos if item["nome"] == nome_atual)

    with st.form("form_atualizar"):
        novo_nome = st.text_input("Novo nome", value=medicamento["nome"])
        novo_horario = st.text_input("Novo horário", value=medicamento["horario"])
        novas_doses = st.number_input(
            "Novas doses por dia",
            min_value=1,
            max_value=10,
            value=int(medicamento["doses_por_dia"]),
        )
        enviado = st.form_submit_button("Atualizar")

    if enviado:
        try:
            atualizar(nome_atual, novo_nome, novo_horario, int(novas_doses))
            st.success("Medicamento atualizado.")
            st.rerun()
        except (RuntimeError, ValueError) as erro:
            st.error(str(erro))


def renderizar_api():
    st.subheader("Consultar informações (OpenFDA)")
    st.caption("Busca informações na base pública da FDA. Use nomes em inglês.")
    nome_api = st.text_input("Nome do medicamento (ex: Aspirin, Ibuprofen)")

    if not st.button("Consultar"):
        return

    if not nome_api:
        st.error("Digite o nome de um medicamento.")
        return

    with st.spinner("Consultando OpenFDA..."):
        info = buscar_info_medicamento(nome_api)

    if info and "erro" not in info:
        st.success("Informações encontradas!")
        col_a, col_b = st.columns(2)
        col_a.metric("Nome genérico", ", ".join(info["nomes_genericos"]))
        col_b.metric("Via", ", ".join(info["via_administracao"]))
        st.write(f"**Fabricante:** {', '.join(info['fabricante'])}")
        with st.expander("Indicações"):
            st.write(info["indicacoes"][0])
        with st.expander("Advertências"):
            st.write(info["advertencias"][0])
    elif info and "erro" in info:
        st.error(info["erro"])
    else:
        st.warning("Nenhuma informação encontrada.")


aplicar_segredos_streamlit()

st.set_page_config(page_title="CuidaMed", page_icon="💊", layout="centered")
st.title("💊 CuidaMed")
st.caption("Gerenciador de horários de medicamentos")
st.info(f"Armazenamento atual: {modo_armazenamento()}")

medicamentos, erro_carregamento = carregar_medicamentos()
if erro_carregamento:
    st.error(erro_carregamento)

aba = st.tabs(["Medicamentos", "Adicionar", "Buscar", "Atualizar", "Consultar API"])

with aba[0]:
    st.subheader("Medicamentos cadastrados")
    renderizar_lista(medicamentos)

with aba[1]:
    renderizar_adicao()

with aba[2]:
    renderizar_busca()

with aba[3]:
    renderizar_atualizacao(medicamentos)

with aba[4]:
    renderizar_api()
