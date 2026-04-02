import streamlit as st
import gspread
from datetime import datetime
from zoneinfo import ZoneInfo
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SPREADSHEET_ID = "1huNRk11OX11ae-lv4NQX-OED3qgTzVHSTxTVV_dPI9o"
PASTA_DRIVE_ID = "1fB3C-D4R3upsDopdJ84L8floWAjbwQgd"

def get_creds():
    return Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )

def get_sheet():
    client = gspread.authorize(get_creds())
    return client.open_by_key(SPREADSHEET_ID).sheet1

def upload_anexo(arquivo):
    if arquivo is None:
        return ""
    creds = get_creds()
    service = build("drive", "v3", credentials=creds)
    file_metadata = {
        "name": arquivo.name,
        "parents": [PASTA_DRIVE_ID]
    }
    media = MediaIoBaseUpload(io.BytesIO(arquivo.read()), mimetype=arquivo.type)
    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    file_id = file.get("id")
    service.permissions().create(fileId=file_id, body={"type": "anyone", "role": "reader"}).execute()
    return f"https://drive.google.com/file/d/{file_id}/view"

def salvar_chamado(dados, arquivo=None):
    agora_brasil = datetime.now(ZoneInfo("America/Sao_Paulo"))
    link_anexo = upload_anexo(arquivo)
    nova_linha = [
        agora_brasil.strftime("%d/%m/%Y %H:%M:%S"),
        dados.get("solicitante", ""),
        dados.get("categoria", ""),
        dados.get("orgao", ""),
        dados.get("login", ""),
        dados.get("url", ""),
        dados.get("link_gravacao", ""),
        dados.get("descricao", ""),
        link_anexo,
        "Aguardando abertura",
        "",
        "",
        ""
    ]
    sheet = get_sheet()
    sheet.append_row(nova_linha)
    return True