import streamlit as st
import pandas as pd
import datetime


# --- Configuração da Página ---
st.set_page_config(
    page_title="Lançamento de Dados",
    layout="centered" 
)

st.title("  Lançamento Manual de Métricas")
st.caption("Insira os dados brutos da semana para atualizar o dashboard.")

st.markdown("---")

# --- Formulário de Tráfego Pago ---
st.header("Formulário: Tráfego Pago (Semanal)")
st.markdown("Insira os totais consolidados para a semana de referência.")

with st.form(key="form_trafego_pago"):
    
    semana_referencia = st.date_input(
        "Semana de Referência (selecione a segunda-feira da semana)",
        value=datetime.date.today()
    )
    
    custo_total = st.number_input(
        "Custo Total da Semana (R$)",
        min_value=0.0,
        format="%.2f",
        step=50.0
    )
    
    leads_gerados = st.number_input(
        "Leads Gerados (Total)",
        min_value=0,
        step=1
    )
    
    agendamentos_gerados = st.number_input(
        "Agendamentos Gerados (originados do Tráfego Pago)",
        min_value=0,
        step=1
    )
    
    vendas_geradas = st.number_input(
        "Vendas Geradas (originadas do Tráfego Pago)",
        min_value=0,
        step=1
    )

    submitted = st.form_submit_button("Salvar Lançamento de Tráfego Pago")

if submitted:
    st.success(f"Dados salvos para a semana de {semana_referencia}!")
    
    data_dict = {
        "Semana": [semana_referencia],
        "Custo Total": [custo_total],
        "Leads": [leads_gerados],
        "Agendamentos": [agendamentos_gerados],
        "Vendas": [vendas_geradas]
    }
    st.dataframe(pd.DataFrame(data_dict), hide_index=True, use_container_width=True)
