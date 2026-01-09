import streamlit as st
import pandas as pd
import urllib.parse

# 1. CONFIGURAÇÕES ESTÉTICAS E TÍTULO
st.set_page_config(page_title="História Itacoatiara 2026", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD !important; } 
    [data-testid="stSidebar"] { background-color: #1565C0 !important; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    .card { background-color: white; padding: 15px; border-radius: 10px; border-left: 5px solid #0D47A1; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 2. IDENTIFICAÇÃO E CONEXÃO
SHEET_ID = "1HFRKm-NY5jvlx6W_pV8AA1fmNq8wOwng5su4V4U3DLU"

def carregar_dados(aba_nome):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(aba_nome.strip())}"
    df = pd.read_csv(url)
    df.columns = [str(c).strip().upper() for c in df.columns]
    return df

# 3. LOGIN
if 'autenticado' not in st.session_state: st.session_state.autenticado = False

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3429/3429404.png", width=100) # Ícone de História
    st.title("🛡️ Painel do Professor")
    if not st.session_state.autenticado:
        u = st.text_input("Usuário")
        s = st.text_input("Senha", type="password")
        if st.button("Acessar Sistema"):
            if u == "admin" and s == "2026":
                st.session_state.autenticado = True
                st.rerun()
            else: st.error("Dados incorretos")
        st.stop()

# 4. INTERFACE PRINCIPAL (PÓS-LOGIN)
turmas = ["8º01", "8º02", "8º03", "9º01", "9º02", "8º04", "8º05", "9º03", "9º04", "9º05"]
turma_sel = st.sidebar.selectbox("📅 Selecione a Turma", turmas)

# ABAS DE NAVEGAÇÃO
tab_diario, tab_livros, tab_regras = st.tabs(["📊 Diário e Créditos", "📚 Livros Didáticos", "📜 Regras do Pacto"])

# --- ABA 1: DIÁRIO E CRÉDITOS ---
with tab_diario:
    try:
        df = carregar_dados(turma_sel)
        st.subheader(f"Lista de Alunos - {turma_sel}")
        
        for index, row in df.iterrows():
            nome = row['NOME']
            saldo = float(row['SALDO'])
            cor = "green" if saldo >= 9 else "orange" if saldo >= 7 else "red"
            
            with st.container():
                # Layout: Nome/Notas | Saldo | Ações | Zap
                c1, c2, c3, c4 = st.columns([2.5, 1, 4, 1.5])
                
                with c1:
                    st.markdown(f"**{nome}**")
                    st.caption(f"AV1: {row['AV1']} | AV2: {row['AV2']}")
                
                c2.markdown(f"<h2 style='color:{cor}; margin:0;'>{saldo:.1f}</h2>", unsafe_allow_html=True)
                
                with c3:
                    # Botões de Ocorrências Específicas
                    b1, b2, b3, b4 = st.columns(4)
                    # Nota: Como ainda não ativamos a escrita automática para evitar perda de dados teste, 
                    # os botões aqui geram a mensagem para o Zap com o motivo.
                    if b1.button("📕 -0.2", key=f"mat_{index}", help="Material/Sono"):
                        st.session_state[f"msg_{index}"] = "esquecimento de material ou desatenção em sala"
                    if b2.button("📝 -0.5", key=f"tar_{index}", help="Tarefa"):
                        st.session_state[f"msg_{index}"] = "não realização da tarefa de casa/classe"
                    if b3.button("🚫 -0.5", key=f"ati_{index}", help="Atitude"):
                        st.session_state[f"msg_{index}"] = "atitude inconveniente ou indisciplina"
                    if b4.button("⭐ +0.2", key=f"des_{index}", help="Destaque"):
                        st.session_state[f"msg_{index}"] = "participação exemplar e destaque positivo"

                with c4:
                    motivo = st.session_state.get(f"msg_{index}", "acompanhamento de rotina")
                    texto_zap = (f"*História em Foco (M. Ivone)* 🛡️\n\n"
                                 f"Olá! Informo o saldo de confiança de *{nome}*: *{saldo:.1f} pts*.\n"
                                 f"Status: {motivo}.\n"
                                 f"Notas: AV1: {row['AV1']} | AV2: {row['AV2']}\n\n"
                                 f"Obrigado pela parceria!")
                    link_whatsapp = f"https://wa.me/{str(row['TELEFONE']).split('.')[0]}?text={urllib.parse.quote(texto_zap)}"
                    st.link_button("📱 Notificar", link_whatsapp)
                st.markdown("---")

    except Exception as e:
        st.error(f"Erro ao carregar turma. Verifique a aba '{turma_sel}' na planilha.")

# --- ABA 2: LIVROS DIDÁTICOS ---
with tab_livros:
    st.subheader("📖 Biblioteca Digital de História")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**1º Bimestre**")
        st.link_button("📄 Abrir PDF (5MB)", "https://raw.githubusercontent.com/LUIZALBERTOPEPINO/historia-em-foco-2026/main/livro_8_9_bim1.pdf")
        st.info("**2º Bimestre**")
        st.button("🔒 Disponível em breve", disabled=True, key="b2")
    with col2:
        st.info("**3º Bimestre**")
        st.button("🔒 Disponível em breve", disabled=True, key="b3")
        st.info("**4º Bimestre**")
        st.button("🔒 Disponível em breve", disabled=True, key="b4")

# --- ABA 3: REGRAS DO PACTO ---
with tab_regras:
    st.markdown(f"""
    ### 📜 O Pacto da Confiança - Prof. Luiz Alberto
    Para garantir a transparência com os pais e alunos das turmas de **8ºs e 9ºs anos**, 
    utilizamos o sistema de crédito comportamental:
    
    * **Saldo Inicial:** 10.0 pontos (Crédito de Confiança).
    * **Perda de Material ou Dormir em aula:** -0,2 pts.
    * **Tarefa de casa/classe não realizada:** -0,5 pts.
    * **Atitude inconveniente / Indisciplina:** -0,5 pts.
    * **Não realização de Seminários/Trabalhos:** -1,0 pts.
    * **⭐ Destaque Positivo / Participação:** +0,2 pts.
    
    *As notas de AV1 e AV2 são somadas ao desempenho atitudinal para compor a média bimestral.*
    """)
