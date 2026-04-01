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

# Estado da mensagem
if "status_banner" not in st.session_state:
    st.session_state.status_banner = ""

if "tipo_banner" not in st.session_state:
    st.session_state.tipo_banner = ""

# Placeholder FIXO no topo
banner_placeholder = st.empty()

def renderizar_banner():
    if st.session_state.status_banner:
        cor_fundo = "#d1fae5" if st.session_state.tipo_banner == "sucesso" else "#fee2e2"
        cor_texto = "#065f46" if st.session_state.tipo_banner == "sucesso" else "#991b1b"
        cor_borda = "#a7f3d0" if st.session_state.tipo_banner == "sucesso" else "#fecaca"

        banner_placeholder.markdown(
            f"""
            <div style="
                background-color:{cor_fundo};
                color:{cor_texto};
                padding:14px 16px;
                border-radius:10px;
                border:1px solid {cor_borda};
                font-weight:600;
                margin-top:16px;
                margin-bottom:16px;
            ">
                {st.session_state.status_banner}
            </div>
            """,
            unsafe_allow_html=True
        )

# Renderiza a mensagem já salva, se existir
renderizar_banner()

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
    if not solicitante or not orgao or not descricao:
        st.session_state.status_banner = "Preencha pelo menos: Solicitante, Órgão e Descrição."
        st.session_state.tipo_banner = "erro"
        renderizar_banner()
        st.stop()

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
            st.session_state.status_banner = "✅ Chamado aberto com sucesso!"
            st.session_state.tipo_banner = "sucesso"
        else:
            st.session_state.status_banner = "O chamado não foi salvo."
            st.session_state.tipo_banner = "erro"

        renderizar_banner()

    except Exception as e:
        st.session_state.status_banner = f"Erro ao salvar o chamado: {e}"
        st.session_state.tipo_banner = "erro"
        renderizar_banner()