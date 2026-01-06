import streamlit as st
import pandas as pd

# Configuração de Estética
st.set_page_config(page_title="História em Foco 2026", layout="wide")
st.title("🛡️ Sistema Crédito de Confiança - Prof. Luiz Alberto")

# Simulação de base de dados (Em janeiro, conectaremos ao seu Google Sheets)
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame({
        'Nome': ['Exemplo: José da Silva', 'Exemplo: Aluno Especial'],
        'Turma': ['7º 03', '7º 03'],
        'Categoria': ['Regular', 'Especial'],
        'Saldo': [10.0, 10.0],
        'Telefone': ['5592999999999', '5592999999999']
    })

# Menu Lateral - Filtros
turma_sel = st.sidebar.selectbox("Selecione a Turma", st.session_state.df['Turma'].unique())
alunos_turma = st.session_state.df[st.session_state.df['Turma'] == turma_sel]

# Botão de Bônus Coletivo
if st.button("🏆 ATRIBUIR BÔNUS COLETIVO (+1.0)"):
    st.session_state.df.loc[st.session_state.df['Turma'] == turma_sel, 'Saldo'] += 1.0
    st.success(f"Bônus de 1.0 aplicado a todos os alunos da {turma_sel}!")

st.divider()

# Lista de Gerenciamento
for index, row in alunos_turma.iterrows():
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        st.write(f"**{row['Nome']}** ({row['Categoria']})")
        st.metric("Saldo Atual", f"{row['Saldo']:.1f}")

    with col2:
        if row['Categoria'] == 'Regular':
            if st.button(f"📕 -0.2 (Material)", key=f"mat_{index}"):
                st.session_state.df.at[index, 'Saldo'] -= 0.2
                st.rerun()
            if st.button(f"📝 -0.5 (Tarefa)", key=f"tar_{index}"):
                st.session_state.df.at[index, 'Saldo'] -= 0.5
                st.rerun()
        else:
            st.info("⭐ Aluno com acompanhamento especial (Inclusivo)")

    with col3:
        msg = f"Olá! O aluno {row['Nome']} está com saldo {row['Saldo']:.1f} em História. 🟢"
        link_zap = f"https://wa.me/{row['Telefone']}?text={msg}"
        st.link_button("📱 Notificar Pai (WhatsApp)", link_zap)

st.sidebar.markdown("---")
st.sidebar.subheader("📚 Links de Ouro (Alunos)")
st.sidebar.write("[Vídeo: O que é História?](https://youtube.com)")
