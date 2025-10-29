
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import BackEnd as bk  



st.set_page_config(
    page_title="Dashboard Comercial — Ubivis",
    layout="wide",
)

st.title(" Dashboard Comercial — Ubivis")
st.markdown("Etapa 3 — Visão Unificada de Custos (CPL, CPAg, CAC)")
st.markdown("---")


#--------------------------------------------------------------
# VISÃO GERAL (CPL, CPAg, CAC)

st.header("Visão Geral — Métricas de Custo por Canal")

df_kpis = bk.get_kpis_globais()

#  Calcular CPL, CPAg (Custo por Agendamento) e CAC

df_kpis["CPL (Custo por Lead)"] = np.where(
    df_kpis["Leads"] > 0, df_kpis["Custo Total"] / df_kpis["Leads"], 0
)
df_kpis["CPAg (Custo por Agendamento)"] = np.where(
    df_kpis["Agendamentos"] > 0, df_kpis["Custo Total"] / df_kpis["Agendamentos"], 0
)
df_kpis["CAC (Custo por Venda)"] = np.where(
    df_kpis["Vendas"] > 0, df_kpis["Custo Total"] / df_kpis["Vendas"], 0
)

st.subheader("Métricas de Custo Unificadas")
st.markdown("Quanto custa para gerar um **Lead**, um **Agendamento** e uma **Venda** em cada canal.")

col1, col2, col3 = st.columns(3)

# Coluna para Tráfego Pago
with col1:
    kpi_pago = df_kpis[df_kpis["Canal"] == "Tráfego Pago"].iloc[0]
    st.markdown("#### Tráfego Pago")
    st.metric("CPL (Custo por Lead)", f"R$ {kpi_pago['CPL (Custo por Lead)']:.2f}")
    st.metric("CPAg (Custo por Agendamento)", f"R$ {kpi_pago['CPAg (Custo por Agendamento)']:.2f}")
    st.metric("CAC (Custo por Venda)", f"R$ {kpi_pago['CAC (Custo por Venda)']:.2f}")

# Coluna para LinkedIn
with col2:
    kpi_linkedin = df_kpis[df_kpis["Canal"] == "LinkedIn"].iloc[0]
    st.markdown("#### LinkedIn")
    st.metric("CPL (Custo por Lead)", "N/A") 
    st.metric("CPAg (Custo por Agendamento)", f"R$ {kpi_linkedin['CPAg (Custo por Agendamento)']:.2f}")
    st.metric("CAC (Custo por Venda)", f"R$ {kpi_linkedin['CAC (Custo por Venda)']:.2f}")

# Coluna para Apollo
with col3:
    kpi_apollo = df_kpis[df_kpis["Canal"] == "Apollo"].iloc[0]
    st.markdown("#### Apollo (Cold Mail)")
    st.metric("CPL (Custo por Lead)", "N/A") 
    st.metric("CPAg (Custo por Agendamento)", f"R$ {kpi_apollo['CPAg (Custo por Agendamento)']:.2f}")
    st.metric("CAC (Custo por Venda)", f"R$ {kpi_apollo['CAC (Custo por Venda)']:.2f}")


# 4. Exibir Tabela Resumo
st.subheader("Tabela de Conversão Unificada")
st.dataframe(
    df_kpis.style.format({
        "Custo Total": "R$ {:,.2f}",
        "CPL (Custo por Lead)": "R$ {:,.2f}",
        "CPAg (Custo por Agendamento)": "R$ {:,.2f}",
        "CAC (Custo por Venda)": "R$ {:,.2f}",
    }),
    use_container_width=True,
    hide_index=True
)

st.markdown("---")


#--------------------------------------------------------------
#  TRÁFEGO PAGO 

st.header("Análise Detalhada: Tráfego Pago")
st.subheader("Histórico semanal — Leads Recebidos")

db_leads_semanal, db_funil_trafego_pago = bk.get_dados_trafego_pago()

# Processar dados e calcular métricas
# (Cálculo do CPL Semanal)
db_leads_semanal["CPL Semanal"] = np.where(
    db_leads_semanal["Leads Recebidos"] > 0,
    db_leads_semanal["Custo"] / db_leads_semanal["Leads Recebidos"], 0
)

