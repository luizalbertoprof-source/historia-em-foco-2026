import streamlit as st
import pandas as pd
import urllib.parse

# Configuração de Tema e Estética
st.set_page_config(page_title="História em Foco 2026", layout="wide", page_icon="🛡️")

# Estilo CSS para organizar os botões
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; font-size: 12px; height: 2.5em; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Sistema Crédito de Confiança")
st.caption("Itacoatiara - Prof. Luiz Alberto")

aba1, aba2 = st.tabs(["📊 Diário de Classe", "📜 Regras do Sistema"])

with aba2:
    st.markdown("""
    ### 📜 Regras para Pais e Alunos
    O **Crédito de Confiança (10.0)** avalia o compromisso e o respeito do aluno.
    
    #### 🟢 Pontos Positivos:
    * **🏆 Bônus Coletivo (+1,0):** Turma exemplar.
    * **⭐ Destaque (+0,2):** Participação brilhante.
    
    #### 🔴 Reduções por Atitude:
    * **📕 Material/Conversa/Dormir (-0,2):** Falta de foco ou esquecimento de material.
    * **📝 Tarefa não Realizada (-0,5):** Não entrega de deveres.
    * **🚫 Atitude Inconveniente (-0,5):** Bagunça, palavrões, gestos ou desrespeito.
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

    st.sidebar.header("⚙️ Painel do Professor")
    turma_sel = st.sidebar.selectbox("Selecione a Turma", sorted(st.session_state.df['Turma'].unique()))

    if st.sidebar.button("🏆 BÔNUS COLETIVO (+1.0)", key="bonus"):
        st.session_state.df.loc[st.session_state.df['Turma'] == turma_sel, 'Saldo'] += 1.0
        st.rerun()

    st.write(f"### Turma: {turma_sel}")
    alunos_turma = st.session_state.df[st.session_state.df['Turma'] == turma_sel]

    for index, row in alunos_turma.iterrows():
        with st.container():
            c1, c2, c3, c4 = st.columns([2, 1, 4, 2])
            
            # Coluna 1 e 2: Nome e Saldo
            c1.write(f"**{row['Nome']}**")
            cor = "green" if row['Saldo'] >= 9 else "orange" if row['Saldo'] >= 7 else "red"
            c2.markdown(f"<h3 style='color:{cor}; margin:0;'>{row['Saldo']:.1f}</h3>", unsafe_allow_html=True)

            # Coluna 3: Botões de Ação
            if row['Categoria'] == 'Regular':
                with c3:
                    r1, r2 = st.columns(2)
                    if r1.button(f"📕 Material (-0.2)", key=f"mat_{index}"):
                        st.session_state.df.at[index, 'Saldo'] -= 0.2
                        st.rerun()
                    if r1.button(f"💬 Conversa/Sono (-0.2)", key=f"conv_{index}"):
                        st.session_state.df.at[index, 'Saldo'] -= 0.2
                        st.rerun()
                    if r2.button(f"📝 Tarefa (-0.5)", key=f"tar_{index}"):
                        st.session_state.df.at[index, 'Saldo'] -= 0.5
                        st.rerun()
                    if r2.button(f"🚫 Inconveniente (-0.5)", key=f"inc_{index}"):
                        st.session_state.df.at[index, 'Saldo'] -= 0.5
                        st.rerun()
            else:
                c3.info("🌟 Atendimento Especializado")

            # Coluna 4: WhatsApp
            with c4:
                link_app = "https://historia-itacoatiara.streamlit.app"
                msg = f"*História em Foco 🛡️*\nOlá! O saldo de *{row['Nome']}* hoje é *{row['Saldo']:.1f}*.\nVerifique os detalhes aqui: {link_app}"
                st.link_button("📱 Notificar", f"https://wa.me/{row['Telefone']}?text={urllib.parse.quote(msg)}")
            st.divider()
