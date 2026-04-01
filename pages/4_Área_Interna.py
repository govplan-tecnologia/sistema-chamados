import streamlit as st
import pandas as pd
import os
from datetime import datetime
from utils.styles import aplicar_estilo, mostrar_logo

aplicar_estilo()
mostrar_logo()

st.title("Área Interna")
st.write("Use os filtros abaixo para localizar e atualizar chamados.")

st.divider()

CAMINHO_ARQUIVO = "data/chamados.csv"
SENHA_ADMIN = "govplan2026!"

senha = st.text_input("Senha de acesso", type="password")

if senha != SENHA_ADMIN:
    st.warning("Digite a senha para liberar a edição.")
else:
    st.success("Acesso liberado.")

    if not os.path.exists(CAMINHO_ARQUIVO):
        st.warning("Nenhum chamado encontrado.")
    else:
        df = pd.read_csv(CAMINHO_ARQUIVO, encoding="utf-8-sig")

        if df.empty:
            st.info("A base está vazia.")
        else:
            colunas_necessarias = [
                "data_abertura",
                "solicitante",
                "categoria",
                "orgao",
                "login",
                "url",
                "link_gravacao",
                "descricao",
                "anexo",
                "status",
                "numero_chamado_externo",
                "observacao_interna",
                "data_fechamento",
            ]

            for coluna in colunas_necessarias:
                if coluna not in df.columns:
                    df[coluna] = ""

            df["status"] = df["status"].fillna("").astype(str).str.strip()
            df["solicitante"] = df["solicitante"].fillna("").astype(str).str.strip()
            df["descricao"] = df["descricao"].fillna("").astype(str).str.strip()
            df["numero_chamado_externo"] = df["numero_chamado_externo"].fillna("").astype(str).str.strip()

            df.loc[df["status"] == "", "status"] = "Aguardando abertura"

            df["data_abertura_original"] = df["data_abertura"].astype(str)

            if "data_abertura" in df.columns:
                df["data_abertura"] = pd.to_datetime(
                    df["data_abertura"],
                    errors="coerce",
                    dayfirst=True
                )

            st.subheader("Filtros")

            col1, col2, col3 = st.columns(3)

            with col1:
                filtro_solicitante = st.text_input("Pesquisar por solicitante")

            with col2:
                filtro_palavra = st.text_input("Pesquisar por palavra-chave")

            with col3:
                filtro_status = st.selectbox(
                    "Filtrar por status",
                    ["Aguardando abertura", "Aberto", "Finalizado", "Todos"]
                )

            resultado = df.copy()

            if filtro_solicitante:
                resultado = resultado[
                    resultado["solicitante"].str.contains(filtro_solicitante, case=False, na=False)
                ]

            if filtro_palavra:
                resultado = resultado[
                    resultado["descricao"].str.contains(filtro_palavra, case=False, na=False) |
                    resultado["orgao"].astype(str).str.contains(filtro_palavra, case=False, na=False) |
                    resultado["numero_chamado_externo"].astype(str).str.contains(filtro_palavra, case=False, na=False)
                ]

            if filtro_status != "Todos":
                resultado = resultado[resultado["status"] == filtro_status]

            ordem_status = {
                "Aguardando abertura": 0,
                "Aberto": 1,
                "Finalizado": 2
            }

            resultado["ordem_status"] = resultado["status"].map(ordem_status).fillna(99)
            resultado = resultado.sort_values(
                by=["ordem_status", "data_abertura"],
                ascending=[True, False]
            )

            st.success(f"{len(resultado)} chamado(s) encontrado(s)")

            if resultado.empty:
                st.info("Nenhum chamado encontrado com esses filtros.")
            else:
                opcoes = resultado.index.tolist()

                indice = st.selectbox(
                    "Selecione o chamado para editar",
                    opcoes,
                    format_func=lambda x: (
                        f"{resultado.loc[x, 'solicitante']} | "
                        f"{resultado.loc[x, 'status']} | "
                        f"{resultado.loc[x, 'categoria']} | "
                        f"{resultado.loc[x, 'numero_chamado_externo'] if resultado.loc[x, 'numero_chamado_externo'] else 'Sem número'}"
                    )
                )

                st.divider()
                st.subheader("Dados do chamado")

                data_formatada = ""
                data_valor = resultado.loc[indice, "data_abertura"]

                if pd.notna(data_valor):
                    data_formatada = data_valor.strftime("%d/%m/%Y")
                else:
                    data_formatada = resultado.loc[indice, "data_abertura_original"]

                col_a, col_b = st.columns(2)

                with col_a:
                    st.write(f"**Data:** {data_formatada}")
                    st.write(f"**Solicitante:** {resultado.loc[indice, 'solicitante']}")
                    st.write(f"**Categoria:** {resultado.loc[indice, 'categoria']}")
                    st.write(f"**Status atual:** {resultado.loc[indice, 'status']}")

                with col_b:
                    st.write(f"**Órgão:** {resultado.loc[indice, 'orgao']}")
                    st.write(f"**Login:** {resultado.loc[indice, 'login']}")
                    st.write(f"**URL:** {resultado.loc[indice, 'url']}")
                    st.write(f"**Gravação:** {resultado.loc[indice, 'link_gravacao']}")

                st.write("**Descrição:**")
                st.info(resultado.loc[indice, "descricao"] if resultado.loc[indice, "descricao"] else "Sem descrição")

                st.divider()
                st.subheader("Atualização")

                lista_status = ["Aguardando abertura", "Aberto", "Finalizado"]
                status_atual = resultado.loc[indice, "status"]

                novo_status = st.selectbox(
                    "Novo status",
                    lista_status,
                    index=lista_status.index(status_atual) if status_atual in lista_status else 0
                )

                numero_chamado = st.text_input(
                    "Nº do chamado",
                    value=str(resultado.loc[indice, "numero_chamado_externo"])
                )

                observacao_interna = st.text_area(
                    "Observação interna",
                    value=str(resultado.loc[indice, "observacao_interna"])
                )

                salvar = st.button("Salvar alterações")

                if salvar:
                    df.loc[indice, "status"] = novo_status
                    df.loc[indice, "numero_chamado_externo"] = numero_chamado
                    df.loc[indice, "observacao_interna"] = observacao_interna

                    if novo_status == "Finalizado":
                        if not str(df.loc[indice, "data_fechamento"]).strip() or str(df.loc[indice, "data_fechamento"]).lower() == "nan":
                            df.loc[indice, "data_fechamento"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    else:
                        df.loc[indice, "data_fechamento"] = ""

                    df.to_csv(CAMINHO_ARQUIVO, index=False, encoding="utf-8-sig")
                    st.success("Chamado atualizado com sucesso!")