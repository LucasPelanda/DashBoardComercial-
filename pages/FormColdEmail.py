import streamlit as st
import pandas as pd
import datetime


# --- Configuração da Página ---
st.set_page_config(
    page_title="Lançamento - Apollo",
    layout="centered"
)

st.title("Lançamento Manual — Cold Email (Apollo)")
st.caption("Insira os dados brutos semanais das campanhas do Apollo.")

st.markdown("---")

# --- Formulários do Apollo (Cold Email) ---

# Para simular um banco de dados de campanhas, vamos usar o st.session_state
# Isso armazena uma lista de campanhas enquanto o app está rodando.
st.session_state.apollo_campanhas_cadastradas = [
    "UBSmart - Teste Grátis",
    "UBSmart - CEOs",
    "Taste UB-Smart",
    "Michigan USA - Grant",
    "LinkedIn Teste Grátis"
]



st.subheader("Lançamento Semanal (Apollo)")
st.markdown("Insira os dados semanais para uma campanha específica.")

with st.form(key="form_apollo_lancamento"):
    
    semana_referencia_apollo = st.date_input(
        "Semana de Referência (Apollo)",
        value=datetime.date.today()
    )
    
    #. Dropdown de Campanha
    # Usamos a lista que está no session_state
    campanha_selecionada = st.selectbox(
        "Selecione a Campanha",
        options=st.session_state.apollo_campanhas_cadastradas
    )
    
    # Campos Numéricos
    custo_semanal_apollo = st.number_input(
        "Custo da Semana (para esta campanha) (R$)",
        min_value=0.0,
        format="%.2f",
        step=50.0
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        emails_enviados = st.number_input(
            "Emails Enviados",
            min_value=0,
            step=10
        )
        emails_abertos = st.number_input(
            "Emails Abertos",
            min_value=0,
            step=1
        )
    with col2:
        respostas = st.number_input(
            "Respostas",
            min_value=0,
            step=1
        )
        bounces = st.number_input(
            "Bounces",
            min_value=0,
            step=1
        )
    with col3:
        agendamentos = st.number_input(
            "Agendamentos (desta campanha)",
            min_value=0,
            step=1
        )
        vendas = st.number_input(
            "Vendas (desta campanha)",
            min_value=0,
            step=1
        )

    # Botão de Envio
    submitted_apollo = st.form_submit_button("Salvar Lançamento do Apollo")

# --- Lógica de Submissão do Lançamento ---
if submitted_apollo:
    st.success(f"Dados salvos para a campanha '{campanha_selecionada}' na semana de {semana_referencia_apollo}!")
    
    # Criamos o dicionário com os dados
    data_dict_apollo = {
        "Semana": [semana_referencia_apollo],
        "Campanha": [campanha_selecionada],
        "Custo": [custo_semanal_apollo],
        "Emails Enviados": [emails_enviados],
        "Emails Abertos": [emails_abertos],
        "Respostas": [respostas],
        "Bounces": [bounces],
        "Agendamentos": [agendamentos],
        "Vendas": [vendas]
    }
    
    st.dataframe(pd.DataFrame(data_dict_apollo), hide_index=True, use_container_width=True)
    
    # Próximo passo (lógica do backend):
    # bk.salvar_dados_apollo(data_dict_apollo)
    # st.cache_data.clear()