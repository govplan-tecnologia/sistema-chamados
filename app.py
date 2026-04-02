import streamlit as st
from utils.styles import aplicar_estilo, mostrar_logo

st.set_page_config(
    page_title="Central de Chamados",
    page_icon="📞",
    layout="wide"
)

aplicar_estilo()
mostrar_logo()

st.title("Central de Chamados")
st.subheader("Sistema interno para abertura e acompanhamento de chamados")
st.divider()

st.write("Bem-vindo ao sistema de chamados. Escolha uma opção abaixo ou navegue pelo menu lateral.")
st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="
        background-color:#132A63;
        padding:30px 20px;
        border-radius:16px;
        text-align:center;
        color:white;
        min-height:160px;
        display:flex;
        flex-direction:column;
        justify-content:center;
    ">
        <div style="font-size:36px;">📋</div>
        <div style="font-size:20px; font-weight:700; margin-top:10px;">Abrir Chamado</div>
        <div style="font-size:14px; margin-top:8px; opacity:0.85;">Registre um novo chamado de suporte</div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Abrir chamado →", use_container_width=True, key="btn_abertura"):
        st.switch_page("pages/1_Abertura_de_Chamado.py")

with col2:
    st.markdown("""
    <div style="
        background-color:#1B3F8B;
        padding:30px 20px;
        border-radius:16px;
        text-align:center;
        color:white;
        min-height:160px;
        display:flex;
        flex-direction:column;
        justify-content:center;
    ">
        <div style="font-size:36px;">🔍</div>
        <div style="font-size:20px; font-weight:700; margin-top:10px;">Acompanhamento</div>
        <div style="font-size:14px; margin-top:8px; opacity:0.85;">Consulte o status dos seus chamados</div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Ver meus chamados →", use_container_width=True, key="btn_acompanhamento"):
        st.switch_page("pages/3_Acompanhamento.py")

with col3:
    st.markdown("""
    <div style="
        background-color:#7EDC12;
        padding:30px 20px;
        border-radius:16px;
        text-align:center;
        color:#132A63;
        min-height:160px;
        display:flex;
        flex-direction:column;
        justify-content:center;
    ">
        <div style="font-size:36px;">📊</div>
        <div style="font-size:20px; font-weight:700; margin-top:10px;">Dashboard</div>
        <div style="font-size:14px; margin-top:8px; opacity:0.85;">Visualize os indicadores gerais</div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Ver dashboard →", use_container_width=True, key="btn_dashboard"):
        st.switch_page("pages/2_Dashboard.py")

st.write("")
st.info("💡 Certifique-se de digitar corretamente seu nome para conseguir acompanhar seus chamados depois.")