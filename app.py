import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="História em Foco 2026", layout="wide", page_icon="🛡️")

# CSS para botões menores e organizados por cores
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 6px; font-size: 11px; height: 2.2em; margin-bottom: 2px; }
    .btn-acad { background-color: #E1F5FE; border: 1px solid #01579B; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Sistema Crédito de Confiança")
st.caption("Gestão de Sala: Comportamento + Acadêmico | Prof. Luiz Alberto")

aba1, aba2 = st.tabs(["📊 Painel de Aula", "📜 Regras do Sistema"])

with aba2:
    st.markdown("""
    ### 📜 Como funciona o seu Crédito (10.0)
    O saldo é dividido em: **7.0 (Atividades)**, **1.5 (Participação)** e **1.5 (Comportamento)**.
    
    #### 🎓 Atividades Acadêmicas (Peso no 7.0):
    * **📚 Provas/AV:** Avaliação formal de conhecimento.
    * **🎤 Seminários/Apres.:** Trabalho de pesquisa e fala em público (-1.0 se não realizar).
    * **🎮 Jogos/Rodadas:** Atividades interativas em sala (-0.2 se não participar).
    
    #### ⚠️ Comportamento e Foco:
    * **🚫 Inconveniente/Palavrão:** -0.5 pontos.
    * **💬 Conversa/Sono/Material:** -0.2 pontos.
    """)

with aba1:
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame({
            'Nome': ['Adria', 'Davy', 'Gustavo', 'Aluno Especial'],
            'Turma': ['7º 03', '7º 03', '9º 01', '7º 03'],
            'Categoria': ['Regular', 'Regular', 'Regular', 'Especial'],
            'Saldo': [10.0, 10.0, 10.0, 10.0],
            'Telefone': ['5592999999999', '5592999999999', '5592999999999', '5592999999999']
        })

    st.sidebar.header("⚙️ Painel do Mestre")
    turma_sel = st.sidebar.selectbox("Turma", sorted(st.session_state.df['Turma'].unique()))
    
    if st.sidebar.button("🏆 BÔNUS COLETIVO (+1.0)"):
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
                    # Divisão em Acadêmico e Comportamental
                    ac, cp = st.columns(2)
                    with ac: # Bloco de 7.0
                        if st.button(f"🎤 Seminário/Apres (-1.0)", key=f"sem_{index}"):
                            st.session_state.df.at[index, 'Saldo'] -= 1.0
                            st.rerun()
                        if st.button(f"🎮 Jogo/Rodada (-0.2)", key=f"jog_{index}"):
                            st.session_state.df.at[index, 'Saldo'] -= 0.2
                            st.rerun()
                    with cp: # Bloco de 3.0 (Part + Comp)
                        if st.button(f"🚫 Inconveniente (-0.5)", key=f"inc_{index}"):
                            st.session_state.df.at[index, 'Saldo'] -= 0.5
                            st.rerun()
                        if st.button(f"💬 Conversa/Sono/Mat (-0.2)", key=f"con_{index}"):
                            st.session_state.df.at[index, 'Saldo'] -= 0.2
                            st.rerun()
            else:
                c3.info("🌟 Acompanhamento Especializado")

            with c4:
                link_app = "https://historia-itacoatiara.streamlit.app"
                msg = f"*História em Foco 🛡️*\nOlá! O saldo de *{row['Nome']}* é *{row['Saldo']:.1f}*.\nAtividades e comportamento atualizados.\nRegras: {link_app}"
                st.link_button("📱 Notificar", f"https://wa.me/{row['Telefone']}?text={urllib.parse.quote(msg)}")
            st.divider()
