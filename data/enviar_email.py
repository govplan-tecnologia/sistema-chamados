import yagmail


def enviar_email_novo_chamado(dados_chamado: dict):
    yag = yagmail.SMTP(
        user="sistema.chamados.teste@gmail.com",
        password="gfkpclmziuhpbdvp"
    )

    link_gravacao = dados_chamado.get("link_gravacao", "")
    if not link_gravacao:
        link_gravacao = "Não informado"

    criticidade = dados_chamado.get("criticidade", "")
    if not criticidade:
        criticidade = "Não informada"

    corpo = f"""
Uma nova abertura de chamado foi registrada:

🔴 Criticidade: {criticidade}
Solicitante: {dados_chamado.get("solicitante", "")}
Login: {dados_chamado.get("login", "")}
Órgão: {dados_chamado.get("orgao", "")}
URL: {dados_chamado.get("url", "")}
Categoria: {dados_chamado.get("categoria", "")}
Descrição:
{dados_chamado.get("descricao", "")}
Link gravação: {link_gravacao}
"""

    destinatarios = [
        "monithelly.flavia@govplan.com.br",
        "franciele@govplan.com.br",
    ]

    yag.send(
        to=destinatarios,
        subject=f"[{criticidade}] Nova abertura de chamado",
        contents=corpo
    )

    print("E-mail enviado para:", destinatarios)