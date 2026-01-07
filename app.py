import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="História em Foco 2026", layout="wide", page_icon="🛡️")

# Estilos Visuais
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD !important; } 
    [data-testid="stSidebar"] { background-color: #1565C0 !important; }
    input { color: #000000 !important; background-color: #FFFFFF !important; -webkit-text-fill-color: #000000 !important; }
    .stButton>button { border-radius: 8px; font-weight: bold; font-size: 11px; }
    </style>
    """, unsafe_allow_html=True)

# Login (Usuário: admin | Senha: 2026)
if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if not st.session_state.autenticado:
    st.sidebar.title("🔐 Acesso")
    u = st.sidebar.text_input("Usuário")
    s = st.sidebar.text_input("Senha", type="password")
    if st.sidebar.button("Entrar"):
        if u == "admin" and s == "2026":
            st.session_state.autenticado = True
            st.rerun()
    st.stop()

# Cabeçalho
st.markdown("### 🛡️ Sistema de Crédito de Confiança\n**Prof. Luiz Alberto Pepino** | Maria Ivone de Araújo Leite - 2026")

# Inicialização da Base (Com coluna de última ocorrência)
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame({
        'Nome': ['Adria', 'Davy', 'Gustavo'],
        'Turma': ['7º 03', '7º 03', '9º 01'],
        'AV1': [0.0, 0.0, 0.0],
        'AV2': [0.0, 0.0, 0.0],
        'Saldo': [10.0, 10.0, 10.0],
        'Ultima_Ocorrencia': ['Nenhuma', 'Nenhuma', 'Nenhuma'],
        'Telefone': ['5592999999999', '5592999999999', '5592999999999']
    })

turma_sel = st.sidebar.selectbox("Selecionar Turma", sorted(st.session_state.df['Turma'].unique()))
alunos = st.session_state.df[st.session_state.df['Turma'] == turma_sel]

st.divider()

for index, row in alunos.iterrows():
    with st.container():
        # Colunas: Nome | Notas | Saldo | Ações | WhatsApp
        c1, c2, c3, c4, c5 = st.columns([1.5, 1.2, 0.6, 3.5, 1.2])
        
        c1.write(f"**{row['Nome']}**")
        
        with c2: # Notas
            n1, n2 = st.columns(2)
            new_v1 = n1.number_input("AV1", 0.0, 10.0, float(row['AV1']), key=f"v1_{index}", step=0.5)
            new_v2 = n2.number_input("AV2", 0.0, 10.0, float(row['AV2']), key=f"v2_{index}", step=0.5)
            if new_v1 != row['AV1'] or new_v2 != row['AV2']:
                st.session_state.df.at[index, 'AV1'] = new_v1
                st.session_state.df.at[index, 'AV2'] = new_v2
        
        # Saldo com cor
        cor = "green" if row['Saldo'] >= 9 else "orange" if row['Saldo'] >= 7 else "red"
        c3.markdown(f"<h3 style='color:{cor}; margin:0;'>{row['Saldo']:.1f}</h3>", unsafe_allow_html=True)

        with c4: # Ações e Registro de Ocorrência
            bt1, bt2, bt3, bt4 = st.columns(4)
            if bt1.button("📕 -0.2", help="Material/Sono", key=f"b1_{index}"):
                st.session_state.df.at[index, 'Saldo'] -= 0.2
                st.session_state.df.at[index, 'Ultima_Ocorrencia'] = "esquecimento de material ou desatenção (sono/conversa)"
                st.rerun()
            if bt2.button("📝 -0.5", help="Tarefa", key=f"b2_{index}"):
                st.session_state.df.at[index, 'Saldo'] -= 0.5
                st.session_state.df.at[index, 'Ultima_Ocorrencia'] = "não realização da tarefa de casa/classe"
                st.rerun()
            if bt3.button("🚫 -0.5", help="Atitude", key=f"b3_{index}"):
                st.session_state.df.at[index, 'Saldo'] -= 0.5
                st.session_state.df.at[index, 'Ultima_Ocorrencia'] = "atitude inconveniente ou indisciplina em sala"
                st.rerun()
            if bt4.button("⭐ +0.2", help="Destaque", key=f"b4_{index}"):
                st.session_state.df.at[index, 'Saldo'] += 0.2
                st.session_state.df.at[index, 'Ultima_Ocorrencia'] = "participação exemplar e destaque positivo na aula"
                st.rerun()

        with c5: # WhatsApp Específico
            texto_ocorrencia = row['Ultima_Ocorrencia']
            msg = (f"*História em Foco 🛡️*\n"
                   f"Olá! Informo o saldo de *{row['Nome']}*: *{row['Saldo']:.1f}*.\n"
                   f"Notas: AV1: {row['AV1']} | AV2: {row['AV2']}\n"
                   f"Último registro: {texto_ocorrencia}.\n"
                   f"Regras: https://historia-itacoatiara.streamlit.app")
            st.link_button("📱 Notificar", f"https://wa.me/{row['Telefone']}?text={urllib.parse.quote(msg)}")
        st.divider()