# Métricas de topo
leads_semana_atual = db_leads_semanal["Leads Recebidos"].iloc[-1]
leads_semana_passada = db_leads_semanal["Leads Recebidos"].iloc[-2]
variacao = ((leads_semana_atual - leads_semana_passada) / leads_semana_passada) * 100
media_4s = db_leads_semanal["Leads Recebidos"].tail(4).mean()
cpl_medio_periodo = db_leads_semanal["CPL Semanal"].replace(0, np.nan).mean() # Ignora semanas com 0


# 3. Exibir métricas
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        "Leads Recebidos (Sem. Atual)",
        f"{leads_semana_atual}",
        f"{variacao:+.1f}% vs sem. ant."
    )
with col2:
    st.metric("Média Leads (Últimas 4s)", f"{media_4s:.1f}")
with col3:
    st.metric("CPL Médio (Período)", f"R$ {cpl_medio_periodo:.2f}")

# 4. Gerar e exibir gráficos
st.subheader("Evolução Semanal (Leads x CPL)")


if db_leads_semanal["CPL Semanal"].max() > 0:
    db_leads_semanal["CPL Normalizado"] = (
        db_leads_semanal["CPL Semanal"] / db_leads_semanal["CPL Semanal"].max()
    ) * db_leads_semanal["Leads Recebidos"].max()
else:
    db_leads_semanal["CPL Normalizado"] = 0

fig_trafego = px.line(
    db_leads_semanal,
    x="Semana",
    y=["Leads Recebidos", "CPL Normalizado"],
    markers=True,
    title="Leads Recebidos vs CPL (Escala Normalizada)"
)

fig_trafego.data[0].name = "Leads Recebidos"
fig_trafego.data[1].name = "CPL Semanal (R$)"

fig_trafego.update_layout(
    yaxis_title="Leads / CPL (escala normalizada)",
    legend_title_text="Métrica",
    hovermode="x unified"
)

st.plotly_chart(fig_trafego, use_container_width=True)




st.subheader("Funil de Conversão — Tráfego Pago")
st.markdown("Etapas: **Leads → Whats → Agenda → Resposta → Vendas**")
fig_funil_pago = px.funnel(
    db_funil_trafego_pago,
    x="Quantidade",
    y="Etapa",
    title="Funil — Tráfego Pago"
)
st.plotly_chart(fig_funil_pago, use_container_width=True)

st.markdown("---")

#------------------------------------------------------------
#  LINKEDIN 

st.header("Análise Detalhada: Campanhas LinkedIn")

tabela_linkedin, db_linkedin_semanal = bk.get_dados_linkedin()

tabela_linkedin["Taxa Aceitação (%)"] = (tabela_linkedin["Accepted"] / tabela_linkedin["Invite Sent"]) * 100
tabela_linkedin["Taxa Resposta (%)"] = (tabela_linkedin["Replies"] / tabela_linkedin["Messages"]) * 100
tabela_linkedin["Taxa Conversão (Agenda/Respostas) %"] = np.where(
    tabela_linkedin["Replies"] > 0, (tabela_linkedin["Agendamentos"] / tabela_linkedin["Replies"]) * 100, 0
)

tabela_linkedin["CPAg (Custo por Agendamento)"] = np.where(
    tabela_linkedin["Agendamentos"] > 0, tabela_linkedin["Custo"] / tabela_linkedin["Agendamentos"], 0
)


total_convites = tabela_linkedin["Invite Sent"].sum()
total_agendamentos = tabela_linkedin["Agendamentos"].sum()
total_custo_linkedin = tabela_linkedin["Custo"].sum()
cpag_medio_linkedin = total_custo_linkedin / total_agendamentos if total_agendamentos > 0 else 0


col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Convites Enviados", f"{total_convites}")
with col2:
    st.metric("Agendamentos (Período)", f"{total_agendamentos}")
with col3:
    st.metric("Custo Total", f"R$ {total_custo_linkedin:,.2f}")
