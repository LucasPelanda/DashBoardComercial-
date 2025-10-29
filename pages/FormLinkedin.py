import streamlit as st
import pandas as pd
import datetime


# --- Configuração da Página ---
st.set_page_config(
    page_title="Lançamento - LinkedIn",
    layout="centered"
)

st.title("🔗 Lançamento Manual — LinkedIn (SDRs)")
st.caption("Insira os dados brutos semanais das campanhas ou SDRs do LinkedIn.")

st.markdown("---")

# --- Formulários do LinkedIn ---

# Simula um banco de dados de campanhas/SDRs usando st.session_state
st.session_state.linkedin_campanhas_cadastradas = [
    "LinkedIn Aline",
    "Linkedin Ana",
    "Linkedin Paulo",
    "LinkedIn Helper Ale"
]



st.subheader("Lançamento Semanal (LinkedIn)")
st.markdown("Insira os dados semanais para uma campanha ou SDR específico.")

with st.form(key="form_linkedin_lancamento"):
    
    # 1. Campo de Data
    semana_referencia_linkedin = st.date_input(
        "Semana de Referência (LinkedIn)",
        value=datetime.date.today()
    )
    
    # 2. Dropdown de Campanha/SDR
    campanha_selecionada = st.selectbox(
        "Selecione a Campanha/SDR",
        options=st.session_state.linkedin_campanhas_cadastradas
    )
    
    # 3. Campos Numéricos
    custo_semanal_linkedin = st.number_input(
        "Custo da Semana (para esta campanha) (R$)",
        min_value=0.0,
        format="%.2f",
        step=50.0
    )
    
    st.markdown("Métricas de Prospecção:")
    col1, col2, col3 = st.columns(3)
    with col1:
        invite_sent = st.number_input(
            "Convites Enviados (Invite Sent)",
            min_value=0,
            step=5
        )
    with col2:
        accepted = st.number_input(
            "Aceitos (Accepted)",
            min_value=0,
            step=1
        )
    with col3:
        messages = st.number_input(
            "Mensagens (Messages)",
            min_value=0,
            step=5
        )

    st.markdown("Métricas de Conversão:")
    col4, col5, col6 = st.columns(3)
    with col4:
        replies = st.number_input(
            "Respostas (Replies)",
            min_value=0,
            step=1
        )
    with col5:
        agendamentos = st.number_input(
            "Agendamentos (desta campanha)",
            min_value=0,
            step=1
        )
    with col6:
        vendas = st.number_input(
            "Vendas (desta campanha)",
            min_value=0,
            step=1
        )

    # 4. Botão de Envio
    submitted_linkedin = st.form_submit_button("Salvar Lançamento do LinkedIn")

# --- Lógica de Submissão do Lançamento ---
if submitted_linkedin:
    st.success(f"Dados salvos para a campanha '{campanha_selecionada}' na semana de {semana_referencia_linkedin}!")
    
    # Criamos o dicionário com os dados
    data_dict_linkedin = {
        "Semana": [semana_referencia_linkedin],
        "Campanha": [campanha_selecionada],
        "Custo": [custo_semanal_linkedin],
        "Invite Sent": [invite_sent],
        "Accepted": [accepted],
        "Messages": [messages],
        "Replies": [replies],
        "Agendamentos": [agendamentos],
        "Vendas": [vendas]
    }
    
    st.dataframe(pd.DataFrame(data_dict_linkedin), hide_index=True, use_container_width=True)
    
    # Próximo passo (lógica do backend):
    # bk.salvar_dados_linkedin(data_dict_linkedin)
    # st.cache_data.clear()