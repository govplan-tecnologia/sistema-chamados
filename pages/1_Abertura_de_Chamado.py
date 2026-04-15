import streamlit as st
from data.salvar_chamados import salvar_chamado
from data.enviar_email import enviar_email_novo_chamado
from utils.styles import aplicar_estilo, mostrar_logo

st.set_page_config(page_title="Abertura de Chamado", layout="centered")

aplicar_estilo()
mostrar_logo()

st.title("Abertura de Chamado")
st.write("Preencha as informações abaixo para abrir um chamado.")
st.divider()

if "sucesso" not in st.session_state:
    st.session_state.sucesso = False

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

    criticidade = st.selectbox(
        "Criticidade",
        [
            "4 - Baixo",
            "3 - Médio",
            "2 - Alto",
            "1 - Crítico"
        ],
        help=(
            "Classifique o impacto do incidente: "
            "1-Crítico = sistema indisponível ou falha grave; "
            "2-Alto = funcionalidade essencial afetada; "
            "3-Médio = impacto parcial; "
            "4-Baixo = dúvidas, ajustes ou melhorias."
        )
    )

    descricao = st.text_area("Descrição")

    anexos = st.file_uploader(
        "Anexar arquivos (opcional)",
        type=[
            "png", "jpg", "jpeg",
            "pdf",
            "xlsx", "xls", "csv",
            "doc", "docx",
            "txt"
        ],
        accept_multiple_files=True,
        help="Você pode enviar uma ou mais imagens, planilhas, PDFs ou documentos."
    )

    enviar = st.form_submit_button("Abrir chamado")

if st.session_state.sucesso:
    st.success("✅ Chamado aberto com sucesso!")
    st.session_state.sucesso = False

if enviar:
    if not solicitante or not orgao or not descricao:
        st.error("Preencha pelo menos: Solicitante, Órgão e Descrição.")
    else:
        dados = {
            "solicitante": solicitante,
            "categoria": categoria,
            "orgao": orgao,
            "login": login,
            "url": url,
            "link_gravacao": link_gravacao,
            "criticidade": criticidade,
            "descricao": descricao,
            "anexos": anexos
        }

        try:
            resultado = salvar_chamado(dados)

            try:
                enviar_email_novo_chamado(dados)
            except Exception as e:
                st.warning(f"O chamado foi salvo, mas o e-mail falhou: {e}")

            if resultado:
                st.session_state.sucesso = True
                st.rerun()

        except Exception as e:
            st.error(f"Erro ao salvar o chamado: {e}")
            st.exception(e)