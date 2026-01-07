import streamlit as st
import pandas as pd
import urllib.parse

# 1. CONFIGURAÇÃO DE TEMA (Paleta Azul solicitada)
st.set_page_config(page_title="História em Foco 2026", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    /* Fundo Azul Claro */
    .stApp { background-color: #E3F2FD; }
    /* Sidebar Azul mais forte */
    [data-testid="stSidebar"] { background-color: #1976D2; color: white; }
    [data-testid="stSidebar"] * { color: white !important; }
    /* Estilo dos Botões */
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    .st-key-login_btn { background-color: #0D47A1; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE LOGIN SIMPLES
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

def login():
    st.sidebar.title("🔐 Acesso Restrito")
    usuario = st.sidebar.text_input("Usuário (CPF ou Matrícula)")
    senha = st.sidebar.text_input("Senha", type="password")
    if st.sidebar.button("Entrar", key="login_btn"):
        # Aqui você definirá uma lógica de senha por aluno/pai em janeiro
        if usuario == "admin" and senha == "2026": # Exemplo para o Prof.
            st.session_state.autenticado = True
            st.session_state.perfil = "professor"
            st.rerun()
        elif usuario and senha: # Lógica para pais
            st.session_state.autenticado = True
            st.session_state.perfil = "pai"
            st.session_state.usuario_logado = usuario
            st.rerun()

if not st.session_state.autenticado:
    login()
    st.warning("Por favor, faça o login para acessar os dados de desempenho.")
    st.stop()

# 3. CABEÇALHO PERSONALIZADO
col_img, col_tit = st.columns([1, 4])
with col_img:
    # Tenta carregar a imagem que você subiu no GitHub
    try:
        st.image("perfil.png", width=150)
    except:
        st.info("Coloque a foto 'perfil.png' no GitHub")

with col_tit:
    st.markdown(f"""
    # Sistema de Crédito de Confiança
    **Disciplina:** História | **Prof:** Luiz Alberto Pepino
    **Escola:** Estadual Maria Ivone de Araújo Leite
    *Itacoatiara, Amazonas - 2026*
    """)

# 4. ABAS DO SISTEMA
aba_painel, aba_materiais, aba_regras = st.tabs(["📊 Desempenho", "📚 Materiais de Estudo", "📜 Regras Claras"])

with aba_regras:
    st.markdown("""
    ### 🛡️ Guia do Pacto de Confiança (Para Pais e Alunos)
    Este sistema visa premiar a autonomia e o respeito. O aluno inicia com **10.0 pontos**.
    
    **1. Bloco de Atividades (7.0 pontos):**
    - **AV1 e AV2:** Notas das provas bimestrais.
    - **Seminários:** Apresentação e pesquisa (-1.0 se não realizar).
    - **Leitura e Jogos:** Participação nas dinâmicas (-0.2 se não participar).
    
    **2. Bloco de Atitude (3.0 pontos):**
    - **Respeito:** Atitudes inconvenientes, palavrões ou desrespeito (-0.5).
    - **Foco:** Dormir em sala ou conversa paralela (-0.2).
    - **Material:** Esquecimento de livro/caderno (-0.2).
    
    **3. Bonificações:**
    - **🏆 Coletivo:** Turma toda colaborativa (+1.0).
    - **⭐ Destaque:** Aluno que superou as expectativas (+0.2).
    """)

with aba_materiais:
    st.subheader("📖 Material Didático e Apoio")
    # Busca do Livro do 7º Ano
    busca = st.text_input("🔍 Pesquisar no Livro do 7º Ano (Temas, Capítulos...)", placeholder="Ex: Brasil Holandês")
    if busca:
        st.write(f"Resultados para: '{busca}' no livro 'Viver História'...")
        # Link para o PDF que você anexou (ajustaremos para o link direto em janeiro)
        st.markdown("[📄 Abrir Livro do 7º Ano (PDF)](https://github.com/seu-usuario/seu-repo/raw/main/EDIT-Viver-Historia-História-7-ano.pdf)")
    
    st.divider()
    st.subheader("🎥 Vídeos e Leituras Sugeridas")
    st.write("🔗 [Vídeo: A Formação do Brasil Colonial](https://youtube.com)")
    st.write("🔗 [Artigo: O Ciclo do Ouro em Minas Gerais](https://google.com)")

with aba_painel:
    # Simulação de dados (Será substituído pelo Google Sheets em 20/01)
    df = pd.DataFrame({
        'Nome': ['Adria', 'Davy', 'Gustavo'],
        'Turma': ['7º 03', '7º 03', '9º 01'],
        'Saldo': [10.0, 9.8, 10.0],
        'AV1': [8.5, 7.0, 9.0],
        'AV2': [0.0, 0.0, 0.0],
        'Telefone': ['5592999999999', '5592999999999', '5592999999999']
    })

    if st.session_state.perfil == "professor":
        turma = st.selectbox("Selecione a Turma", df['Turma'].unique())
        # Lógica de botões igual à anterior para o professor...
    else:
        st.info(f"Olá! Exibindo dados apenas de: {st.session_state.usuario_logado}")
        # Lógica de filtro para o pai ver apenas o seu filho
