import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="História Itacoatiara 2026", layout="wide")

# Link da sua planilha
SHEET_ID = "1HFRKm-NY5jvlx6W_pV8AA1fmNq8wOwng5su4V4U3DLU"

# 1. FUNÇÃO PARA DESCOBRIR AS ABAS AUTOMATICAMENTE
@st.cache_data
def listar_abas_reais():
    # Acessa a planilha mestre para ver os nomes das abas
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit#gid=0"
    try:
        # Lê apenas a estrutura para identificar as abas disponíveis
        html_sheets = pd.read_html(f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/pubhtml", header=0)
        return [str(i) for i in range(len(html_sheets))] # Fallback simples
    except:
        # Lista manual robusta caso a detecção automática falhe no servidor
        return ["8º01", "8º02", "8º03", "9º01", "9º02", "8º04", "8º05", "9º03", "9º04", "9º05"]

def carregar_dados(aba_nome):
    # O segredo: .strip() remove espaços invisíveis antes e depois do nome
    nome_limpo = aba_nome.strip()
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(nome_limpo)}"
    df = pd.read_csv(url)
    df.columns = [str(c).strip().upper() for c in df.columns]
    return df

# 2. LOGIN
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

st.sidebar.title("🛡️ Sistema de Confiança")

if not st.session_state.autenticado:
    u = st.sidebar.text_input("Usuário")
    s = st.sidebar.text_input("Senha", type="password")
    if st.sidebar.button("Entrar"):
        if u == "admin" and s == "2026":
            st.session_state.autenticado = True
            st.rerun()
    st.stop()

# 3. INTERFACE
abas_disponiveis = listar_abas_reais()
turma_sel = st.sidebar.selectbox("Escolha a Turma", abas_disponiveis)

try:
    df = carregar_dados(turma_sel)
    st.title(f"📊 Turma: {turma_sel}")
    
    # Validação de Colunas
    if 'NOME' in df.columns:
        for index, row in df.iterrows():
            with st.container():
                c1, c2, c3, c4 = st.columns([2, 1, 2, 1])
                c1.write(f"👤 **{row['NOME']}**")
                
                # Saldo com cor
                saldo = float(row.get('SALDO', 10.0))
                cor = "green" if saldo >= 9 else "orange" if saldo >= 7 else "red"
                c2.markdown(f"<h3 style='color:{cor}; margin:0;'>{saldo:.1f}</h3>", unsafe_allow_html=True)
                
                c3.write(f"AV1: {row.get('AV1', 0)} | AV2: {row.get('AV2', 0)}")
                
                # Botão Zap
                tel = str(row.get('TELEFONE', '')).split('.')[0]
                msg = f"Olá! Saldo de {row['NOME']}: {saldo:.1f}."
                if tel:
                    c4.link_button("📱 Zap", f"https://wa.me/{tel}?text={urllib.parse.quote(msg)}")
                st.divider()
    else:
        st.error(f"Não encontrei a coluna 'NOME' na aba {turma_sel}.")
        st.write("Colunas lidas:", list(df.columns))

except Exception as e:
    st.error(f"Erro ao ler a aba '{turma_sel}'.")
    st.info("Dica: Verifique se a sua planilha está 'Pública' (Qualquer pessoa com o link pode ler).")
    st.caption(f"Erro: {e}")
