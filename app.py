import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="História Itacoatiara 2026", layout="wide")

# Link direto para exportação (Transforma a planilha em um CSV legível)
SHEET_ID = "1HFRKm-NY5jvlx6W_pV8AA1fmNq8wOwng5su4V4U3DLU"

def carregar_dados(aba):
    # Esta URL força o Google a entregar os dados puramente como texto, evitando o erro de InvalidURL
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={aba}"
    return pd.read_csv(url)

# Cabeçalho
st.sidebar.title("🛡️ Sistema de Confiança")

# Login
if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if not st.session_state.autenticado:
    u = st.sidebar.text_input("Usuário")
    s = st.sidebar.text_input("Senha", type="password")
    if st.sidebar.button("Entrar"):
        if u == "admin" and s == "2026":
            st.session_state.autenticado = True
            st.rerun()
    st.stop()

# Menu de Turmas
turmas = ["8º01", "8º02", "8º03", "9º01", "9º02", "8º04", "8º05", "9º03", "9º04", "9º05"]
turma_sel = st.sidebar.selectbox("Escolha a Turma", turmas)

try:
    df = carregar_dados(turma_sel)
    st.title(f"📊 Turma: {turma_sel}")
    
    for index, row in df.iterrows():
        with st.container():
            c1, c2, c3, c4 = st.columns([2, 1, 2, 1])
            c1.write(f"👤 **{row['NOME']}**")
            
            saldo = float(row['SALDO'])
            cor = "green" if saldo >= 9 else "orange" if saldo >= 7 else "red"
            c2.markdown(f"<h3 style='color:{cor};'>{saldo:.1f}</h3>", unsafe_allow_html=True)
            
            c3.write(f"AV1: {row['AV1']} | AV2: {row['AV2']}")
            
            # Zap
            tel = str(row['TELEFONE']).replace(".0", "")
            msg = f"Olá! Saldo de {row['NOME']}: {saldo:.1f}."
            c4.link_button("📱 Zap", f"https://wa.me/{tel}?text={urllib.parse.quote(msg)}")
            st.divider()
            
except Exception as e:
    st.error("Erro ao carregar os dados da aba. Verifique se o nome da aba na planilha está igual ao selecionado.")
    st.info(f"Dica: O nome da aba deve ser exatamente '{turma_sel}' no Google Sheets.")
