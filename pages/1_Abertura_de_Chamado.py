import streamlit as st
from data.salvar_chamados import salvar_chamado
# from utils.styles import aplicar_estilo, mostrar_logo

# aplicar_estilo()
# mostrar_logo()

if "chamado_salvo_ok" not in st.session_state:
    st.session_state["chamado_salvo_ok"] = False

st.title("Abertura de Chamado")
st.caption("BUILD TESTE 01/04 - MSG OK")
st.write("Preencha as informações abaixo para abrir um chamado.")
st.divider()

if st.session_state["chamado_salvo_ok"]:
    st.markdown(
        """
        <div style="
            background-color:#d1fae5;
            color:#065f46;
            padding:14px 16px;
            border-radius:10px;
            border:1px solid #a7f3d0;
            font-weight:600;
            margin-bottom:16px;
        ">
            Chamado salvo com sucesso!
        </div>
        """,
        unsafe_allow_html=True
    )
    st.session_state["chamado_salvo_ok"] = False

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
        st.markdown(
            """
            <div style="
                background-color:#fee2e2;
                color:#991b1b;
                padding:14px 16px;
                border-radius:10px;
                border:1px solid #fecaca;
                font-weight:600;
                margin-top:16px;
            ">
                Preencha pelo menos: Solicitante, Órgão e Descrição.
            </div>
            """,
            unsafe_allow_html=True
        )
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
            st.session_state["chamado_salvo_ok"] = True
            st.rerun()
        except Exception as e:
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
                    Erro ao salvar o chamado: {e}
                </div>
                """,
                unsafe_allow_html=True
            )