import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="História em Foco 2026", layout="wide", page_icon="🛡️")

# Estilos Visuais
st.markdown("""
    <style>
    .stNumberInput>div>div>input { font-weight: bold; color: #01579B; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 2.2em; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Sistema Crédito de Confiança")
st.caption("Itacoatiara - Prof. Luiz Alberto | Gestão Acadêmica Integrada")

aba1, aba2 = st.tabs(["📊 Painel de Aula e Notas", "📜 Regras do Sistema"])

# --- REGRAS ---
with aba2:
    st.markdown("""
    ### 📜 Composição da Nota Final
    O saldo de **10.0** pontos é composto por:
    1. **Atividades Acadêmicas (7.0 pts):** Notas de AV1, AV2, Seminários e Jogos.
    2. **Engajamento e Atitude (3.0 pts):** Comportamento, Participação e Destaque.
    """)

# --- PAINEL PRINCIPAL ---
with aba1:
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

    st.sidebar.header("⚙️ Ferramentas")
    turma_sel = st.sidebar.selectbox("Selecionar Turma", sorted(st.session_state.df['Turma'].unique()))
    
    alunos_turma = st.session_state.df[st.session_state.df['Turma'] == turma_sel]

    for index, row in alunos_turma.iterrows():
        with st.container():
            # Layout expandido para caber as notas
            c1, c2, c3, c4, c5 = st.columns([1.5, 0.7, 1.5, 3.0, 1.5])
            
            c1.write(f"**{row['Nome']}**")
            
            # Semáforo do Saldo
            cor = "green" if row['Saldo'] >= 9 else "orange" if row['Saldo'] >= 7 else "red"
            c2.markdown(f"<h3 style='color:{cor}; margin:0;'>{row['Saldo']:.1f}</h3>", unsafe_allow_html=True)

            # NOVOS CAMPOS: Entrada de Notas
            with c3:
                nova_av1 = st.number_input("AV1", min_value=0.0, max_value=10.0, value=float(row['AV1']), key=f"av1_{index}", step=0.5)
                if nova_av1 != row['AV1']:
                    st.session_state.df.at[index, 'AV1'] = nova_av1
                    st.rerun()

            # BOTÕES DE ATITUDE E ACADÊMICO
            if row['Categoria'] == 'Regular':
                with c4:
                    col_a, col_b = st.columns(2)
                    if col_a.button(f"🎤 Seminário (-1.0)", key=f"s_{index}"):
                        st.session_state.df.at[index, 'Saldo'] -= 1.0
                        st.rerun()
                    if col_a.button(f"🚫 Atitude (-0.5)", key=f"i_{index}"):
                        st.session_state.df.at[index, 'Saldo'] -= 0.5
                        st.rerun()
                    if col_b.button(f"💬 Conversa (-0.2)", key=f"c_{index}"):
                        st.session_state.df.at[index, 'Saldo'] -= 0.2
                        st.rerun()
                    if col_b.button(f"⭐ DESTAQUE (+0.2)", key=f"d_{index}"):
                        st.session_state.df.at[index, 'Saldo'] += 0.2
                        st.rerun()
            else:
                c4.info("🌟 Acompanhamento Diferenciado")

            # NOTIFICAÇÃO COM NOTA DA AV1
            with c5:
                msg = (f"*História em Foco 🛡️*\n"
                       f"Olá! Informo o desempenho de *{row['Nome']}*:\n"
                       f"📝 *Nota AV1:* {row['AV1']}\n"
                       f"🛡️ *Crédito Atual:* {row['Saldo']:.1f}\n"
                       f"Regras: https://historia-itacoatiara.streamlit.app")
                st.link_button("📱 Notificar", f"https://wa.me/{row['Telefone']}?text={urllib.parse.quote(msg)}")
            st.divider()
