import streamlit as st
import gspread
from datetime import datetime
from zoneinfo import ZoneInfo
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

def salvar_chamado(dados):
    agora_brasil = datetime.now(ZoneInfo("America/Sao_Paulo"))
    nova_linha = [
        agora_brasil.strftime("%d/%m/%Y %H:%M:%S"),
        dados.get("solicitante", ""),
        dados.get("categoria", ""),
        dados.get("orgao", ""),
        dados.get("login", ""),
        dados.get("url", ""),
        dados.get("link_gravacao", ""),
        dados.get("descricao", ""),
        dados.get("anexo", ""),
        "Aguardando abertura",
        "",
        "",
        ""
    ]
    sheet = get_sheet()
    sheet.append_row(nova_linha)
    return True