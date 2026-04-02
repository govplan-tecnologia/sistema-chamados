import streamlit as st
import pandas as pd
from utils.styles import aplicar_estilo, mostrar_logo
from data.ler_chamados import ler_chamados

aplicar_estilo()
mostrar_logo()

st.title("Acompanhamento de Chamados")
st.write("Pesquise e filtre seus chamados.")
st.divider()

df = ler_chamados()

if df.empty:
    st.info("Nenhum chamado encontrado.")
else:
    if "data_abertura" in df.columns:
        df["data_abertura"] = pd.to_datetime(df["data_abertura"], errors="coerce", dayfirst=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        nome = st.text_input("Solicitante")
    with col2:
        numero = st.text_input("Nº do chamado")
    with col3:
        status = st.selectbox(
            "Status",
            ["Todos"] + sorted(df["status"].dropna().astype(str).unique().tolist())
            if "status" in df.columns else ["Todos"]
        )

    col4, col5 = st.columns(2)
    with col4:
        data_inicio = st.date_input("Data inicial", value=None)
    with col5:
        data_fim = st.date_input("Data final", value=None)

    resultado = df.copy()
    if nome:
        resultado = resultado[resultado["solicitante"].astype(str).str.contains(nome, case=False, na=False)]
    if numero:
        resultado = resultado[resultado["numero_chamado_externo"].astype(str).str.contains(numero, case=False, na=False)]
    if status != "Todos":
        resultado = resultado[resultado["status"].astype(str) == status]
    if data_inicio and "data_abertura" in resultado.columns:
        resultado = resultado[resultado["data_abertura"].dt.date >= data_inicio]
    if data_fim and "data_abertura" in resultado.columns:
        resultado = resultado[resultado["data_abertura"].dt.date <= data_fim]

    if resultado.empty:
        st.info("Nenhum chamado encontrado com esses filtros.")
    else:
        st.success(f"{len(resultado)} chamado(s) encontrado(s)")
        if "data_abertura" in resultado.columns:
            resultado["Data"] = resultado["data_abertura"].dt.strftime("%d/%m/%Y")
        resultado = resultado.rename(columns={
            "solicitante": "Solicitante", "categoria": "Categoria",
            "status": "Status", "numero_chamado_externo": "Nº Chamado",
            "orgao": "Órgão", "login": "Login", "url": "URL",
            "link_gravacao": "Gravação", "descricao": "Descrição", "anexo": "Anexo"
        })
        colunas = ["Data", "Solicitante", "Categoria", "Status", "Nº Chamado", "Órgão", "Descrição", "Login", "URL", "Gravação"]
        colunas = [c for c in colunas if c in resultado.columns]
        resultado = resultado[colunas].copy()

        def cor_status(valor):
            valor = str(valor).strip().lower()
            if valor == "finalizado":
                return "background-color: #D9F2D9; color: #1B5E20; font-weight: bold;"
            elif valor == "aberto":
                return "background-color: #DCEBFF; color: #0D47A1; font-weight: bold;"
            elif valor == "aguardando abertura":
                return "background-color: #FFF4CC; color: #8A6D00; font-weight: bold;"
            return ""

        styled_df = resultado.style.map(cor_status, subset=["Status"])
        st.dataframe(styled_df, use_container_width=True, hide_index=True)