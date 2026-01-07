import streamlit as st
import pandas as pd
import urllib.parse

# 1. TEMA PERSONALIZADO (Azul e Estética Solicitada)
st.set_page_config(page_title="História em Foco 2026", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD !important; } 
    [data-testid="stSidebar"] { background-color: #1565C0 !important; }
    input { color: #000000 !important; background-color: #FFFFFF !important; -webkit-text-fill-color: #000000 !important; }
    [data-testid="stSidebar"] label { color: #FFFFFF !important; font-weight: bold !important; }
    .stButton>button { background-color: #0D47A1 !important; color: #FFFFFF !important; border: 2px solid #FFFFFF !important; }
    .santinho { background-color: #FFF9C4; border: 2px solid #FBC02D; border-radius: 10px; padding: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE LOGIN
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

def login():
    st.sidebar.title("🔐 Acesso 2026")
    usuario = st.sidebar.text_input("Usuário", placeholder="Matrícula ou Admin")
    senha = st.sidebar.text_input("Senha", type="password", placeholder="Sua senha")
    if st.sidebar.button("ENTRAR"):
        if usuario == "admin" and senha == "2026":
            st.session_state.autenticado = True
            st.session_state.perfil = "professor"
            st.rerun()
        else:
            # Aqui simularemos o login dos pais em janeiro
            st.session_state.autenticado = True
            st.session_state.perfil = "pai"
            st.session_state.usuario_logado = usuario
            st.rerun()

if not st.session_state.autenticado:
    login()
    st.info("🛡️ **Bem-vindo à Escola Estadual Maria Ivone de Araújo Leite.**\n\nPor favor, utilize o menu lateral para acessar o painel de História.")
    st.stop()

# 3. CABEÇALHO INTEGRADO
col_img, col_tit = st.columns([1, 4])
with col_img:
    try: st.image("perfil.png", width=120)
    except: st.warning("Subir perfil.png")

with col_tit:
    st.markdown(f"""
    # 🛡️ Sistema de Crédito de Confiança
    **Disciplina de História** | Prof. Luiz Alberto Pepino
    **Escola Estadual Maria Ivone de Araújo Leite** | Itacoatiara, 2026
    """)

aba_painel, aba_links, aba_regras = st.tabs(["📊 Desempenho", "🔗 Links de Estudo", "📜 Regras para Pais"])

with aba_regras:
    st.markdown("""
    ### 🤝 O Pacto de Confiança: Como Funciona?
    O objetivo é que cada aluno cuide do seu patrimônio de **10.0 pontos**.
    
    #### ✅ Como manter ou ganhar pontos:
    * **🏆 Comportamento da Turma:** Se a turma toda colaborar, todos ganham **+1.0 ponto**.
    * **⭐ Participação Extra:** Atitudes de destaque em sala somam **+0.2 pontos**.
    
    #### ❌ O que reduz o saldo:
    * **Leve (-0,2):** Conversa excessiva, dormir em sala ou esquecer o livro/caderno.
    * **Médio (-0,5):** Não realizar a tarefa do dia ou ter atitudes inconvenientes (palavrões/bagunça).
    * **Grave (-1,0):** Não realizar ou não apresentar seminários e trabalhos.
    """)

with aba_links:
    st.subheader("📚 Central de Estudos")
    st.write("Aqui o Prof. Luiz Alberto disponibilizará os vídeos e textos das aulas.")
    st.markdown("- [🎥 Vídeo: Introdução aos Estudos Históricos](https://youtube.com)")
    st.markdown("- [📄 Texto: O que é História e por que estudar?](https://google.com)")

with aba_painel:
    # Simulação da Planilha
    df = pd.DataFrame({
        'Nome': ['Adria', 'Davy', 'Gustavo', 'Aluno Especial'],
        'Turma': ['7º 03', '7º 03', '9º 01', '7º 03'],
        'Categoria': ['Regular', 'Regular', 'Regular', 'Especial'],
        'AV1': [9.5, 8.0, 10.0, 0.0],
        'AV2': [0.0, 0.0, 0.0, 0.0],
        'Saldo': [10.0, 9.2, 10.0, 10.0],
        'Telefone': ['5592999999999', '5592999999999', '5592999999999', '5592999999999']
    })

    if st.session_state.perfil == "professor":
        st.sidebar.success("✅ Modo Professor Ativo")
        turma_sel = st.sidebar.selectbox("Turma Atual", sorted(df['Turma'].unique()))
        
        # FILTRO DE SANTINHOS
        ver_santinhos = st.sidebar.checkbox("😇 Ver 'Santinhos' (Saldo 10)")
        
        alunos = df[df['Turma'] == turma_sel]
        if ver_santinhos:
            alunos = alunos[alunos['Saldo'] == 10.0]
            st.balloons()
            st.success("Exibindo apenas os alunos com Saldo Máximo! 🌟")

        for index, row in alunos.iterrows():
            with st.container():
                c1, c2, c3, c4 = st.columns([2, 1, 4, 1.5])
                c1.write(f"**{row['Nome']}**")
                cor = "green" if row['Saldo'] >= 9 else "orange" if row['Saldo'] >= 7 else "red"
                c2.markdown(f"<h3 style='color:{cor}; margin:0;'>{row['Saldo']:.1f}</h3>", unsafe_allow_html=True)
                
                with c3:
                    if row['Categoria'] == 'Regular':
                        ca, cb = st.columns(2)
                        if ca.button(f"📕 -0.2", key=f"m_{index}"): st.toast("Debitado!"); st.rerun()
                        if cb.button(f"🚫 -0.5", key=f"i_{index}"): st.toast("Debitado!"); st.rerun()
                    else: st.info("🌟 Acompanhamento Diferenciado")
                
                with c4:
                    msg = f"*História em Foco 🛡️*\nOlá! O saldo de *{row['Nome']}* é *{row['Saldo']:.1f}*."
                    st.link_button("📱 Notificar", f"https://wa.me/{row['Telefone']}?text={urllib.parse.quote(msg)}")
                st.divider()
    else:
        st.info("⚠️ Painel do Responsável: Em janeiro você verá aqui apenas o desempenho do seu filho.")
