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

# ✅ Inicializa o estado da mensagem
if "mensagem" not in st.session_state:
    st.session_state.mensagem = None
if "mensagem_tipo" not in st.session_state:
    st.session_state.mensagem_tipo = None

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
        # ✅ Salva o erro no session_state
        st.session_state.mensagem = "Preencha pelo menos: Solicitante, Órgão e Descrição."
        st.session_state.mensagem_tipo = "erro"
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
            resultado = salvar_chamado(dados)
            try:
                enviar_email_novo_chamado(dados)
            except Exception:
                pass

            if resultado:
                # ✅ Salva o sucesso no session_state
                st.session_state.mensagem = "Chamado aberto com sucesso!"
                st.session_state.mensagem_tipo = "sucesso"
            else:
                st.session_state.mensagem = "O chamado não foi salvo."
                st.session_state.mensagem_tipo = "erro"

        except Exception as e:
            st.session_state.mensagem = f"Erro ao salvar o chamado: {e}"
            st.session_state.mensagem_tipo = "erro"

# ✅ Exibe a mensagem FORA do formulário, após o rerun
if st.session_state.mensagem:
    if st.session_state.mensagem_tipo == "sucesso":
        st.success(st.session_state.mensagem)
    else:
        st.error(st.session_state.mensagem)
    # Limpa após exibir para não ficar preso na tela
    st.session_state.mensagem = None
    st.session_state.mensagem_tipo = None