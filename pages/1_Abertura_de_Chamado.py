import streamlit as st
from data.salvar_chamados import salvar_chamado
from data.enviar_email import enviar_email_novo_chamado
from utils.styles import aplicar_estilo, mostrar_logo

st.set_page_config(page_title="Abertura de Chamado", layout="centered")

aplicar_estilo()
mostrar_logo()

if "mensagem_sucesso" not in st.session_state:
    st.session_state.mensagem_sucesso = False

if "mensagem_erro" not in st.session_state:
    st.session_state.mensagem_erro = ""

st.title("Abertura de Chamado")
st.write("Preencha as informações abaixo para abrir um chamado.")
st.divider()

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
        st.session_state.mensagem_sucesso = False
        st.session_state.mensagem_erro = ""

        if not solicitante or not orgao or not descricao:
            st.session_state.mensagem_erro = "Preencha pelo menos: Solicitante, Órgão e Descrição."
        else:
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

                st.session_state.mensagem_sucesso = True

            except Exception as e:
                st.session_state.mensagem_erro = f"Erro ao salvar o chamado: {e}"

if st.session_state.mensagem_sucesso:
    st.markdown(
        """
        <div style="
            background-color:#d1fae5;
            color:#065f46;
            padding:14px 16px;
            border-radius:10px;
            border:1px solid #a7f3d0;
            font-weight:600;
            margin-top:16px;
        ">
            ✅ Chamado aberto com sucesso!
        </div>
        """,
        unsafe_allow_html=True
    )

if st.session_state.mensagem_erro:
    st.markdown(
        f"""
        <div style="
            background-color:#fee2e2;
            color:#991b1b;
            padding:14px 16px;
            border-radius:10px;
            border:1px solid #fecaca;
            font-weight:600;
            margin-top:16px;
        ">
            {st.session_state.mensagem_erro}
        </div>
        """,
        unsafe_allow_html=True
    )