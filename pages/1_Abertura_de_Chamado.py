import streamlit as st
from data.salvar_chamados import salvar_chamado
from data.enviar_email import enviar_email_novo_chamado
from utils.styles import aplicar_estilo, mostrar_logo

st.set_page_config(page_title="Abertura de Chamado", layout="centered")

aplicar_estilo()
mostrar_logo()

# 🔹 Controle de mensagem (ESSENCIAL)
if "mostrar_msg" not in st.session_state:
    st.session_state["mostrar_msg"] = False

if "msg" not in st.session_state:
    st.session_state["msg"] = ""

if "tipo" not in st.session_state:
    st.session_state["tipo"] = ""

st.title("Abertura de Chamado")
st.write("Preencha as informações abaixo para abrir um chamado.")
st.divider()

# 🔹 Exibição do banner no topo (ESSENCIAL)
if st.session_state.get("mostrar_msg"):
    if st.session_state.get("tipo") == "sucesso":
        st.success(st.session_state.get("msg"))
    else:
        st.error(st.session_state.get("msg"))

    # limpa depois de mostrar
    st.session_state["mostrar_msg"] = False

# 🔹 Formulário
with st.form("form_chamado", clear_on_submit=False):
    solicitante = st.text_input("Solicitante")
    categoria = st.selectbox(
        "Categoria",
        ["Bug", "Sugestão de melhoria", "Robô de fontes"]
    )
    orgao = st.text_input("Órgão")
    login = st.text_input("Login")
    url = st.text_input("URL")
    link_gravacao = st.text_input("Link da gravação")
    descricao = st.text_area("Descrição")
    anexo = st.file_uploader("Anexo (opcional)")
    enviar = st.form_submit_button("Abrir chamado")

# 🔹 Lógica de envio
if enviar:
    if not solicitante or not orgao or not descricao:
        st.session_state["msg"] = "Preencha pelo menos: Solicitante, Órgão e Descrição."
        st.session_state["tipo"] = "erro"
        st.session_state["mostrar_msg"] = True
        st.rerun()

    nome_anexo = anexo.name if anexo else ""

    dados = {
        "solicitante": solicitante,
        "categoria": categoria,
        "orgao": orgao,
        "login": login,
        "url": url,
        "link_gravacao": link_gravacao,
        "descricao": descricao,
        "anexo": nome_anexo
    }

    try:
        resultado = salvar_chamado(dados)

        try:
            enviar_email_novo_chamado(dados)
        except Exception:
            pass

        if resultado:
            st.session_state["msg"] = "✅ Chamado aberto com sucesso!"
            st.session_state["tipo"] = "sucesso"
        else:
            st.session_state["msg"] = "O chamado não foi salvo."
            st.session_state["tipo"] = "erro"

        st.session_state["mostrar_msg"] = True
        st.rerun()

    except Exception as e:
        st.session_state["msg"] = f"Erro ao salvar o chamado: {e}"
        st.session_state["tipo"] = "erro"
        st.session_state["mostrar_msg"] = True
        st.rerun()