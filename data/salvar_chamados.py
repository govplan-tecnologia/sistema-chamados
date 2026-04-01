import os
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

CAMINHO_ARQUIVO = "data/chamados.csv"


def salvar_chamado(dados):
    agora_brasil = datetime.now(ZoneInfo("America/Sao_Paulo"))

    novo_registro = {
        "data_abertura": agora_brasil.strftime("%d/%m/%Y %H:%M:%S"),
        "solicitante": dados.get("solicitante", ""),
        "categoria": dados.get("categoria", ""),
        "orgao": dados.get("orgao", ""),
        "login": dados.get("login", ""),
        "url": dados.get("url", ""),
        "link_gravacao": dados.get("link_gravacao", ""),
        "descricao": dados.get("descricao", ""),
        "anexo": dados.get("anexo", ""),
        "status": "Aguardando abertura",
        "numero_chamado_externo": "",
        "observacao_interna": "",
        "data_fechamento": ""
    }

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

    if os.path.exists(CAMINHO_ARQUIVO):
        df = pd.read_csv(CAMINHO_ARQUIVO, encoding="utf-8-sig")

        for coluna in colunas_necessarias:
            if coluna not in df.columns:
                df[coluna] = ""

        df = df[colunas_necessarias]
    else:
        df = pd.DataFrame(columns=colunas_necessarias)

    df_novo = pd.DataFrame([novo_registro], columns=colunas_necessarias)
    df_final = pd.concat([df, df_novo], ignore_index=True)

    df_final.to_csv(CAMINHO_ARQUIVO, index=False, encoding="utf-8-sig")