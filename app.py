import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import urllib.parse

# Configuração Visual
st.set_page_config(page_title="História em Foco 2026", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD !important; } 
    [data-testid="stSidebar"] { background-color: #1565C0 !important; }
    input { color: #000000 !important; background-color: #FFFFFF !important; }
    .stButton>button { background-color: #0D47A1 !important; color: white !important; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

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

# Título
st.title("🛡️ Sistema de Crédito de Confiança")
st.caption("Maria Ivone de Araújo Leite | Prof. Luiz Alberto Pepino")

# Seleção de Turma (Mapeando as abas da sua planilha)
turma_sel = st.sidebar.selectbox("Selecionar Turma", 
    ["8º01", "8º02", "8º03", "9º01", "9º02", "8º04", "8º05", "9º03", "9º04", "9º05"])

# Lendo os dados da aba selecionada
df = conn.read(worksheet=turma_sel)

for index, row in df.iterrows():
    with st.container():
        c1, c2, c3, c4, c5 = st.columns([1.5, 1.2, 0.8, 3.5, 1.5])
        
        # Foto e Nome
        with c1:
            if pd.notna(row['FOTO']):
                st.image(row['FOTO'], width=80)
            st.write(f"**{row['NOME']}**")
        
        # Notas
        with c2:
            n1, n2 = st.columns(2)
            av1 = n1.number_input("AV1", 0.0, 10.0, float(row['AV1']), key=f"av1_{index}")
            av2 = n2.number_input("AV2", 0.0, 10.0, float(row['AV2']), key=f"av2_{index}")
            # Se mudar nota, poderíamos atualizar aqui (implementaremos o save geral abaixo)

        # Saldo
        cor = "green" if row['SALDO'] >= 9 else "orange" if row['SALDO'] >= 7 else "red"
        c3.markdown(f"<h2 style='color:{cor};'>{row['SALDO']:.1f}</h2>", unsafe_allow_html=True)

        # Ações
        with c4:
            b1, b2, b3, b4 = st.columns(4)
            if b1.button("📕 -0.2", key=f"b1_{index}"):
                df.at[index, 'SALDO'] -= 0.2
                df.at[index, 'OCORRENCIA'] = "Material/Desatenção"
                conn.update(worksheet=turma_sel, data=df)
                st.rerun()
            if b2.button("📝 -0.5", key=f"b2_{index}"):
                df.at[index, 'SALDO'] -= 0.5
                df.at[index, 'OCORRENCIA'] = "Tarefa não feita"
                conn.update(worksheet=turma_sel, data=df)
                st.rerun()
            if b3.button("🚫 -0.5", key=f"b3_{index}"):
                df.at[index, 'SALDO'] -= 0.5
                df.at[index, 'OCORRENCIA'] = "Atitude Inconveniente"
                conn.update(worksheet=turma_sel, data=df)
                st.rerun()
            if b4.button("⭐ +0.2", key=f"b4_{index}"):
                df.at[index, 'SALDO'] += 0.2
                df.at[index, 'OCORRENCIA'] = "Destaque Positivo"
                conn.update(worksheet=turma_sel, data=df)
                st.rerun()

        # WhatsApp
        with c5:
            msg = f"*História 🛡️*\nSaldo de *{row['NOME']}*: *{row['SALDO']:.1f}*.\nMotivo: {df.at[index, 'OCORRENCIA']}."
            st.link_button("📱 Notificar", f"https://wa.me/{row['TELEFONE']}?text={urllib.parse.quote(msg)}")
        st.divider()
