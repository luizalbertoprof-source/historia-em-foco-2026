import streamlit as st
import pandas as pd
import urllib.parse

# Configurações de exibição
st.set_page_config(page_title="Gestão História MMXXVI", layout="wide")

# Estilo focado em produtividade para o professor
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD !important; }
    .status-card { background-color: white; padding: 10px; border-radius: 5px; border-left: 5px solid #1A237E; }
    .nota-final { font-size: 1.2rem; font-weight: bold; color: #1A237E; }
    </style>
    """, unsafe_allow_html=True)

SHEET_ID = "1HFRKm-NY5jvlx6W_pV8AA1fmNq8wOwng5su4V4U3DLU"

def carregar_dados(aba_nome):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(aba_nome.strip())}"
    df = pd.read_csv(url)
    df.columns = [str(c).strip().upper() for c in df.columns]
    return df

# Cabeçalho simplificado para uso do professor
st.title("🛡️ Painel de Gestão: História MMXXVI")
st.caption(f"Prof. Luiz Alberto Pepino | Escola Maria Ivone")

# Barra Lateral
turmas = ["8º01", "8º02", "8º03", "9º01", "9º02", "8º04", "8º05", "9º03", "9º04", "9º05"]
turma_sel = st.sidebar.selectbox("Escolha a Turma", turmas)

try:
    df = carregar_dados(turma_sel)
    
    # Métrica da Turma
    media_confianca = df['SALDO'].mean()
    st.metric(f"Média de Confiança: {turma_sel}", f"{media_confianca:.2f}")

    for index, row in df.iterrows():
        # CÁLCULO DA NOTA FINAL PROPORCIONAL
        # Aqui o Saldo de Confiança entra como bônus ou ônus na média das AVs
        av1 = float(row['AV1'])
        av2 = float(row['AV2'])
        saldo = float(row['SALDO'])
        
        media_provisoria = (av1 + av2) / 2
        # O ajuste: Se saldo é 10, ajuste é 0. Se saldo é 9.5, ajuste é -0.5.
        ajuste = saldo - 10.0
        nota_final = media_provisoria + ajuste
        
        # Garante que a nota não seja menor que zero nem maior que 10
        nota_final = max(0.0, min(10.0, nota_final))

        with st.container():
            c1, c2, c3, c4 = st.columns([2, 2, 2, 1])
            
            with c1:
                st.write(f"👤 **{row['NOME']}**")
                st.caption(f"Telefone: {row['TELEFONE']}")

            with c2:
                st.write(f"AV1: {av1} | AV2: {av2}")
                st.markdown(f"Saldo: **{saldo:.1f}**")

            with c3:
                cor_final = "blue" if nota_final >= 6 else "red"
                st.markdown(f"Nota Final Projetada:")
                st.markdown(f"<span class='nota-final' style='color:{cor_final}'>{nota_final:.2f}</span>", unsafe_allow_html=True)

            with c4:
                # O Zap continua sendo sua ferramenta de comunicação com o pai
                motivo = "Acompanhamento de rotina" # Aqui você pode expandir se quiser
                texto_zap = f"Olá! Saldo de {row['NOME']}: {saldo:.1f}. Nota Final Projetada: {nota_final:.2f}."
                st.link_button("📱 Zap", f"https://wa.me/{str(row['TELEFONE']).split('.')[0]}?text={urllib.parse.quote(texto_zap)}")
            
            st.divider()

except Exception as e:
    st.error("Erro ao carregar os dados. Verifique a planilha.")
