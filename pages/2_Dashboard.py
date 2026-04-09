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
    if "criticidade" not in df.columns:
        df["criticidade"] = "Não informada"

    df["status"] = df["status"].fillna("").astype(str).str.strip()
    df["categoria"] = df["categoria"].fillna("").astype(str).str.strip()
    df["criticidade"] = df["criticidade"].fillna("").astype(str).str.strip()

    df.loc[df["status"] == "", "status"] = "Aguardando abertura"
    df.loc[df["categoria"] == "", "categoria"] = "Não informado"
    df.loc[df["criticidade"] == "", "criticidade"] = "Não informada"

    if "data_abertura" in df.columns:
        df["data_abertura"] = pd.to_datetime(
            df["data_abertura"],
            errors="coerce",
            dayfirst=True
        )

    if "data_fechamento" in df.columns:
        df["data_fechamento"] = pd.to_datetime(
            df["data_fechamento"],
            errors="coerce",
            dayfirst=True
        )
    else:
        df["data_fechamento"] = pd.NaT

    total_chamados = int(len(df))
    aguardando = int((df["status"] == "Aguardando abertura").sum())
    aberto = int((df["status"] == "Aberto").sum())
    finalizado = int((df["status"] == "Finalizado").sum())

    chamados_por_status = df["status"].value_counts().reset_index()
    chamados_por_status.columns = ["status", "quantidade"]

    ordem_status = ["Aguardando abertura", "Aberto", "Finalizado", "Não informado"]
    chamados_por_status["status"] = pd.Categorical(
        chamados_por_status["status"],
        categories=ordem_status,
        ordered=True
    )
    chamados_por_status = chamados_por_status.sort_values("status")

    chamados_por_categoria = df["categoria"].value_counts().reset_index()
    chamados_por_categoria.columns = ["categoria", "quantidade"]

    ordem_criticidade = [
        "1 - Crítico",
        "2 - Alto",
        "3 - Médio",
        "4 - Baixo"
    ]

    df_criticidade = df[df["criticidade"] != "Não informada"].copy()

    chamados_por_criticidade = df_criticidade["criticidade"].value_counts().reset_index()
    chamados_por_criticidade.columns = ["criticidade", "quantidade"]
    chamados_por_criticidade["criticidade"] = pd.Categorical(
        chamados_por_criticidade["criticidade"],
        categories=ordem_criticidade,
        ordered=True
    )
    chamados_por_criticidade = chamados_por_criticidade.sort_values("criticidade")

    COR_FUNDO = "rgba(0,0,0,0)"
    COR_FONTE = "#132A63"
    COR_GRID = "rgba(19, 42, 99, 0.08)"

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #132A63 0%, #1E3A8A 100%);
                padding:20px;
                border-radius:18px;
                text-align:center;
                color:white;
                min-height:130px;
                display:flex;
                flex-direction:column;
                justify-content:center;
                box-shadow:0 4px 14px rgba(0,0,0,0.08);
            ">
                <div style="font-size:18px;font-weight:600;color:white;">Total</div>
                <div style="font-size:42px;font-weight:700;color:#FFFFFF;margin-top:10px;">{total_chamados}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="
                background:#FFFFFF;
                padding:20px;
                border-radius:18px;
                text-align:center;
                min-height:130px;
                display:flex;
                flex-direction:column;
                justify-content:center;
                border:1px solid #E8EEF7;
                box-shadow:0 4px 14px rgba(0,0,0,0.05);
            ">
                <div style="font-size:18px;font-weight:600;color:#132A63;">Aguardando</div>
                <div style="font-size:42px;font-weight:700;color:#FBC02D;margin-top:10px;">{aguardando}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div style="
                background:#FFFFFF;
                padding:20px;
                border-radius:18px;
                text-align:center;
                min-height:130px;
                display:flex;
                flex-direction:column;
                justify-content:center;
                border:1px solid #E8EEF7;
                box-shadow:0 4px 14px rgba(0,0,0,0.05);
            ">
                <div style="font-size:18px;font-weight:600;color:#132A63;">Aberto</div>
                <div style="font-size:42px;font-weight:700;color:#1E88E5;margin-top:10px;">{aberto}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div style="
                background:#FFFFFF;
                padding:20px;
                border-radius:18px;
                text-align:center;
                min-height:130px;
                display:flex;
                flex-direction:column;
                justify-content:center;
                border:1px solid #E8EEF7;
                box-shadow:0 4px 14px rgba(0,0,0,0.05);
            ">
                <div style="font-size:18px;font-weight:600;color:#132A63;">Finalizado</div>
                <div style="font-size:42px;font-weight:700;color:#2E7D32;margin-top:10px;">{finalizado}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    df_finalizados = df.dropna(subset=["data_fechamento", "data_abertura"]).copy()
    if not df_finalizados.empty:
        df_finalizados["tempo_resolucao"] = (
            df_finalizados["data_fechamento"] - df_finalizados["data_abertura"]
        ).dt.days

        media_tempo = df_finalizados["tempo_resolucao"].mean()

        st.markdown(
            f"""
            <div style="
                background:#FFFFFF;
                padding:18px;
                border-radius:18px;
                text-align:center;
                color:#132A63;
                margin-bottom:25px;
                border:1px solid #E8EEF7;
                box-shadow:0 4px 14px rgba(0,0,0,0.05);
            ">
                <div style="font-size:18px;font-weight:600;">⏱ Média de dias para fechamento</div>
                <div style="font-size:34px;font-weight:700;margin-top:8px;">{round(media_tempo, 2)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.info("Ainda não há chamados finalizados com data de fechamento preenchida.")

    if not chamados_por_criticidade.empty:
        st.subheader("Chamados por criticidade")
        fig_criticidade = px.bar(
            chamados_por_criticidade,
            x="criticidade",
            y="quantidade",
            color="criticidade",
            text="quantidade",
            category_orders={"criticidade": ordem_criticidade},
            color_discrete_map={
                "1 - Crítico": "#D32F2F",
                "2 - Alto": "#F57C00",
                "3 - Médio": "#FBC02D",
                "4 - Baixo": "#2E7D32"
            }
        )
        fig_criticidade.update_traces(
            textposition="outside",
            marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>Quantidade: %{y}<extra></extra>"
        )
        fig_criticidade.update_layout(
            height=430,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor=COR_FUNDO,
            plot_bgcolor="#FFFFFF",
            font=dict(color=COR_FONTE),
            xaxis_title="Criticidade",
            yaxis_title="Quantidade",
            legend_title="Criticidade",
            bargap=0.45
        )
        fig_criticidade.update_xaxes(
            showgrid=False,
            linecolor="rgba(0,0,0,0)",
            tickfont=dict(size=12)
        )
        fig_criticidade.update_yaxes(
            showgrid=True,
            gridcolor=COR_GRID,
            zeroline=False
        )
        st.plotly_chart(fig_criticidade, use_container_width=True)

    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        st.subheader("Status dos chamados")
        fig_status = px.bar(
            chamados_por_status,
            x="quantidade",
            y="status",
            orientation="h",
            color="status",
            text="quantidade",
            category_orders={"status": ordem_status},
            color_discrete_map={
                "Aguardando abertura": "#FBC02D",
                "Aberto": "#1E88E5",
                "Finalizado": "#2E7D32",
                "Não informado": "#BDBDBD"
            }
        )
        fig_status.update_traces(
            textposition="outside",
            marker_line_width=0,
            hovertemplate="<b>%{y}</b><br>Quantidade: %{x}<extra></extra>"
        )
        fig_status.update_layout(
            height=380,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor=COR_FUNDO,
            plot_bgcolor="#FFFFFF",
            font=dict(color=COR_FONTE),
            xaxis_title="Quantidade",
            yaxis_title="",
            showlegend=False,
            bargap=0.35
        )
        fig_status.update_xaxes(
            showgrid=True,
            gridcolor=COR_GRID,
            zeroline=False
        )
        fig_status.update_yaxes(
            showgrid=False,
            autorange="reversed"
        )
        st.plotly_chart(fig_status, use_container_width=True)

    with col_graf2:
        st.subheader("Chamados por categoria")
        fig_categoria = px.pie(
            chamados_por_categoria,
            names="categoria",
            values="quantidade",
            hole=0.58,
            color="categoria",
            color_discrete_sequence=[
                "#132A63",
                "#2E7D32",
                "#42A5F5",
                "#8BC34A",
                "#BDBDBD"
            ]
        )
        fig_categoria.update_traces(
            textinfo="percent+label",
            pull=[0.02] * len(chamados_por_categoria),
            marker=dict(line=dict(color="#FFFFFF", width=2)),
            hovertemplate="<b>%{label}</b><br>Quantidade: %{value}<br>Percentual: %{percent}<extra></extra>"
        )
        fig_categoria.update_layout(
            height=380,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor=COR_FUNDO,
            plot_bgcolor="#FFFFFF",
            font=dict(color=COR_FONTE),
            legend_title="Categoria"
        )
        st.plotly_chart(fig_categoria, use_container_width=True)