with col4:
    st.metric("CPAg Médio", f"R$ {cpag_medio_linkedin:.2f}")

# Gerar e exibir gráficos
fig_engajamento = px.line(
    db_linkedin_semanal,
    x="Semana",
    y=["Mensagens", "Respostas", "Agendamentos"],
    markers=True,
    title="Engajamento — Mensagens, Respostas e Agendamentos por Semana"
)
fig_engajamento.update_layout(legend_title_text="Métrica")
st.plotly_chart(fig_engajamento, use_container_width=True)

st.subheader("Funil de Conversão — LinkedIn")
funil_linkedin_df = pd.DataFrame({
    "Etapa": ["Convites", "Aceitos", "Respostas", "Agendamentos"], 
    "Quantidade": [
        tabela_linkedin["Invite Sent"].sum(),
        tabela_linkedin["Accepted"].sum(),
        tabela_linkedin["Replies"].sum(),
        tabela_linkedin["Agendamentos"].sum()
    ]
})
fig_funil_linkedin = px.funnel(
    funil_linkedin_df,
    x="Quantidade",
    y="Etapa",
    title="Funil de Conversão Geral — Campanhas LinkedIn"
)
st.plotly_chart(fig_funil_linkedin, use_container_width=True)

st.subheader("Campanhas com mais Agendamentos") 
fig_top_campanhas = px.bar(
    tabela_linkedin.sort_values(by="Agendamentos", ascending=True), 
    x="Agendamentos", 
    y="Campanha",
    orientation="h",
    color="Agendamentos",
    text="Agendamentos", 
    title="Campanhas com maior número de agendamentos"
)
fig_top_campanhas.update_traces(textposition="outside")
st.plotly_chart(fig_top_campanhas, use_container_width=True)

