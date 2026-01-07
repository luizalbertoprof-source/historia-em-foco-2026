import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="História em Foco 2026", layout="wide", page_icon="🛡️")

# Estilos Visuais (Azul Maria Ivone)
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD !important; } 
    [data-testid="stSidebar"] { background-color: #1565C0 !important; }
    input { color: #000000 !important; background-color: #FFFFFF !important; -webkit-text-fill-color: #000000 !important; }
    .stButton>button { border-radius: 8px; font-weight: bold; font-size: 11px; }
    </style>
    """, unsafe_allow_html=True)

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

# Cabeçalho Atualizado (8º e 9º Anos)
st.markdown("### 🛡️ Sistema de Crédito de Confiança\n**História: 8ºs e 9ºs Anos** | Prof. Luiz Alberto Pepino | Maria Ivone - 2026")

# Inicialização da Base com Turmas de 8º e 9º
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame({
        'Nome': ['Exemplo 8º Ano', 'Exemplo 9º Ano', 'Aluno Especial'],
        'Turma': ['8º 01', '9º 01', '8º 01'],
        'AV1': [0.0, 0.0, 0.0], 'AV2': [0.0, 0.0, 0.0], 'Saldo': [10.0, 10.0, 10.0],
        'Ultima_Ocorrencia': ['Nenhuma', 'Nenhuma', 'Nenhuma'],
        'Telefone': ['5592999999999', '5592999999999', '5592999999999'],
        'Categoria': ['Regular', 'Regular', 'Especial']
    })

aba_painel, aba_material, aba_regras = st.tabs(["📊 Diário e Notas", "📖 Livro Didático", "📜 Regras"])

with aba_regras:
    st.markdown("### 📜 Regras: Material/Sono (-0.2) | Tarefa (-0.5) | Atitude (-0.5) | Seminário (-1.0) | Destaque (+0.2)")

with aba_material:
    st.subheader("📚 Material Didático - 1º Bimestre")
    st.write("Abaixo está o recorte do livro didático para as turmas de 8º e 9º anos.")
    # Substitua 'SEU_USUARIO' pelo seu nome no GitHub
    link_pdf = "https://raw.githubusercontent.com/LUIZALBERTOPEPINO/historia-em-foco-2026/main/livro_8_9_bim1.pdf"
    st.link_button("📄 Abrir Livro (PDF 5MB)", link_pdf)
    st.info("Dica: Use este material para estudar para as AVs e realizar as tarefas de casa.")

with aba_painel:
    turma_sel = st.sidebar.selectbox("Selecionar Turma", sorted(st.session_state.df['Turma'].unique()))
    alunos = st.session_state.df[st.session_state.df['Turma'] == turma_sel]

    for index, row in alunos.iterrows():
        with st.container():
            c1, c2, c3, c4, c5 = st.columns([1.5, 1.2, 0.6, 3.5, 1.2])
            c1.write(f"**{row['Nome']}**")
            with c2:
                n1, n2 = st.columns(2)
                row['AV1'] = n1.number_input("AV1", 0.0, 10.0, float(row['AV1']), key=f"v1_{index}")
                row['AV2'] = n2.number_input("AV2", 0.0, 10.0, float(row['AV2']), key=f"v2_{index}")
            
            cor = "green" if row['Saldo'] >= 9 else "orange" if row['Saldo'] >= 7 else "red"
            c3.markdown(f"<h3 style='color:{cor}; margin:0;'>{row['Saldo']:.1f}</h3>", unsafe_allow_html=True)

            with c4:
                bt1, bt2, bt3, bt4 = st.columns(4)
                if bt1.button("📕 -0.2", key=f"b1_{index}"):
                    st.session_state.df.at[index, 'Saldo'] -= 0.2
                    st.session_state.df.at[index, 'Ultima_Ocorrencia'] = "esquecimento de material ou desatenção"; st.rerun()
                if bt2.button("📝 -0.5", key=f"b2_{index}"):
                    st.session_state.df.at[index, 'Saldo'] -= 0.5
                    st.session_state.df.at[index, 'Ultima_Ocorrencia'] = "não realização da tarefa"; st.rerun()
                if bt3.button("🚫 -0.5", key=f"b3_{index}"):
                    st.session_state.df.at[index, 'Saldo'] -= 0.5
                    st.session_state.df.at[index, 'Ultima_Ocorrencia'] = "atitude inconveniente"; st.rerun()
                if bt4.button("⭐ +0.2", key=f"b4_{index}"):
                    st.session_state.df.at[index, 'Saldo'] += 0.2
                    st.session_state.df.at[index, 'Ultima_Ocorrencia'] = "participação exemplar"; st.rerun()

            with c5:
                msg = f"*História 🛡️*\nSaldo de *{row['Nome']}*: *{row['Saldo']:.1f}*.\nMotivo: {row['Ultima_Ocorrencia']}."
                st.link_button("📱 Zap", f"https://wa.me/{row['Telefone']}?text={urllib.parse.quote(msg)}")
            st.divider()
