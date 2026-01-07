import streamlit as st
import pandas as pd
import urllib.parse

# 1. TEMA PERSONALIZADO (Azul e Estética Solicitada)
st.set_page_config(page_title="História em Foco 2026", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; } /* Azul Claro */
    [data-testid="stSidebar"] { background-color: #1565C0; color: white; } /* Azul Forte */
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE LOGIN
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

def login():
    st.sidebar.subheader("🔐 Acesso 2026")
    usuario = st.sidebar.text_input("Usuário")
    senha = st.sidebar.text_input("Senha", type="password")
    if st.sidebar.button("Entrar"):
        if usuario == "admin" and senha == "2026": # Senha mestra do Prof.
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.sidebar.error("Usuário ou senha incorretos")

if not st.session_state.autenticado:
    login()
    st.info("👋 Bem-vindo! Por favor, identifique-se no menu lateral para acessar o Sistema de Crédito de Confiança.")
    st.stop()

# 3. CABEÇALHO (Com o novo nome da Escola e Disciplina)
st.markdown(f"""
    # 🛡️ Sistema de Crédito de Confiança
    **Disciplina de História** | Prof. Luiz Alberto Pepino
    **Escola Estadual Maria Ivone de Araújo Leite**
    *Itacoatiara, Amazonas | 2026*
    """)
st.divider()

# 4. ABAS DE NAVEGAÇÃO
aba_painel, aba_links, aba_regras = st.tabs(["📊 Diário e Notas", "🔗 Links de Estudo", "📜 Regras do Pacto"])

with aba_regras:
    st.markdown("""
    ### 📜 Entenda o Crédito de Confiança (Saldo 10.0)
    O saldo avalia o compromisso integral do aluno em sala.
    
    **🔴 Reduções:**
    * **Material/Sono/Conversa:** -0,2
    * **Tarefa não realizada:** -0,5
    * **Atitude Inconveniente (Palavrão/Bagunça):** -0,5
    * **Seminário não realizado:** -1,0
    
    **🟢 Bonificações:**
    * **🏆 Bônus Coletivo:** +1,0 (Turma nota 10)
    * **⭐ Destaque Individual:** +0,2
    """)

with aba_links:
    st.subheader("📚 Conteúdos Sugeridos")
    st.info("Aqui você encontrará vídeos e leituras para reforçar o conteúdo das aulas.")
    st.write("👉 [Sugestão de Vídeo: Introdução à História](https://youtube.com)")
    st.write("👉 [Sugestão de Leitura: O Brasil no século XVIII](https://google.com)")

with aba_painel:
    # Base de dados fictícia (conectaremos ao Google Sheets no dia 20/01)
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame({
            'Nome': ['Adria', 'Davy', 'Gustavo', 'Aluno Especial'],
            'Turma': ['7º 03', '7º 03', '9º 01', '7º 03'],
            'Categoria': ['Regular', 'Regular', 'Regular', 'Especial'],
            'AV1': [0.0, 0.0, 0.0, 0.0],
            'AV2': [0.0, 0.0, 0.0, 0.0],
            'Saldo': [10.0, 10.0, 10.0, 10.0],
            'Telefone': ['5592999999999', '5592999999999', '5592999999999', '5592999999999']
        })

    st.sidebar.success("✅ Modo Professor Ativo")
    turma_sel = st.sidebar.selectbox("Escolha a Turma", sorted(st.session_state.df['Turma'].unique()))
    
    if st.sidebar.button("🏆 BÔNUS TURMA (+1.0)"):
        st.session_state.df.loc[st.session_state.df['Turma'] == turma_sel, 'Saldo'] += 1.0
        st.rerun()

    alunos_turma = st.session_state.df[st.session_state.df['Turma'] == turma_sel]

    for index, row in alunos_turma.iterrows():
        with st.container():
            c1, c2, c3, c4 = st.columns([1.5, 0.7, 4.0, 1.5])
            c1.write(f"**{row['Nome']}**")
            cor = "green" if row['Saldo'] >= 9 else "orange" if row['Saldo'] >= 7 else "red"
            c2.markdown(f"<h3 style='color:{cor}; margin:0;'>{row['Saldo']:.1f}</h3>", unsafe_allow_html=True)

            with c3:
                n1, n2, bt1, bt2 = st.columns([1,1,2,2])
                n1.number_input("AV1", 0.0, 10.0, float(row['AV1']), key=f"a1_{index}")
                n2.number_input("AV2", 0.0, 10.0, float(row['AV2']), key=f"a2_{index}")
                if bt1.button("📕 -0.2", key=f"m_{index}"):
                    st.session_state.df.at[index, 'Saldo'] -= 0.2
                    st.rerun()
                if bt2.button("🚫 -0.5", key=f"i_{index}"):
                    st.session_state.df.at[index, 'Saldo'] -= 0.5
                    st.rerun()
            
            with c4:
                msg = f"*História em Foco 🛡️*\nOlá! O saldo de *{row['Nome']}* é *{row['Saldo']:.1f}*."
                st.link_button("📱 Notificar", f"https://wa.me/{row['Telefone']}?text={urllib.parse.quote(msg)}")
            st.divider()
