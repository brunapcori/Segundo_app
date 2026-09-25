import pandas as pd
import streamlit as st

# -----------------------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Simulador de Custos e Orçamento",
    page_icon="💰",
    layout="wide"
)

# -----------------------------------------------------------------------------
# BASE DE DADOS INTERNA
# -----------------------------------------------------------------------------
@st.cache_data
def carregar_dados() -> pd.DataFrame:
    dados = [
        {"Item": "Aço Carbono", "Categoria": "Matéria-Prima", "Valor (R$)": 4500.00, "Prioridade": "Alta"},
        {"Item": "Chapas de Alumínio", "Categoria": "Matéria-Prima", "Valor (R$)": 3200.00, "Prioridade": "Média"},
        {"Item": "Desenvolvedor Python", "Categoria": "Mão de Obra", "Valor (R$)": 6500.00, "Prioridade": "Alta"},
        {"Item": "Designer UX/UI", "Categoria": "Mão de Obra", "Valor (R$)": 3800.00, "Prioridade": "Média"},
        {"Item": "Frete Rodoviário", "Categoria": "Logística", "Valor (R$)": 1800.00, "Prioridade": "Baixa"},
        {"Item": "Importação Expressa", "Categoria": "Logística", "Valor (R$)": 2400.00, "Prioridade": "Média"},
        {"Item": "Conta de Luz Industrial", "Categoria": "Energia", "Valor (R$)": 1500.00, "Prioridade": "Alta"},
        {"Item": "Licença de Software CAD", "Categoria": "Ferramentas", "Valor (R$)": 1200.00, "Prioridade": "Média"},
        {"Item": "Brocas e Furadeiras", "Categoria": "Ferramentas", "Valor (R$)": 850.00, "Prioridade": "Baixa"},
        {"Item": "Serviço de Solda", "Categoria": "Mão de Obra", "Valor (R$)": 2100.00, "Prioridade": "Alta"},
    ]
    return pd.DataFrame(dados)

df_base = carregar_dados()

# -----------------------------------------------------------------------------
# BARRA LATERAL (SIDEBAR)
# -----------------------------------------------------------------------------
st.sidebar.header("⚙️ Parâmetros do Projeto")

orcamento_total = st.sidebar.slider(
    label="Orçamento Total Disponível (R$)",
    min_value=5000,
    max_value=50000,
    value=20000,
    step=500,
    format="R$ %d"
)

categorias_disponiveis = df_base["Categoria"].unique().tolist()

categorias_selecionadas = st.sidebar.multiselect(
    label="Filtrar por Categorias:",
    options=categorias_disponiveis,
    default=categorias_disponiveis
)

# -----------------------------------------------------------------------------
# LÓGICA DE FILTRAGEM E CÁLCULOS
# -----------------------------------------------------------------------------
if categorias_selecionadas:
    df_filtrado = df_base[df_base["Categoria"].isin(categorias_selecionadas)]
else:
    df_filtrado = df_base.iloc[0:0]  # DataFrame vazio caso nada seja selecionado

gasto_total_filtrado = df_filtrado["Valor (R$)"].sum()
saldo_restante = orcamento_total - gasto_total_filtrado

# -----------------------------------------------------------------------------
# ÁREA PRINCIPAL
# -----------------------------------------------------------------------------
st.title("💰 Simulador de Custos e Orçamento")
st.caption("Acompanhe gastos simulados, aplique filtros dinâmicos e controle o saldo em tempo real.")

st.markdown("---")

# PAINEL DE MÉTRICAS
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Orçamento Definido",
        value=f"R$ {orcamento_total:,.2f}"
    )

with col2:
    st.metric(
        label="Gasto Filtrado",
        value=f"R$ {gasto_total_filtrado:,.2f}"
    )

with col3:
    st.metric(
        label="Saldo Restante",
        value=f"R$ {saldo_restante:,.2f}",
        delta=f"R$ {saldo_restante:,.2f}"
    )

# ALERTAS CONDICIONAIS
if saldo_restante >= 0:
    st.success(f"✅ **Projeto dentro da meta!** Você possui **R$ {saldo_restante:,.2f}** disponíveis.")
else:
    estouro = abs(saldo_restante)
    st.error(f"⚠️ **Atenção: Orçamento excedido!** O valor ultrapassou a meta em **R$ {estouro:,.2f}**.")

st.markdown("---")

# GRÁFICO E TABELA
if not df_filtrado.empty:
    col_grafico, col_tabela = st.columns([1, 1])

    with col_grafico:
        st.subheader("📊 Gastos por Categoria")
        # Agrupamento para exibição no gráfico
        df_agrupado = df_filtrado.groupby("Categoria")["Valor (R$)"].sum().reset_index()
        df_agrupado = df_agrupado.set_index("Categoria")
        
        st.bar_chart(df_agrupado, horizontal=True)

    with col_tabela:
        st.subheader("📋 Itens Filtrados")
        st.dataframe(
            df_filtrado,
            use_container_width=True,
            hide_index=True
        )
else:
    st.warning("Nenhuma categoria selecionada na barra lateral. Ajuste os filtros para visualizar os dados.")
