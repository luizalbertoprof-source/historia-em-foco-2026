import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import urllib.parse

st.set_page_config(page_title="História em Foco 2026", layout="wide")

# Função para limpar o link dos Secrets e evitar o erro InvalidURL
def get_clean_url():
    try:
        url = st.secrets["connections"]["gsheets"]["spreadsheet"]
        # Remove espaços, quebras de linha e aspas extras que causam o erro
        return url.strip().replace('"', '').replace("'", "")
    except:
        return None

url_limpa = get_clean_url()

if not url_limpa:
    st.error("Link da planilha não encontrado nos Secrets.")
    st.stop()

# Conexão usando a URL limpa
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Forçamos a leitura usando a URL tratada para evitar o erro de caracteres de controle
    lista_turmas = ["8º01", "8º02", "8º03", "9º01", "9º02", "8º04", "8º05", "9º03", "9º04", "9º05"]
    
    st.sidebar.title("🔐 Painel Prof. Luiz")
    
    # Login Simples
    if 'autenticado' not in st.session_state: st.session_state.autenticado = False
    if not st.session_state.autenticado:
        u = st.sidebar.text_input("Usuário")
        s = st.sidebar.text_input("Senha", type="password")
        if st.sidebar.button("Entrar"):
            if u == "admin" and s == "2026":
                st.session_state.autenticado = True
                st.rerun()
        st.stop()

    turma_sel = st.sidebar.selectbox("Selecionar Turma", lista_turmas)

    # Lendo os dados
    df = conn.read(spreadsheet=url_limpa, worksheet=turma_sel)

    st.title(f"🛡️ Turma {turma_sel}")
    
    for index, row in df.iterrows():
        with st.container():
            c1, c2, c3, c4 = st.columns([2, 1, 3, 1])
            c1.write(f"👤 **{row['NOME']}**")
            
            saldo = float(row['SALDO'])
            cor = "green" if saldo >= 9 else "orange" if saldo >= 7 else "red"
            c2.markdown(f"<h3 style='color:{cor};'>{saldo:.1f}</h3>", unsafe_allow_html=True)
            
            with c3:
                st.write(f"AV1: {row['AV1']} | AV2: {row['AV2']}")
                st.caption(f"Última: {row['OCORRENCIA']}")
            
            with c4:
                st.link_button("📱 Zap", f"https://wa.me/{row['TELEFONE']}")
            st.divider()

except Exception as e:
    st.error("Erro ao carregar os dados.")
    st.info(f"Detalhe técnico: {e}")
