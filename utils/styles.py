import streamlit as st


def aplicar_estilo():
    st.markdown("""
    <style>
    /* Fundo geral */
    .stApp {
        background-color: #F4F7FB;
    }

    /* Container principal */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #132A63 !important;
    }

    /* Textos da sidebar */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Item ativo do menu */
    section[data-testid="stSidebarNav"] a[aria-current="page"] {
        background-color: #7EDC12 !important;
        color: #132A63 !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
    }

    section[data-testid="stSidebarNav"] a[aria-current="page"] * {
        color: #132A63 !important;
    }

    /* Links do menu */
    section[data-testid="stSidebarNav"] a {
        border-radius: 10px;
    }

    /* Títulos */
    h1, h2, h3 {
        color: #132A63 !important;
    }

    /* Texto geral */
    p, label, span, div {
        color: #132A63;
    }

    /* Botões normais e de formulário */
    .stButton > button,
    .stForm button[kind="primary"] {
        background-color: #7EDC12 !important;
        color: #132A63 !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
    }

    .stButton > button:hover,
    .stForm button[kind="primary"]:hover {
        background-color: #6BC50F !important;
        color: #132A63 !important;
    }

    /* Inputs */
    .stTextInput input,
    .stTextArea textarea {
        border-radius: 10px !important;
        border: 1px solid #D9E2F1 !important;
        background-color: white !important;
        color: #132A63 !important;
    }

    /* Selectbox */
    div[data-baseweb="select"] > div {
        border-radius: 10px !important;
        border: 1px solid #D9E2F1 !important;
        background-color: white !important;
        color: #132A63 !important;
    }

    /* File uploader */
    [data-testid="stFileUploader"] section {
        border-radius: 12px !important;
    }

    /* Divider */
    hr {
        border-color: #D9E2F1 !important;
    }
    </style>
    """, unsafe_allow_html=True)


def mostrar_logo():
    st.image("assets/logo/logo_govplan.jpg", width=220)