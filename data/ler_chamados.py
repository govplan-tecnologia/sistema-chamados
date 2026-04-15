import json
import streamlit as st
import pandas as pd
import gspread

SPREADSHEET_ID = "1huNRk11OX11ae-lv4NQX-OED3qgTzVHSTxTVV_dPI9o"


def get_sheet():
    creds_info = dict(st.secrets["gcp_service_account"])
    client = gspread.service_account_from_dict(creds_info)
    return client.open_by_key(SPREADSHEET_ID).sheet1


def normalizar_anexos(valor):
    if pd.isna(valor) or valor is None or str(valor).strip() == "":
        return []

    valor = str(valor).strip()

    if valor.startswith("[") or valor.startswith("{"):
        try:
            dados = json.loads(valor)

            if isinstance(dados, dict):
                dados = [dados]

            if isinstance(dados, list):
                anexos = []
                for item in dados:
                    if isinstance(item, dict):
                        anexos.append({
                            "nome_original": item.get("nome_original", ""),
                            "nome_salvo": item.get("nome_salvo", ""),
                            "caminho": item.get("caminho", ""),
                            "tipo": item.get("tipo", ""),
                            "tamanho_bytes": item.get("tamanho_bytes", None)
                        })
                return anexos
        except Exception:
            pass

    return [{
        "nome_original": valor.split("/")[-1],
        "nome_salvo": valor.split("/")[-1],
        "caminho": valor,
        "tipo": "",
        "tamanho_bytes": None
    }]


def ler_chamados():
    sheet = get_sheet()
    dados = sheet.get_all_records()
    df = pd.DataFrame(dados)

    if df.empty:
        return df

    # Padroniza data de abertura
    if "data_abertura" in df.columns:
        df["data_abertura"] = pd.to_datetime(
            df["data_abertura"],
            format="%d/%m/%Y %H:%M:%S",
            errors="coerce"
        )

    # Padroniza data de fechamento
    if "data_fechamento" in df.columns:
        df["data_fechamento"] = pd.to_datetime(
            df["data_fechamento"],
            format="%d/%m/%Y %H:%M:%S",
            errors="coerce"
        )

    # Compatibilidade entre coluna antiga "anexo" e nova "anexos"
    if "anexos" in df.columns:
        df["anexos"] = df["anexos"].apply(normalizar_anexos)
    elif "anexo" in df.columns:
        df["anexos"] = df["anexo"].apply(normalizar_anexos)
    else:
        df["anexos"] = [[] for _ in range(len(df))]

    return df


def atualizar_chamado(indice_linha, status, numero, observacao, data_fechamento):
    sheet = get_sheet()
    linha = indice_linha + 2

    colunas = {
        "status": 11,
        "numero_chamado_externo": 12,
        "observacao_interna": 13,
        "data_fechamento": 14
    }

    sheet.update_cell(linha, colunas["status"], status)
    sheet.update_cell(linha, colunas["numero_chamado_externo"], numero)
    sheet.update_cell(linha, colunas["observacao_interna"], observacao)
    sheet.update_cell(linha, colunas["data_fechamento"], data_fechamento)