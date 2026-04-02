import streamlit as st
import pandas as pd
import plotly.express as px
from utils.styles import aplicar_estilo, mostrar_logo
from data.ler_chamados import ler_chamados

aplicar_estilo()
mostrar_logo()

st.title("Dashboard de Chamados")
st.write("Acompanhe os principais indicadores dos chamados.")
st.divider()

df = ler_chamados()

if df.empty:
    st.warning("Nenhum chamado registrado ainda.")
else:
    df = df.copy()
    if "status" not in df.columns:
        df["status"] = "Aguardando abertura"
    if "categoria" not in df.columns:
        df["categoria"] = "Não informado"

    df["status"] = df["status"].fillna("").astype(str).str.strip()
    df["categoria"] = df["categoria"].fillna("").astype(str).str.strip()
    df.loc[df["status"] == "", "status"] = "Aguardando abertura"
    df.loc[df["categoria"] == "", "categoria"] = "Não informado"

    if "data_abertura" in df.columns:
        df["data_abertura"] = pd.to_datetime(df["data_abertura"], errors="coerce", dayfirst=True)
    if "data_fechamento" in df.columns:
        df["data_fechamento"] = pd.to_datetime(df["data_fechamento"], errors="coerce", dayfirst=True)
    else:
        df["data_fechamento"] = pd.NaT

    total_chamados = int(len(df))
    aguardando = int((df["status"] == "Aguardando abertura").sum())
    aberto = int((df["status"] == "Aberto").sum())
    finalizado = int((df["status"] == "Finalizado").sum())

    chamados_por_status = df["status"].value_counts().reset_index()
    chamados_por_status.columns = ["status", "quantidade"]
    chamados_por_categoria = df["categoria"].value_counts().reset_index()
    chamados_por_categoria.columns = ["categoria", "quantidade"]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div style="background-color:#132A63;padding:20px;border-radius:16px;text-align:center;color:white;min-height:130px;display:flex;flex-direction:column;justify-content:center;">
            <div style="font-size:18px;font-weight:600;color:white;">Total</div>
            <div style="font-size:42px;font-weight:700;color:#7EDC12;margin-top:10px;">{total_chamados}</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div style="background-color:#EAF0FA;padding:20px;border-radius:16px;text-align:center;min-height:130px;display:flex;flex-direction:column;justify-content:center;">
            <div style="font-size:18px;font-weight:600;color:#132A63;">Aguardando</div>
            <div style="font-size:42px;font-weight:700;color:#C79200;margin-top:10px;">{aguardando}</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div style="background-color:#EAF0FA;padding:20px;border-radius:16px;text-align:center;min-height:130px;display:flex;flex-direction:column;justify-content:center;">
            <div style="font-size:18px;font-weight:600;color:#132A63;">Aberto</div>
            <div style="font-size:42px;font-weight:700;color:#1E88E5;margin-top:10px;">{aberto}</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div style="background-color:#EAF0FA;padding:20px;border-radius:16px;text-align:center;min-height:130px;display:flex;flex-direction:column;justify-content:center;">
            <div style="font-size:18px;font-weight:600;color:#132A63;">Finalizado</div>
            <div style="font-size:42px;font-weight:700;color:#2E7D32;margin-top:10px;">{finalizado}</div></div>""", unsafe_allow_html=True)

    st.write("")
    st.write("")

    df_finalizados = df.dropna(subset=["data_fechamento", "data_abertura"]).copy()
    if not df_finalizados.empty:
        df_finalizados["tempo_resolucao"] = (df_finalizados["data_fechamento"] - df_finalizados["data_abertura"]).dt.days
        media_tempo = df_finalizados["tempo_resolucao"].mean()
        st.markdown(f"""<div style="background-color:#DFF5BF;padding:18px;border-radius:16px;text-align:center;color:#132A63;margin-bottom:25px;">
            <div style="font-size:18px;font-weight:600;">⏱ Média de dias para fechamento</div>
            <div style="font-size:34px;font-weight:700;margin-top:8px;">{round(media_tempo, 2)}</div></div>""", unsafe_allow_html=True)
    else:
        st.info("Ainda não há chamados finalizados com data de fechamento preenchida.")

    col_graf1, col_graf2 = st.columns(2)
    with col_graf1:
        st.subheader("Status dos chamados")
        fig_status = px.pie(chamados_por_status, names="status", values="quantidade", hole=0.45, color="status",
            color_discrete_map={"Aguardando abertura": "#F4C542", "Aberto": "#5DADE2", "Finalizado": "#7EDC12", "Não informado": "#D9D9D9"})
        fig_status.update_layout(height=360, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="#F4F7FB", plot_bgcolor="#F4F7FB", font=dict(color="#132A63"))
        st.plotly_chart(fig_status, use_container_width=True)

    with col_graf2:
        st.subheader("Chamados por categoria")
        fig_categoria = px.pie(chamados_por_categoria, names="categoria", values="quantidade", hole=0.45, color="categoria",
            color_discrete_sequence=["#132A63", "#7EDC12", "#A9D18E", "#D9D9D9"])
        fig_categoria.update_layout(height=360, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="#F4F7FB", plot_bgcolor="#F4F7FB", font=dict(color="#132A63"))
        st.plotly_chart(fig_categoria, use_container_width=True)