if enviar:
    if not solicitante or not orgao or not descricao:
        st.error("Preencha pelo menos: Solicitante, Órgão e Descrição.")
    else:
        dados = {
            "solicitante": solicitante,
            "categoria": categoria,
            "orgao": orgao,
            "login": login,
            "url": url,
            "link_gravacao": link_gravacao,
            "descricao": descricao,
        }
        try:
            resultado = salvar_chamado(dados, arquivo=anexo)
            try:
                enviar_email_novo_chamado(dados)
            except Exception:
                pass
            if resultado:
                st.session_state.sucesso = True
                st.rerun()
        except Exception as e:
            st.error(f"Erro ao salvar o chamado: {e}")