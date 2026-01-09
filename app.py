import streamlit as st
import pandas as pd
import urllib.parse

# 1. CONFIGURAÇÕES ESTÉTICAS E TÍTULO
st.set_page_config(page_title="História MMXXVI - Prof. Luiz", layout="wide", page_icon="🛡️")

# Estilos customizados para um visual acadêmico e moderno
st.markdown("""
    <style>
    .stApp { background-color: #F0F4F8 !important; } 
    [data-testid="stSidebar"] { background-color: #1A237E !important; }
    .stButton>button { width: 100%; border-radius: 20px; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { background-color: #FFD600 !important; color: #1A237E !important; }
    .header-box { background-color: #1A237E; color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 25px; }
    .disclaimer { font-size: 0.85rem; color: #546E7A; font-style: italic; border-top: 1px solid #CFD8DC; margin-top: 20px; padding-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. IDENTIFICAÇÃO E CONEXÃO
SHEET_ID = "1HFRKm-NY5jvlx6W_pV8AA1fmNq8wOwng5su4V4U3DLU"

def carregar_dados(aba_nome):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(aba_nome.strip())}"
    df = pd.read_csv(url)
    df.columns = [str(c).strip().upper() for c in df.columns]
    return df

# 3. BARRA LATERAL (SIDEBAR)
with st.sidebar:
    st.markdown("<h1 style='color: #FFD600; text-align: center;'>🏛️ MMXXVI</h1>", unsafe_allow_html=True)
    st.write("---")
    if 'autenticado' not in st.session_state: st.session_state.autenticado = False
    
    if not st.session_state.autenticado:
        st.subheader("🛡️ Acesso Restrito")
        u = st.text_input("Usuário")
        s = st.text_input("Senha", type="password")
        if st.button("ENTRAR"):
            if u == "admin" and s == "2026":
                st.session_state.autenticado = True
                st.rerun()
            else: st.error("Acesso Negado")
        st.stop()
    
    st.success("Professor Conectado")
    turmas = ["8º01", "8º02", "8º03", "9º01", "9º02", "8º04", "8º05", "9º03", "9º04", "9º05"]
    turma_sel = st.selectbox("📂 Selecione a Turma", turmas)
    st.write("---")
    st.caption("Desenvolvido para apoio pedagógico.")

# 4. CABEÇALHO OFICIAL
st.markdown(f"""
    <div class="header-box">
        <h1 style='margin:0;'>SISTEMA DE CRÉDITO DE CONFIANÇA</h1>
        <h3 style='margin:0; color: #FFD600;'>PROF. LUIZ ALBERTO PEPINO</h3>
        <p style='margin:5px 0 0 0;'>Escola Estadual Maria Ivone de Araújo Leite</p>
        <p style='margin:0;'><b>Disciplina: História | Ano MMXXVI</b></p>
    </div>
    """, unsafe_allow_html=True)

# 5. CONTEÚDO PRINCIPAL
tab_diario, tab_livros, tab_regras = st.tabs(["📊 Desempenho", "📖 Material Didático", "📜 Termos e Regras"])

with tab_diario:
    try:
        df = carregar_dados(turma_sel)
        for index, row in df.iterrows():
            with st.expander(f"👤 {row['NOME']}", expanded=False):
                c1, c2, c3 = st.columns([1, 1, 1])
                
                # Saldo
                val_saldo = float(row['SALDO'])
                cor = "green" if val_saldo >= 9 else "orange" if val_saldo >= 7 else "red"
                c1.metric("Saldo de Confiança", f"{val_saldo:.1f} pts")
                
                # Notas
                c2.write(f"**AV1:** {row['AV1']} | **AV2:** {row['AV2']}")
                
                # Ações
                with c3:
                    motivo = st.selectbox("Ocorrência:", 
                        ["Acompanhamento de rotina", "Material/Sono", "Tarefa não feita", "Indisciplina", "Destaque Positivo"], 
                        key=f"sel_{index}")
                    
                    texto_zap = (f"*História MMXXVI* 🛡️\n\n"
                                 f"Olá! Informo o saldo de *{row['NOME']}*: *{val_saldo:.1f} pts*.\n"
                                 f"Registro: {motivo}.\n"
                                 f"Notas: AV1: {row['AV1']} | AV2: {row['AV2']}\n\n"
                                 f"Prof. Luiz Alberto Pepino")
                    
                    st.link_button("📱 Enviar para Responsável", 
                                   f"https://wa.me/{str(row['TELEFONE']).split('.')[0]}?text={urllib.parse.quote(texto_zap)}")

    except Exception as e:
        st.error(f"Erro ao carregar turma {turma_sel}.")

with tab_livros:
    st.subheader("📚 Livros Didáticos de História")
    st.link_button("📘 1º Bimestre (8º e 9º Anos)", "https://raw.githubusercontent.com/LUIZALBERTOPEPINO/historia-em-foco-2026/main/livro_8_9_bim1.pdf")

with tab_regras:
    st.markdown("""
    ### 📜 Diretrizes do Sistema
    Este app baseia-se no **Crédito de Confiança**, onde o aluno inicia com 10.0 pontos e gere seu comportamento.
    
    **Regras de Crédito/Débito:**
    * 📕 Material/Desatenção: -0.2
    * 📝 Tarefa não realizada: -0.5
    * 🚫 Indisciplina: -0.5
    * ⭐ Destaque Positivo: +0.2
    """)
    
    # AVISO LEGAL (DISCLAIMER) solicitado
    st.markdown(f"""
    <div class="disclaimer">
        ⚠️ <b>Informação Importante:</b> Este aplicativo é uma ferramenta suplementar de gestão pedagógica do Prof. Luiz Alberto Pepino. 
        <b>Não substitui os documentos oficiais</b> (boletins e históricos escolares) emitidos pela secretaria da 
        Escola Estadual Maria Ivone de Araújo Leite. Seu propósito é exclusivamente facilitar o acompanhamento em tempo real 
        do desempenho e comportamento por parte dos pais ou responsáveis.
    </div>
    """, unsafe_allow_html=True)
