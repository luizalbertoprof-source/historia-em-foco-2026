import streamlit as st
import pandas as pd
import urllib.parse

# 1. IDENTIDADE VISUAL MMXXVI
st.set_page_config(page_title="História Itacoatiara 2026", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD !important; } 
    [data-testid="stSidebar"] { background-color: #1A237E !important; }
    [data-testid="stSidebar"] .stMarkdown p { color: white !important; }
    .header-box { background-color: #1A237E; color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXÃO DIRETA
SHEET_ID = "1HFRKm-NY5jvlx6W_pV8AA1fmNq8wOwng5su4V4U3DLU"

def carregar_dados(aba_nome):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(aba_nome.strip())}"
    return pd.read_csv(url)

# 3. CABEÇALHO PERSONALIZADO
st.markdown(f"""
    <div class="header-box">
        <h2 style='margin:0;'>SISTEMA DE CRÉDITO DE CONFIANÇA</h2>
        <p style='margin:0;'>PROF. LUIZ ALBERTO PEPINO - MMXXVI</p>
        <p style='font-size: 0.8rem; margin:0;'>Escola Estadual Maria Ivone de Araújo Leite</p>
    </div>
    """, unsafe_allow_html=True)

# 4. BARRA LATERAL
turmas = ["8º01", "8º02", "8º03", "9º01", "9º02", "8º04", "8º05", "9º03", "9º04", "9º05"]
turma_sel = st.sidebar.selectbox("📅 Selecione a Turma", turmas)
st.sidebar.write("---")
st.sidebar.caption("Disciplina: História")

# 5. LISTAGEM DE ALUNOS
try:
    df = carregar_dados(turma_sel)
    # Padroniza colunas para evitar erros
    df.columns = [str(c).strip().upper() for c in df.columns]

    for index, row in df.iterrows():
        with st.container():
            col_nome, col_notas, col_saldo, col_zap = st.columns([2, 1.5, 1, 1])
            
            with col_nome:
                st.write(f"👤 **{row['NOME']}**")
            
            with col_notas:
                st.write(f"AV1: {row['AV1']} | AV2: {row['AV2']}")
            
            with col_saldo:
                saldo = float(row['SALDO'])
                cor = "green" if saldo >= 9 else "orange" if saldo >= 7 else "red"
                st.markdown(f"<b style='color:{cor}; font-size:1.2rem;'>{saldo:.1f}</b>", unsafe_allow_html=True)
            
            with col_zap:
                tel = str(row['TELEFONE']).split('.')[0]
                msg = f"*História MMXXVI* 🛡️\nOlá! Saldo de {row['NOME']}: {saldo:.1f}. Notas AV1: {row['AV1']} | AV2: {row['AV2']}."
                st.link_button("📱 Zap", f"https://wa.me/{tel}?text={urllib.parse.quote(msg)}")
            
            st.divider()

except Exception as e:
    st.error("Aguardando carregamento da planilha...")

# 6. AVISO LEGAL
st.caption("⚠️ Este app serve para acompanhamento pedagógico e não substitui documentos oficiais.")
