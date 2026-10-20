import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da página
st.set_page_config(
    page_title="Dashboard de Gastos Digitais e Pessoais",
    page_icon="💳",
    layout="wide"
)

# 2. Inicialização dos dados no Estado da Sessão (Session State)
if "df_gastos" not in st.session_state:
    dados_iniciais = {
        "Descrição": ["Netflix", "Supermercado", "Spotify", "Academia", "iCloud", "Restaurante"],
        "Tipo": ["Digital", "Pessoal", "Digital", "Pessoal", "Digital", "Pessoal"],
        "Categoria": ["Assinatura", "Alimentação", "Assinatura", "Saúde/Lazer", "Serviço Nuvem", "Alimentação"],
        "Valor (R$)": [55.90, 420.00, 21.90, 110.00, 14.90, 85.50],
        "Data": ["2026-10-01", "2026-10-05", "2026-10-08", "2026-10-10", "2026-10-12", "2026-10-15"]
    }
    st.session_state.df_gastos = pd.DataFrame(dados_iniciais)

# Título do Dashboard
st.title("📊 Dashboard de Gastos Digitais e Pessoais")
st.markdown("Acompanhe e controle suas assinaturas virtuais e despesas do dia a dia.")

# 3. Barra Lateral (Sidebar) - Adicionar novos gastos
st.sidebar.header("➕ Cadastrar Novo Gasto")

with st.sidebar.form("form_novo_gasto", clear_on_submit=True):
    descricao = st.text_input("Descrição do Gasto", placeholder="Ex: ChatGPT, Feira, Amazon")
    tipo = st.selectbox("Tipo de Gasto", ["Digital", "Pessoal"])
    categoria = st.selectbox(
        "Categoria", 
        ["Assinatura/SaaS", "Serviço Nuvem", "Jogos/Lazer Digital", "Alimentação", "Saúde/Fitness", "Transporte", "Outros"]
    )
    valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f", step=5.0)
    data = st.date_input("Data do Gasto")
    
    submitted = st.form_submit_button("Salvar Gasto")
    
    if submitted:
        if descricao and valor > 0:
            novo_registro = pd.DataFrame([{
                "Descrição": descricao,
                "Tipo": tipo,
                "Categoria": categoria,
                "Valor (R$)": valor,
                "Data": str(data)
            }])
            st.session_state.df_gastos = pd.concat([st.session_state.df_gastos, novo_registro], ignore_index=True)
            st.sidebar.success("Gasto cadastrado com sucesso!")
        else:
            st.sidebar.error("Preencha a descrição e um valor maior que R$ 0,00.")

df = st.session_state.df_gastos

# 4. Métricas Principais (KPIs)
col1, col2, col3 = st.columns(3)

total_geral = df["Valor (R$)"].sum()
total_digital = df[df["Tipo"] == "Digital"]["Valor (R$)"].sum()
total_pessoal = df[df["Tipo"] == "Pessoal"]["Valor (R$)"].sum()

col1.metric("💰 Total de Gastos", f"R$ {total_geral:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col2.metric("🌐 Gastos Digitais", f"R$ {total_digital:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col3.metric("🛍️ Gastos Pessoais", f"R$ {total_pessoal:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.markdown("---")

# 5. Visualizações e Gráficos
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("🌐 Proporção: Digital vs Pessoal")
    if not df.empty:
        fig_pizza = px.pie(
            df, 
            names="Tipo", 
            values="Valor (R$)", 
            hole=0.4,
            color_discrete_sequence=["#4CAF50", "#2196F3"]
        )
        st.plotly_chart(fig_pizza, use_container_width=True)

with col_graf2:
    st.subheader("📌 Gastos por Categoria")
    if not df.empty:
        df_cat = df.groupby("Categoria")["Valor (R$)"].sum().reset_index()
        fig_barras = px.bar(
            df_cat, 
            x="Categoria", 
            y="Valor (R$)", 
            text_auto=".2f",
            color="Categoria"
        )
        st.plotly_chart(fig_barras, use_container_width=True)

st.markdown("---")

# 6. Tabela de Registros
st.subheader("📑 Detalhamento dos Gastos")
st.dataframe(
    df.sort_values(by="Data", ascending=False),
    use_container_width=True,
    hide_index=True
)
