import streamlit as st
import pandas as pd
from datetime import datetime
from utils.styles import aplicar_estilo, mostrar_logo
from data.ler_chamados import ler_chamados, atualizar_chamado

aplicar_estilo()
mostrar_logo()

st.title("Área Interna")
st.write("Use os filtros abaixo para localizar e atualizar chamados.")
st.divider()

SENHA_ADMIN = "govplan2026!"
senha = st.text_input("Senha de acesso", type="password")


def limpar_campos_atualizacao(status_atual="", numero_chamado="", observacao=""):
    st.session_state["novo_status"] = status_atual if status_atual else "Aguardando abertura"
    st.session_state["numero_chamado"] = str(numero_chamado) if pd.notna(numero_chamado) else ""
    st.session_state["observacao_interna"] = str(observacao) if pd.notna(observacao) else ""


if senha != SENHA_ADMIN:
    st.warning("Digite a senha para liberar a edição.")
else:
    st.success("Acesso liberado.")

    df = ler_chamados()

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
            "data_fechamento"
        ]

        for coluna in colunas_necessarias:
            if coluna not in df.columns:
                df[coluna] = ""

        df["status"] = df["status"].fillna("").astype(str).str.strip()
        df["solicitante"] = df["solicitante"].fillna("").astype(str).str.strip()
        df["descricao"] = df["descricao"].fillna("").astype(str).str.strip()
        df["numero_chamado_externo"] = df["numero_chamado_externo"].fillna("").astype(str).str.strip()
        df["observacao_interna"] = df["observacao_interna"].fillna("").astype(str).str.strip()

        df.loc[df["status"] == "", "status"] = "Aguardando abertura"

        df["data_abertura_original"] = df["data_abertura"].astype(str)
        df["data_abertura"] = pd.to_datetime(df["data_abertura"], errors="coerce", dayfirst=True)

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
        resultado = resultado.sort_values(by=["ordem_status", "data_abertura"], ascending=[True, False])

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

            # Controle do chamado atualmente selecionado
            if "indice_chamado_atual" not in st.session_state:
                st.session_state["indice_chamado_atual"] = None

            # Sempre que trocar o chamado, reseta os campos da área de atualização
            if st.session_state["indice_chamado_atual"] != indice:
                st.session_state["indice_chamado_atual"] = indice
                limpar_campos_atualizacao(
                    status_atual=resultado.loc[indice, "status"],
                    numero_chamado=resultado.loc[indice, "numero_chamado_externo"],
                    observacao=resultado.loc[indice, "observacao_interna"]
                )

            st.divider()
            st.subheader("Dados do chamado")

            data_valor = resultado.loc[indice, "data_abertura"]
            data_formatada = (
                data_valor.strftime("%d/%m/%Y")
                if pd.notna(data_valor)
                else resultado.loc[indice, "data_abertura_original"]
            )

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
            st.info(
                resultado.loc[indice, "descricao"]
                if resultado.loc[indice, "descricao"]
                else "Sem descrição"
            )

            st.divider()
            st.subheader("Atualização")

            lista_status = ["Aguardando abertura", "Aberto", "Finalizado"]

            st.selectbox(
                "Novo status",
                lista_status,
                key="novo_status"
            )

            st.text_input(
                "Nº do chamado",
                key="numero_chamado"
            )

            st.text_area(
                "Observação interna",
                key="observacao_interna"
            )

            if st.button("Salvar alterações"):
                data_fechamento = ""

                if st.session_state["novo_status"] == "Finalizado":
                    data_fechamento = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                atualizar_chamado(
                    indice,
                    st.session_state["novo_status"],
                    st.session_state["numero_chamado"],
                    st.session_state["observacao_interna"],
                    data_fechamento
                )

                st.success("Chamado atualizado com sucesso!")

                # Depois de salvar, recarrega os campos com o que acabou de ser salvo
                limpar_campos_atualizacao(
                    status_atual=st.session_state["novo_status"],
                    numero_chamado=st.session_state["numero_chamado"],
                    observacao=st.session_state["observacao_interna"]
                )

                st.rerun()