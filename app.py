import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import urllib.parse

st.set_page_config(page_title="História em Foco 2026", layout="wide")

# Conexão com o Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Erro na conexão com os Secrets. Verifique o link da planilha.")
    st.stop()

# Login
if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if not st.session_state.autenticado:
    st.sidebar.title("🔐 Acesso 2026")
    u = st.sidebar.text_input("Usuário")
    s = st.sidebar.text_input("Senha", type="password")
    if st.sidebar.button("Entrar"):
        if u == "admin" and s == "2026":
            st.session_state.autenticado = True
            st.rerun()
    st.stop()

st.title("🛡️ Sistema de Crédito de Confiança")

# Lista de turmas conforme as abas da sua planilha
lista_turmas = ["8º01", "8º02", "8º03", "9º01", "9º02", "8º04", "8º05", "9º03", "9º04", "9º05"]
turma_sel = st.sidebar.selectbox("Selecionar Turma", lista_turmas)

# Tenta ler os dados
try:
    df = conn.read(worksheet=turma_sel)
    
    if df.empty:
        st.warning(f"A aba '{turma_sel}' parece estar vazia.")
    else:
        for index, row in df.iterrows():
            with st.container():
                c1, c2, c3, c4, c5 = st.columns([1.5, 1.2, 0.8, 3.5, 1.5])
                c1.write(f"**{row['NOME']}**")
                
                # Exibe as notas atuais
                c2.write(f"AV1: {row['AV1']} | AV2: {row['AV2']}")
                
                # Saldo
                cor = "green" if row['SALDO'] >= 9 else "orange" if row['SALDO'] >= 7 else "red"
                c3.markdown(f"<h2 style='color:{cor};'>{row['SALDO']:.1f}</h2>", unsafe_allow_html=True)

                with c4:
                    b1, b2, b3 = st.columns(3)
                    if b1.button("📕 -0.2", key=f"b1_{index}"):
                        st.info("Função de salvar habilitada para o dia 20/01")
                    if b2.button("📝 -0.5", key=f"b2_{index}"):
                        st.info("Registrando...")
                
                with c5:
                    st.link_button("📱 Zap", f"https://wa.me/{row['TELEFONE']}")
                st.divider()

except Exception as e:
    st.error(f"Não consegui ler a aba '{turma_sel}'. Verifique se o nome da aba na Planilha Google é exatamente este.")
    st.info(f"Erro técnico: {e}")
