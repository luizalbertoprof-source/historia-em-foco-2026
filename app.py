import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="História Itacoatiara 2026", layout="wide")

# 1. IDENTIFICAÇÃO DA PLANILHA
SHEET_ID = "1HFRKm-NY5jvlx6W_pV8AA1fmNq8wOwng5su4V4U3DLU"

def carregar_dados(aba):
    # Força a leitura da aba correta e limpa espaços extras
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={aba.replace(' ', '%20')}"
    df = pd.read_csv(url)
    # Padroniza os nomes das colunas para MAIÚSCULO e sem espaços
    df.columns = [str(c).strip().upper() for c in df.columns]
    return df

# 2. SISTEMA DE LOGIN
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

st.sidebar.title("🛡️ Sistema de Confiança")

if not st.session_state.autenticado:
    u = st.sidebar.text_input("Usuário", key="user")
    s = st.sidebar.text_input("Senha", type="password", key="pass")
    if st.sidebar.button("Entrar"):
        if u == "admin" and s == "2026":
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.sidebar.error("Usuário ou senha incorretos")
    st.info("Aguardando login para carregar turmas...")
    st.stop()

# 3. INTERFACE PÓS-LOGIN
turmas = ["8º01", "8º02", "8º03", "9º01", "9º02", "8º04", "8º05", "9º03", "9º04", "9º05"]
turma_sel = st.sidebar.selectbox("Escolha a Turma", turmas)

try:
    df = carregar_dados(turma_sel)
    st.title(f"📊 Diário de Classe: {turma_sel}")
    
    # Verifica se as colunas essenciais existem
    colunas_necessarias = ['NOME', 'SALDO', 'AV1', 'AV2', 'TELEFONE']
    if all(c in df.columns for c in colunas_necessarias):
        
        for index, row in df.iterrows():
            with st.container():
                c1, c2, c3, c4 = st.columns([2, 1, 2, 1])
                
                c1.write(f"👤 **{row['NOME']}**")
                
                # Saldo com cor
                val_saldo = float(row['SALDO'])
                cor = "green" if val_saldo >= 9 else "orange" if val_saldo >= 7 else "red"
                c2.markdown(f"<h3 style='color:{cor}; margin:0;'>{val_saldo:.1f}</h3>", unsafe_allow_html=True)
                
                c3.write(f"AV1: {row['AV1']} | AV2: {row['AV2']}")
                
                # Botão Zap
                tel = str(row['TELEFONE']).split('.')[0] # Limpa números decimais
                msg = f"Olá! Informo o saldo de {row['NOME']}: {val_saldo:.1f}."
                c4.link_button("📱 Zap", f"https://wa.me/{tel}?text={urllib.parse.quote(msg)}")
                st.divider()
    else:
        st.error(f"As colunas da aba {turma_sel} não estão no formato correto.")
        st.info(f"Colunas encontradas: {list(df.columns)}")

except Exception as e:
    st.error(f"Erro ao acessar a aba '{turma_sel}'.")
    st.info("Verifique se o nome da aba no Google Sheets é EXATAMENTE igual ao selecionado.")
