import streamlit as st
import pandas as pd
import urllib.parse

# 1. CONFIGURAÇÕES ESTÉTICAS E TÍTULO DA ABA
st.set_page_config(page_title="Sistema de Crédito de Confiança MMXXVI", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD !important; } 
    [data-testid="stSidebar"] { background-color: #1A237E !important; }
    [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] label { color: #FFFFFF !important; font-weight: 500; }
    .stButton>button { width: 100%; border-radius: 20px; font-weight: bold; background-color: #1A237E; color: white; }
    .header-box { background-color: #1A237E; color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 25px; }
    .metric-card { background-color: #BBDEFB; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #90CAF9; margin-bottom: 20px; }
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

# 3. BARRA LATERAL
with st.sidebar:
    st.markdown("<h2 style='color: #FFD600; text-align: center;'>🛡️ SISTEMA DE CONFIANÇA</h2>", unsafe_allow_html=True)
    st.write("---")
    
    if 'autenticado' not in st.session_state: st.session_state.autenticado = False
    
    if not st.session_state.autenticado:
        u = st.text_input("Usuário")
        s = st.text_input("Senha", type="password")
        if st.button("ACESSAR"):
            if u == "admin" and s == "2026":
                st.session_state.autenticado = True
                st.rerun()
        st.stop()
    
    turmas = ["8º01", "8º02", "8º03", "9º01", "9º02", "8º04", "8º05", "9º03", "9º04", "9º05"]
    turma_sel = st.selectbox("📂 Selecione a Turma", turmas)
    st.write("---")
    st.markdown("🏛️ **Ano MMXXVI**")

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
tab_diario, tab_livros, tab_regras = st.tabs(["📊 Desempenho e Créditos", "📖 Material Didático", "📜 Regras do Pacto"])

with tab_diario:
    try:
        df = carregar_dados(turma_sel)
        
        # Métrica de Crédito Médio e Botão de Crédito Coletivo
        media_turma = df['SALDO'].mean()
        col_m1, col_m2 = st.columns([2, 1])
        with col_m1:
            st.markdown(f"""<div class="metric-card"><h4 style='margin:0; color:#1A237E;'>📈 Crédito Médio: {turma_sel}</h4><h2 style='margin:0; color:#1A237E;'>{media_turma:.2f} pts</h2></div>""", unsafe_allow_html=True)
        with col_m2:
            if st.button("⭐ CRÉDITO COLETIVO (+0.5)"):
                st.balloons()
                st.success("Bom desempenho da turma registrado!")

        st.write("### Relação de Alunos")
        for index, row in df.iterrows():
            with st.expander(f"👤 {row['NOME']}", expanded=False):
                c1, c2, c3 = st.columns([1, 1, 1.5])
                
                val_saldo = float(row['SALDO'])
                cor = "green" if val_saldo >= 9 else "orange" if val_saldo >= 7 else "red"
                c1.metric("Saldo de Confiança", f"{val_saldo:.1f}")
                
                c2.write(f"**AV1:** {row['AV1']} | **AV2:** {row['AV2']}")
                
                with c3:
                    motivo = st.selectbox("Selecione a Ocorrência:", 
                        ["Acompanhamento de rotina", "Material/Sono (-0.2)", "Tarefa não realizada (-0.5)", "Atitude inconveniente/Indisciplina (-0.5)", "Seminário/Trabalho não realizado (-1.0)", "Destaque Positivo (+0.2)"], 
                        key=f"sel_{index}")
                    
                    texto_zap = (f"*História MMXXVI* 🛡️\n\n"
                                 f"Olá! Informo o saldo de *{row['NOME']}*: *{val_saldo:.1f} pts*.\n"
                                 f"Motivo: {motivo}.\n"
                                 f"Notas: AV1: {row['AV1']} | AV2: {row['AV2']}\n\n"
                                 f"Prof. Luiz Alberto Pepino")
                    
                    st.link_button("📱 Notificar Responsável", 
                                   f"https://wa.me/{str(row['TELEFONE']).split('.')[0]}?text={urllib.parse.quote(texto_zap)}")

    except Exception as e:
        st.error(f"Erro ao carregar dados.")

with tab_livros:
    st.subheader("📚 Material Didático Bimestral")
    st.link_button("📘 Livro Didático - 1º Bimestre", "https://raw.githubusercontent.com/LUIZALBERTOPEPINO/historia-em-foco-2026/main/livro_8_9_bim1.pdf")

with tab_regras:
    st.markdown("""
    ### 📜 Diretrizes do Crédito de Confiança
    O saldo de **10.0 pontos** reflete a confiança inicial depositada no aluno. 
    Abaixo estão os critérios transparentes para manutenção dessa pontuação:
    
    **Débitos (Perda de Pontos):**
    * 📕 **-0,2 pts:** Material incompleto, sono ou desatenção.
    * 📝 **-0,5 pts:** Tarefa de casa ou classe não realizada.
    * 🚫 **-0,5 pts:** Atitude inconveniente ou indisciplina.
    * ❌ **-1,0 pts:** Seminários ou trabalhos não entregues.
    
    **Créditos (Ganho de Pontos):**
    * ⭐ **+0,2 pts:** Destaque positivo, participação exemplar ou auxílio aos colegas.
    """)
    
    st.markdown(f"""
    <div class="disclaimer">
        ⚠️ <b>Informação Importante:</b> Este aplicativo é uma ferramenta suplementar de gestão pedagógica do Prof. Luiz Alberto Pepino. 
        Este app não substitui os documentos oficiais (boletins e históricos) emitidos pela escola, e este serve somente 
        para que os pais ou responsáveis façam acompanhamento do desempenho dos alunos.
    </div>
    """, unsafe_allow_html=True)
