import yagmail


def enviar_email_novo_chamado(dados_chamado: dict):
    yag = yagmail.SMTP(
        user="sistema.chamados.teste@gmail.com",
        password="gfkpclmziuhpbdvp"
    )

    link_gravacao = dados_chamado.get("link_gravacao", "")
    if not link_gravacao:
        link_gravacao = "Não informado"

    corpo = f"""
Uma nova resposta foi adicionada:

Solicitante: {dados_chamado.get("solicitante", "")}
Login: {dados_chamado.get("login", "")}
Órgão: {dados_chamado.get("orgao", "")}
URL: {dados_chamado.get("url", "")}

Descrição:
{dados_chamado.get("descricao", "")}

Categoria: {dados_chamado.get("categoria", "")}
Link gravação: {link_gravacao}
"""

    yag.send(
        to="monithelly.flavia@govplan.com.br",
        subject="Nova abertura de chamado",
        contents=corpo
    )