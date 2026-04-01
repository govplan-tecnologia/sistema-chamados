import os
import pandas as pd
from datetime import datetime

CAMINHO_ARQUIVO = "data/chamados.csv"


def salvar_chamado(dados):
    os.makedirs("data", exist_ok=True)

    novo_registro = {
        "data_abertura": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "solicitante": str(dados.get("solicitante", "")).strip(),
        "categoria": str(dados.get("categoria", "")).strip(),
        "orgao": str(dados.get("orgao", "")).strip(),
        "login": str(dados.get("login", "")).strip(),
        "url": str(dados.get("url", "")).strip(),
        "link_gravacao": str(dados.get("link_gravacao", "")).strip(),
        "descricao": str(dados.get("descricao", "")).strip(),
        "anexo": str(dados.get("anexo", "")).strip(),
        "status": "Aguardando abertura",
        "numero_chamado_externo": "",
        "observacao_interna": "",
        "data_fechamento": ""
    }

    colunas_padrao = [
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

    if os.path.exists(CAMINHO_ARQUIVO):
        df_existente = pd.read_csv(CAMINHO_ARQUIVO, encoding="utf-8-sig")

        for coluna in colunas_padrao:
            if coluna not in df_existente.columns:
                df_existente[coluna] = ""

        df_existente = df_existente[colunas_padrao]
        df_novo = pd.concat([df_existente, pd.DataFrame([novo_registro])], ignore_index=True)
    else:
        df_novo = pd.DataFrame([novo_registro], columns=colunas_padrao)

    df_novo.to_csv(CAMINHO_ARQUIVO, index=False, encoding="utf-8-sig")