import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="História em Foco 2026", layout="wide", page_icon="🛡️")

# Estilos Visuais Avançados
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    .st-key-bonus-col { background-color: #FFD700 !important; color: black !important; }
    .st-key-destaque { background-color: #FFF9C4 !important; color: #5D4037 !important; border: 1px solid #FBC02D !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Sistema Crédito de Confiança")
st.caption("Itacoatiara - Prof. Luiz Alberto | Versão Final 2026")

aba1, aba2 = st.tabs(["📊 Painel de Aula", "📜 Regras e Transparência"])

# --- ABA DE REGRAS ---
with aba2:
    st.markdown("""
    ### 📜 Guia para Pais e Alunos
    O aprendizado de História depende de compromisso. O aluno inicia com **10.0 pontos**.
    
    #### 🎓 Bloco Acadêmico (7.0 pts):
    * **🎤 Seminário/Apresentação:** Atividade de fala e pesquisa. (-1.0 se ausente)
    * **🎮 Jogos/Rodadas de Conversa:** Participação ativa. (-0.2 se não participar)
    
    #### ⚠️ Bloco de Atitude (3.0 pts):
    * **🚫 Atitude Inconveniente:** Desrespeito, palavrões ou bagunça grave. (-0.5)
    * **💬 Conversa/Sono/Material:** Falta de foco ou organização. (-0.2)
    * **⭐ Destaque Positivo:** Participação excepcional. (+0.2)
    """)

# --- ABA PRINCIPAL ---
with aba1:
    # Simulando a base que virá do Google Sheets no dia 20/01
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame({
            'Nome': ['Adria', 'Davy', 'Gustavo', 'Aluno Especial (Exemplo)'],
            'Turma': ['7º 03', '7º 03', '9º 01', '7º 03'],
            'Categoria': ['Regular', 'Regular', 'Regular', 'Especial'],
            'Saldo': [10.0, 10.0, 10.0, 10.0],
            'Telefone': ['5592999999999', '5592999999999', '5592999999999', '5592999999999']
        })

    st.sidebar.header("⚙️ Controle")
    turma_sel = st.sidebar.selectbox("Turma Atual", sorted(st.session_state.df['Turma'].unique()))
    
    if st.sidebar.button("🏆 BÔNUS COLETIVO (+1.0)", key="bonus-col"):
        st.session_state.df.loc[st.session_state.df['Turma'] == turma_sel, 'Saldo'] += 1.0
        st.rerun()

    alunos_turma = st.session_state.df[st.session_state.df['Turma'] == turma_sel]

    for index, row in alunos_turma.iterrows():
        with st.container():
            c1, c2, c3, c4 = st.columns([1.5, 0.8, 4.2, 1.5])
            
            c1.write(f"**{row['Nome']}**")
            cor = "green" if row['Saldo'] >= 9 else "orange" if row['Saldo'] >= 7 else "red"
            c2.markdown(f"<h3 style='color:{cor}; margin:0;'>{row['Saldo']:.1f}</h3>", unsafe_allow_html=True)

            if row['Categoria'] == 'Regular':
                with c3:
                    ac, cp = st.columns(2)
                    with ac: # ACADÊMICO
                        if st.button(f"🎤 Seminário (-1.0)", key=f"s_{index}"):
                            st.session_state.df.at[index, 'Saldo'] -= 1.0
                            st.rerun()
                        if st.button(f"🎮 Jogo/Rodada (-0.2)", key=f"j_{index}"):
                            st.session_state.df.at[index, 'Saldo'] -= 0.2
                            st.rerun()
                    with cp: # COMPORTAMENTO
                        if st.button(f"🚫 Inconveniente (-0.5)", key=f"i_{index}"):
                            st.session_state.df.at[index, 'Saldo'] -= 0.5
                            st.rerun()
                        # Botão de Destaque Individual
                        if st.button(f"⭐ DESTAQUE (+0.2)", key=f"destaque_{index}"):
                            st.session_state.df.at[index, 'Saldo'] += 0.2
                            st.rerun()
            else:
                with c3:
                    obs = st.text_input("Obs. do Cuidador/Professor:", key=f"obs_{index}", placeholder="Como foi o dia dele?")
                    st.caption("🌟 Aluno com acompanhamento diferenciado")

            with c4:
                msg_base = f"*História em Foco 🛡️*\nOlá! O saldo de *{row['Nome']}* é *{row['Saldo']:.1f}*."
                if row['Categoria'] == 'Especial' and obs:
                    msg_base += f"\n*Observação:* {obs}"
                
                msg = f"{msg_base}\nVeja as regras: https://historia-itacoatiara.streamlit.app"
                st.link_button("📱 Notificar", f"https://wa.me/{row['Telefone']}?text={urllib.parse.quote(msg)}")
            st.divider()
