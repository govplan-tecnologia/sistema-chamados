import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SPREADSHEET_ID = "1huNRk11OX11ae-lv4NQX-OED3qgTzVHSTxTVV_dPI9o"

def get_sheet():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )
    client = gspread.authorize(creds)
    return client.open_by_key(SPREADSHEET_ID).sheet1

def ler_chamados():
    sheet = get_sheet()
    dados = sheet.get_all_records()
    df = pd.DataFrame(dados)
    return df

def atualizar_chamado(indice_linha, status, numero, observacao, data_fechamento):
    sheet = get_sheet()
    # +2 porque sheets começa em 1 e tem cabeçalho
    linha = indice_linha + 2
    colunas = {
        "status": 10,
        "numero_chamado_externo": 11,
        "observacao_interna": 12,
        "data_fechamento": 13
    }
    sheet.update_cell(linha, colunas["status"], status)
    sheet.update_cell(linha, colunas["numero_chamado_externo"], numero)
    sheet.update_cell(linha, colunas["observacao_interna"], observacao)
    sheet.update_cell(linha, colunas["data_fechamento"], data_fechamento)