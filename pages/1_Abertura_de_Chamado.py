import streamlit as st
from datetime import datetime
from data.salvar_chamados import salvar_chamado
from utils.styles import aplicar_estilo, mostrar_logo

aplicar_estilo()
mostrar_logo()

st.title("Abertura de Chamado")
st.write("Preencha as informações abaixo para abrir um chamado.")
st.divider()

if "mensagem_sucesso" not in st.session_state:
    st.session_state.mensagem_sucesso = ""

# mostra a mensagem no topo, antes do formulário
if st.session_state.mensagem_sucesso:
    st.success(st.session_state.mensagem_sucesso)
    st.session_state.mensagem_sucesso = ""

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
        st.error("Preencha pelo menos: Solicitante, Órgão e Descrição.")
    else:
        nome_anexo = anexo.name if anexo else ""

        dados = {
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "solicitante": solicitante,
            "categoria": categoria,
            "orgao": orgao,
            "login": login,
            "url": url,
            "link_gravacao": link_gravacao,
            "descricao": descricao,
            "status": "Aguardando abertura",
            "anexo": nome_anexo
        }

        try:
            salvar_chamado(dados)
            st.session_state.mensagem_sucesso = "Chamado salvo com sucesso!"
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao salvar o chamado: {e}")