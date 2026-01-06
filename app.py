import streamlit as st
import pandas as pd
import urllib.parse

# Configuração de Tema e Estética
st.set_page_config(page_title="História em Foco 2026", layout="wide", page_icon="🛡️")

# Estilo CSS para botões coloridos e visual profissional
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    .st-key-bonus { background-color: #FFD700; color: black; }
    .st-key-material { background-color: #FF4B4B; color: white; }
    .st-key-tarefa { background-color: #FFA500; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Sistema Crédito de Confiança")
st.subheader("Itacoatiara - Prof. Luiz Alberto")

# Simulação de Base (Em 20/01 conectaremos ao Google Sheets)
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame({
        'Nome': ['Adria', 'Davy', 'Gustavo', 'Aluno Especial (Exemplo)'],
        'Turma': ['7º 03', '7º 03', '9º 01', '7º 03'],
        'Categoria': ['Regular', 'Regular', 'Regular', 'Especial'],
        'Saldo': [10.0, 10.0, 10.0, 10.0],
        'Telefone': ['5592999999999', '5592999999999', '5592999999999', '5592999999999']
    })

# Menu Lateral
st.sidebar.header("⚙️ Painel de Controle")
turma_sel = st.sidebar.selectbox("Selecione a Turma", sorted(st.session_state.df['Turma'].unique()))

# Ação Coletiva
if st.sidebar.button("🏆 ATRIBUIR BÔNUS COLETIVO (+1.0)", key="bonus"):
    st.session_state.df.loc[st.session_state.df['Turma'] == turma_sel, 'Saldo'] += 1.0
    st.sidebar.success(f"Bônus aplicado à turma {turma_sel}!")
    st.rerun()

# Listagem de Alunos
st.write(f"### Gerenciando: Turma {turma_sel}")
alunos_turma = st.session_state.df[st.session_state.df['Turma'] == turma_sel]

for index, row in alunos_turma.iterrows():
    with st.container():
        c1, c2, c3, c4 = st.columns([2, 1, 3, 2])
        
        c1.write(f"**{row['Nome']}**")
        c1.caption(f"Status: {row['Categoria']}")
        
        # Cor do Saldo (Semáforo)
        cor = "green" if row['Saldo'] >= 9 else "orange" if row['Saldo'] >= 7 else "red"
        c2.markdown(f"<h3 style='color:{cor}; margin:0;'>{row['Saldo']:.1f}</h3>", unsafe_allow_html=True)

        if row['Categoria'] == 'Regular':
            with c3:
                sc1, sc2 = st.columns(2)
                if sc1.button(f"📕 -0.2", key=f"mat_{index}"):
                    st.session_state.df.at[index, 'Saldo'] -= 0.2
                    st.rerun()
                if sc2.button(f"📝 -0.5", key=f"tar_{index}"):
                    st.session_state.df.at[index, 'Saldo'] -= 0.5
                    st.rerun()
        else:
            c3.info("🌟 Atendimento Especializado")

        # Botão WhatsApp Automático
        with c4:
            msg = f"*História em Foco 🛡️*\nOlá! Sou o Prof. Luiz Alberto.\nO saldo de confiança de *{row['Nome']}* hoje é *{row['Saldo']:.1f}*.\nObrigado pela parceria!"
            texto_zap = urllib.parse.quote(msg)
            link_zap = f"https://wa.me/{row['Telefone']}?text={texto_zap}"
            st.link_button("📱 Notificar Pai", link_zap)
        
        st.divider()

# Rodapé de Conteúdo
st.sidebar.markdown("---")
st.sidebar.subheader("📚 Links para Alunos")
st.sidebar.write("🔗 [Aula 01: O que é História?](https://youtube.com)")
