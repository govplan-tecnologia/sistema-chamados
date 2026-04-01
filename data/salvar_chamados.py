import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

def salvar_chamado(dados):
    agora_brasil = datetime.now(ZoneInfo("America/Sao_Paulo"))
    
    novo_registro = {
        "data_abertura": agora_brasil.strftime("%d/%m/%Y %H:%M:%S"),
        **dados,
        "status": "Aguardando abertura",
        "numero_chamado_externo": "",
        "observacao_interna": "",
        "data_fechamento": ""
    }

    if "chamados" not in st.session_state:
        st.session_state.chamados = []

    st.session_state.chamados.append(novo_registro)