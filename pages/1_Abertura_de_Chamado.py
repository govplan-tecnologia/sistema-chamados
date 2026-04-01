import streamlit as st
from data.salvar_chamados import salvar_chamado
from data.enviar_email import enviar_email_novo_chamado
from utils.styles import aplicar_estilo, mostrar_logo

st.set_page_config(page_title="Abertura de Chamado", layout="centered")

aplicar_estilo()
mostrar_logo()

if "chamado_sucesso" not in st.session_state:
    st.session_state.chamado_sucesso = False

if "chamado_erro" not in st.session_state:
    st.session_state.chamado_erro = ""

st.title("Abertura de Chamado")
st.write("Preencha as informações abaixo para abrir um chamado.")
st.divider()

# MENSAGENS NO TOPO, FORA DO FORM
if st.session_state.chamado_sucesso:
    st.success("✅ Chamado aberto com sucesso!")
    st.session_state.chamado_sucesso = False

if st.session_state.chamado_erro:
    st.error(st.session_state.chamado_erro)
    st.session_state.chamado_erro = ""

with st.form("form_chamado", clear_on_submit=True):
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

    if enviar:
        if not solicitante or not orgao or not descricao:
            st.session_state.chamado_erro = "Preencha pelo menos: Solicitante, Órgão e Descrição."
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
            salvar_chamado(dados)

            try:
                enviar_email_novo_chamado(dados)
            except Exception:
                pass

            st.session_state.chamado_sucesso = True
            st.rerun()

        except Exception as e:
            st.session_state.chamado_erro = f"Erro ao salvar o chamado: {e}"
            st.rerun()