#  Exibir tabela detalhada
st.subheader(" Desempenho Detalhado por Campanha")
st.dataframe(
    tabela_linkedin[[
        "Campanha", "Custo", "Invite Sent", "Accepted", "Replies", "Agendamentos",
        "Taxa Resposta (%)", "Taxa Conversão (Agenda/Respostas) %", "CPAg (Custo por Agendamento)"
    ]].style.format({
        "Custo": "R$ {:,.2f}",
        "Taxa Resposta (%)": "{:.1f}%",
        "Taxa Conversão (Agenda/Respostas) %": "{:.1f}%",
        "CPAg (Custo por Agendamento)": "R$ {:,.2f}"
    }),
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

#-------------------------------------
# COLD EMAIL (APOLLO) 


st.header("Análise Detalhada: Cold Email — Apollo")
st.subheader(" Desempenho Geral das Campanhas")

dados_apollo, db_apollo_semanal, db_publico_campanhas = bk.get_dados_apollo_publico()


#---------- 
# Não sei como vamos tratar esses dados, esses contas deveiam ser feitas no back, mas coloquei aq por comordidadde 
#  Processar dados e calcular taxas
dados_apollo["Taxa Abertura (%)"] = np.where(
    dados_apollo["Emails Enviados"] > 0, (dados_apollo["Emails Abertos"] / dados_apollo["Emails Enviados"]) * 100, 0
)
dados_apollo["Taxa Resposta (%)"] = np.where(
    dados_apollo["Emails Enviados"] > 0, (dados_apollo["Respostas"] / dados_apollo["Emails Enviados"]) * 100, 0
)
#  Taxa de Agendamento (Agenda/Respostas)
dados_apollo["Taxa Agendamento (Agenda/Respostas) %"] = np.where(
    dados_apollo["Respostas"] > 0, (dados_apollo["Agendamentos"] / dados_apollo["Respostas"]) * 100, 0
)
#  CPAg (Custo por Agendamento)
dados_apollo["CPAg (Custo por Agendamento)"] = np.where(
    dados_apollo["Agendamentos"] > 0, dados_apollo["Custo"] / dados_apollo["Agendamentos"], 0
)
#  Taxa de Bounce
dados_apollo["Taxa Bounce (%)"] = np.where(
    dados_apollo["Emails Enviados"] > 0, (dados_apollo["Bounces"] / dados_apollo["Emails Enviados"]) * 100, 0
)



# Calcular métricas de topo
total_env = dados_apollo["Emails Enviados"].sum()
total_agendamentos_apollo = dados_apollo["Agendamentos"].sum()
total_custo_apollo = dados_apollo["Custo"].sum()
cpag_medio_apollo = total_custo_apollo / total_agendamentos_apollo if total_agendamentos_apollo > 0 else 0
taxa_bounce_media = (dados_apollo["Bounces"].sum() / total_env) * 100 if total_env > 0 else 0

# Exibir métricas de topo
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Emails Enviados", f"{total_env}")
with col2:
    st.metric("Agendamentos", f"{total_agendamentos_apollo}")
with col3:
    st.metric("CPAg Médio", f"R$ {cpag_medio_apollo:.2f}")
with col4:
    st.metric("Taxa de Bounce Média", f"{taxa_bounce_media:.1f}%", delta_color="inverse")


# Gerar e exibir gráficos
st.subheader("Evolução Semanal — Enviados, Respostas e Bounces")
fig_apollo = px.line(
    db_apollo_semanal,
    x="Semana",
    y=["Enviados", "Respostas", "Bounces"],
    markers=True,
    title="Histórico Semanal de Desempenho — Apollo"
)
fig_apollo.update_layout(legend_title_text="Métrica")
st.plotly_chart(fig_apollo, use_container_width=True)

st.subheader("Funil de Conversão — Cold Email (Apollo)")
st.markdown("Etapas: **Enviados → Abertos → Respostas → Agendamentos**")
funil_apollo_df = pd.DataFrame({
    "Etapa": ["Enviados", "Abertos", "Respostas", "Agendamentos"],
    "Quantidade": [
        dados_apollo["Emails Enviados"].sum(),
        dados_apollo["Emails Abertos"].sum(),
        dados_apollo["Respostas"].sum(),
        dados_apollo["Agendamentos"].sum()
    ]
})
fig_funil_apollo = px.funnel(
    funil_apollo_df,
    x="Quantidade",
    y="Etapa",
    title="Funil de Conversão Geral — Apollo"
)
st.plotly_chart(fig_funil_apollo, use_container_width=True)

# Exibir tabela detalhada e melhor campanha
st.subheader(" Desempenho Detalhado por Campanha")
st.dataframe(
    dados_apollo[[
        "Campanha", "Custo", "Emails Enviados", "Taxa Bounce (%)", "Taxa Abertura (%)",
        "Respostas", "Agendamentos", "CPAg (Custo por Agendamento)"
    ]].style.format({
        "Custo": "R$ {:,.2f}",
        "Taxa Bounce (%)": "{:.1f}%",
        "Taxa Abertura (%)": "{:.1f}%",
        "CPAg (Custo por Agendamento)": "R$ {:,.2f}"
    }),
    use_container_width=True,
    hide_index=True
)

# Lógica para "Melhor Campanha" (baseado no maior número de agendamentos)
# Vamos recalcular a taxa de agendamento sobre ENVIADOS para manter a lógica original
dados_apollo["Taxa Agendamento (Agenda/Enviados) %"] = np.where(
    dados_apollo["Emails Enviados"] > 0, (dados_apollo["Agendamentos"] / dados_apollo["Emails Enviados"]) * 100, 0
)
melhor_campanha = dados_apollo.loc[dados_apollo["Taxa Agendamento (Agenda/Enviados) %"].idxmax()]
st.markdown(
    f" **Campanha mais performática:** `{melhor_campanha['Campanha']}` com **{melhor_campanha['Taxa Agendamento (Agenda/Enviados) %']:.1f}%** de taxa de agendamento (sobre enviados)."
)


#-------------------------------------
# SEÇÃO 5: PÚBLICO DAS CAMPANHAS
#-------------------------------------
st.header("Público de cada campanha")
st.dataframe(
    db_publico_campanhas,
    use_container_width=True,
    hide_index=True
)

# --- Rodapé ---
st.markdown("---")
st.caption(" 2025 Ubivis — Dashboard Comercial (Etapa 3 - Custos Unificados)")

