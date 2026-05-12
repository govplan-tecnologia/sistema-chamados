import os
import json
import mimetypes
import streamlit as st
import gspread
import unicodedata
import re
from datetime import datetime
from zoneinfo import ZoneInfo

SPREADSHEET_ID = "1huNRk11OX11ae-lv4NQX-OED3qgTzVHSTxTVV_dPI9o"

def get_sheet():
    if "gcp_service_account" not in st.secrets:
        raise KeyError("A chave 'gcp_service_account' não foi encontrada no secrets.toml")

    creds_info = dict(st.secrets["gcp_service_account"])
    client = gspread.service_account_from_dict(creds_info)
    return client.open_by_key(SPREADSHEET_ID).sheet1

def garantir_pasta_uploads():
    pasta_uploads = "uploads"
    os.makedirs(pasta_uploads, exist_ok=True)
    return pasta_uploads

def limpar_nome_arquivo(nome_arquivo):
    """
    Remove acentos e caracteres problemáticos do nome do arquivo.
    Exemplo: "PLANILHA GESTÃO UFJ.xlsx" -> "PLANILHA_GESTAO_UFJ.xlsx"
    """
    # Normaliza para decompor caracteres acentuados (ex: 'ã' vira 'a' + '~')
    nome = unicodedata.normalize('NFD', nome_arquivo)
    # Filtra apenas caracteres ASCII (remove os acentos)
    nome = nome.encode('ascii', 'ignore').decode('ascii')
    # Substitui espaços por underscores
    nome = nome.replace(" ", "_")
    # Remove qualquer caractere que não seja letra, número, ponto, traço ou underscore
    nome = re.sub(r'[^a-zA-Z0-9._-]', '', nome)
    return nome

def salvar_arquivo(uploaded_file):
    """
    Salva um arquivo enviado pelo st.file_uploader e retorna
    um dicionário com os metadados do anexo.
    """
    if uploaded_file is None:
        return None

    pasta_uploads = garantir_pasta_uploads()

    agora_brasil = datetime.now(ZoneInfo("America/Sao_Paulo"))
    timestamp = agora_brasil.strftime("%Y%m%d_%H%M%S_%f")

    nome_original = uploaded_file.name
    nome_limpo = limpar_nome_arquivo(nome_original)
    nome_salvo = f"{timestamp}_{nome_limpo}"

    caminho_arquivo = os.path.join(pasta_uploads, nome_salvo)

    with open(caminho_arquivo, "wb") as f:
        f.write(uploaded_file.getbuffer())

    mime_type = uploaded_file.type
    if not mime_type:
        mime_type, _ = mimetypes.guess_type(nome_original)
        mime_type = mime_type or "application/octet-stream"

    return {
        "nome_original": nome_original,
        "nome_salvo": nome_salvo,
        "caminho": caminho_arquivo,
        "tipo": mime_type,
        "tamanho_bytes": uploaded_file.size if hasattr(uploaded_file, "size") else None
    }

def salvar_anexos(arquivos):
    if arquivos is None:
        return []

    if not isinstance(arquivos, list):
        arquivos = [arquivos]

    anexos_salvos = []
    for arquivo in arquivos:
        if arquivo is None:
            continue
        anexo = salvar_arquivo(arquivo)
        if anexo:
            anexos_salvos.append(anexo)
    return anexos_salvos

def salvar_chamado(dados):
    agora_brasil = datetime.now(ZoneInfo("America/Sao_Paulo"))

    arquivos_recebidos = dados.get("anexos")
    if arquivos_recebidos is None:
        arquivos_recebidos = dados.get("anexo")

    anexos_salvos = salvar_anexos(arquivos_recebidos)
    anexos_json = json.dumps(anexos_salvos, ensure_ascii=False)

    nova_linha = [
        agora_brasil.strftime("%d/%m/%Y %H:%M:%S"),
        dados.get("solicitante", ""),
        dados.get("categoria", ""),
        dados.get("orgao", ""),
        dados.get("login", ""),
        dados.get("url", ""),
        dados.get("link_gravacao", ""),
        dados.get("descricao", ""),
        anexos_json,
        dados.get("criticidade", ""),
        "Aguardando abertura",
        "",
        "",
        ""
    ]

    sheet = get_sheet()
    sheet.append_row(nova_linha)
    return True
