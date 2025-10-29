import pandas as pd



# --- Tabela 1: KPIs GLOBAIS (NOVA!) ---
# Esta é a tabela mestra que unifica os funis para o cálculo de CPL/CPA/CAC
db_kpis_globais = pd.DataFrame({
    "Canal": ["Tráfego Pago", "LinkedIn", "Apollo"],
    "Custo Total": [
        2500,  # Custo simulado total do Tráfego Pago
        1200,  # Custo simulado total do LinkedIn (ferramentas + SDR)
        800    # Custo simulado total do Apollo (licença + listas)
    ],
    "Leads": [
        1000, # Total de Leads (do db_funil_trafego_pago)
        0,    # LinkedIn não gera "Leads" da mesma forma
        0     # Apollo não gera "Leads" da mesma forma
    ],
    "Agendamentos": [
        310,  # Total de Agendamentos (do db_funil_trafego_pago)
        32,   # Total de Agendamentos (do db_linkedin_campanhas)
        35    # Total de Agendamentos (do db_apollo_campanhas)
    ],
    "Vendas": [
        52,   # Total de Vendas (do db_funil_trafego_pago)
        3,    # Simulação: 3 vendas vieram do LinkedIn
        2     # Simulação: 2 vendas vieram do Apollo
    ]
})


# --- Tabela 2: Tráfego Pago (Semanal) ---
db_leads_semanal = pd.DataFrame({
    "Semana": pd.date_range("2025-07-01", periods=12, freq="W-MON"),
    "Leads Recebidos": [25, 32, 45, 50, 38, 47, 60, 55, 68, 70, 80, 76],
    "Custo": [150, 200, 280, 320, 250, 300, 400, 380, 450, 480, 550, 520] # Custo semanal
})

# --- Tabela 3: Tráfego Pago (Funil) ---
db_funil_trafego_pago = pd.DataFrame({
    "Etapa": ["Leads", "Whats", "Agenda", "Resposta", "Vendas"],
    "Quantidade": [1000, 620, 310, 140, 52]
})

# --- Tabela 4: LinkedIn (Campanhas) ---
db_linkedin_campanhas = pd.DataFrame({
    "Campanha": ["LinkedIn Aline", "Linkedin Ana", "Linkedin Paulo", "LinkedIn Helper Ale"],
    "Invite Sent": [210, 190, 480, 210],
    "Accepted": [120, 100, 316, 101],
    "Messages": [323, 290, 586, 375],
    "Replies": [70, 55, 136, 70],
    "Agendamentos": [7, 4, 15, 6],
    "Custo": [300, 300, 400, 200]  # ATUALIZADO: Custo por campanha/SDR
})

# --- Tabela 5: LinkedIn (Semanal) ---
db_linkedin_semanal = pd.DataFrame({
    "Semana": pd.date_range("2025-07-01", periods=8, freq="W-MON"),
    "Mensagens": [50, 75, 100, 150, 200, 220, 250, 240],
    "Respostas": [5, 12, 18, 25, 32, 40, 48, 45],
    "Agendamentos": [0, 1, 1, 2, 3, 4, 5, 4]
})

# --- Tabela 6: Apollo (Campanhas) ---
db_apollo_campanhas = pd.DataFrame({
    "Campanha": [ "UBSmart - Teste Grátis",  "UBSmart - CEOs",  "Taste UB-Smart", "Michigan USA - Grant",  "LinkedIn Teste Grátis" ],
    "Emails Enviados": [0, 0, 0, 0, 6932],
    "Emails Abertos": [0, 0, 0, 0, 659],
    "Respostas": [0, 0, 0, 0, 50],
    "Agendamentos": [0, 0, 0, 0, 35],
    "Bounces": [0, 0, 0, 0, 210],
    "Custo": [0, 0, 0, 0, 800] 
})

# --- Tabela 7: Apollo (Semanal) ---
db_apollo_semanal = pd.DataFrame({
    "Semana": pd.date_range("2025-07-01", periods=8, freq="W-MON"),
    "Enviados": [0, 0, 0, 0, 0, 0, 0, 271],
    "Abertos": [0, 0, 0, 0, 0, 0, 0, 8.0],
    "Respostas": [0, 0, 0, 0, 0, 0, 0, 0.4],
    "Bounces": [0, 0, 0, 0, 0, 0, 0, 12]
})

# --- Tabela 8: Público (Descritivo) ---
db_publico_campanhas = pd.DataFrame({
    "Campanha": [
        "Teste UB-smart", "LinkedIn Teste Grátis", "Métricas Brasil",
        "UB-smart Produção", "LinkedIn com CEO", "LinkedIn Helper", "Outros"
    ],
    "Descrição": [
        "Focado em cargos superiores de manufatura e qualidade, empresas com >100 funcionários, Brasil inteiro.",
        "Similar ao anterior, mas com foco em teste gratuito.",
        "Campanhas para área de produção e processos industriais.",
        "Campanha voltada a gerentes e diretores da produção.",
        "Campanha direcionada a CEOs e diretores industriais.",
        "Campanha de apoio e remarketing.",
        "-"
    ]
})


# -------------------------------------------------------------------
# FUNÇÕES DE ACESSO A DADOS (GETTERS)
# -------------------------------------------------------------------

def get_kpis_globais():
    """
    Retorna a tabela mestra unificada de KPIs.
    """
    return db_kpis_globais.copy()

def get_dados_trafego_pago():
    """
    Retorna os DataFrames brutos de Tráfego Pago.
    """
    return db_leads_semanal.copy(), db_funil_trafego_pago.copy()

def get_dados_linkedin():
    """
    Retorna os DataFrames brutos de Campanhas do LinkedIn.
    """
    return db_linkedin_campanhas.copy(), db_linkedin_semanal.copy()

def get_dados_apollo_publico():
    """
    Retorna os DataFrames brutos de Apollo e Público.
    """
    return db_apollo_campanhas.copy(), db_apollo_semanal.copy(), db_publico_campanhas.copy()

