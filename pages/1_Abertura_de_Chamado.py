import streamlit as st
from data.salvar_chamados import salvar_chamado

st.title("Abertura de Chamado")
st.caption("BUILD TESTE 02/04 - DEBUG")
st.write("Preencha as informações abaixo para abrir um chamado.")
st.divider()

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

if enviar:
    st.write("DEBUG 1: clique recebido")

    if not solicitante or not orgao or not descricao:
        st.write("DEBUG 2: faltam campos obrigatórios")
        st.error("Preencha pelo menos: Solicitante, Órgão e Descrição.")
    else:
        st.write("DEBUG 3: validação ok")

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

        st.write("DEBUG 4: antes de salvar")
        st.json(dados)

        try:
            salvar_chamado(dados)
            st.write("DEBUG 5: salvou")
            st.balloons()
            st.warning("TESTE VISUAL: SE VOCÊ ESTÁ VENDO ISSO, O PÓS-SAVE EXECUTOU.")
            st.success("Chamado salvo com sucesso!")
        except Exception as e:
            st.write("DEBUG ERRO:")
            st.exception(e)