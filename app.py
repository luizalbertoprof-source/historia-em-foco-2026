# Login Reforçado
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

def realizar_login():
    u = st.sidebar.text_input("Usuário", key="user_input")
    s = st.sidebar.text_input("Senha", type="password", key="pass_input")
    if st.sidebar.button("Entrar"):
        if u == "admin" and s == "2026":
            st.session_state.autenticado = True
            st.rerun() # Isso força o app a carregar as turmas agora
        else:
            st.sidebar.error("Usuário ou senha incorretos")

if not st.session_state.autenticado:
    realizar_login()
    st.info("👋 Por favor, faça o login no menu lateral para visualizar as turmas.")
    st.stop()
