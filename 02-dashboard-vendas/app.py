"""
Dashboard Interativo de Vendas

Autor: Anderson de Lima
Data: Janeiro 2026
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Carrega e processa os dados de vendas."""
    # Gera dados de exemplo (substitua pelo seu CSV real)
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
    
    data = {
        'data_venda': np.random.choice(dates, 5000),
        'id_produto': np.random.randint(1, 101, 5000),
        'categoria': np.random.choice(['Eletrônicos', 'Roupas', 'Alimentos', 'Livros', 'Esportes'], 5000),
        'quantidade': np.random.randint(1, 10, 5000),
        'preco_unitario': np.random.uniform(10, 500, 5000),
        'regiao': np.random.choice(['Norte', 'Sul', 'Leste', 'Oeste', 'Centro'], 5000),
        'id_cliente': np.random.randint(1, 501, 5000)
    }
    
    df = pd.DataFrame(data)
    df['receita'] = df['quantidade'] * df['preco_unitario']
    df['data_venda'] = pd.to_datetime(df['data_venda'])
    
    return df


def calculate_metrics(df):
    """Calcula métricas principais."""
    total_receita = df['receita'].sum()
    total_vendas = len(df)
    ticket_medio = df['receita'].mean()
    clientes_unicos = df['id_cliente'].nunique()
    
    return total_receita, total_vendas, ticket_medio, clientes_unicos


def main():
    """Função principal do dashboard."""
    
    # Header
    st.markdown('<h1 class="main-header">📊 Dashboard de Vendas</h1>', unsafe_allow_html=True)
    
    # Carrega dados
    df = load_data()
    
    # Sidebar - Filtros
    st.sidebar.header("🔍 Filtros")
    
    # Filtro de data
    min_date = df['data_venda'].min().date()
    max_date = df['data_venda'].max().date()
    
    date_range = st.sidebar.date_input(
        "Período",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Filtro de região
    regioes = ['Todas'] + sorted(df['regiao'].unique().tolist())
    regiao_selecionada = st.sidebar.selectbox("Região", regioes)
    
    # Filtro de categoria
    categorias = ['Todas'] + sorted(df['categoria'].unique().tolist())
    categoria_selecionada = st.sidebar.selectbox("Categoria", categorias)
    
    # Aplica filtros
    df_filtered = df.copy()
    
    if len(date_range) == 2:
        df_filtered = df_filtered[
            (df_filtered['data_venda'].dt.date >= date_range[0]) &
            (df_filtered['data_venda'].dt.date <= date_range[1])
        ]
    
    if regiao_selecionada != 'Todas':
        df_filtered = df_filtered[df_filtered['regiao'] == regiao_selecionada]
    
    if categoria_selecionada != 'Todas':
        df_filtered = df_filtered[df_filtered['categoria'] == categoria_selecionada]
    
    # Métricas principais
    total_receita, total_vendas, ticket_medio, clientes_unicos = calculate_metrics(df_filtered)
    
    # Display de métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Receita Total",
            value=f"R$ {total_receita:,.2f}",
            delta=f"{(total_receita / df['receita'].sum() * 100):.1f}% do total"
        )
    
    with col2:
        st.metric(
            label="🛒 Total de Vendas",
            value=f"{total_vendas:,}",
            delta=f"{(total_vendas / len(df) * 100):.1f}% do total"
        )
    
    with col3:
        st.metric(
            label="🎯 Ticket Médio",
            value=f"R$ {ticket_medio:,.2f}"
        )
    
    with col4:
        st.metric(
            label="👥 Clientes Únicos",
            value=f"{clientes_unicos:,}"
        )
    
    st.markdown("---")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Tendência de Vendas")
        
        # Agrupa por dia
        daily_sales = df_filtered.groupby(df_filtered['data_venda'].dt.date)['receita'].sum().reset_index()
        daily_sales.columns = ['Data', 'Receita']
        
        fig_trend = px.line(
            daily_sales,
            x='Data',
            y='Receita',
            title='Receita Diária',
            labels={'Receita': 'Receita (R$)', 'Data': 'Data'}
        )
        fig_trend.update_traces(line_color='#1f77b4', line_width=2)
        fig_trend.update_layout(hovermode='x unified')
        
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        st.subheader("🥧 Vendas por Região")
        
        sales_by_region = df_filtered.groupby('regiao')['receita'].sum().reset_index()
        
        fig_region = px.pie(
            sales_by_region,
            values='receita',
            names='regiao',
            title='Distribuição de Receita por Região',
            hole=0.4
        )
        fig_region.update_traces(textposition='inside', textinfo='percent+label')
        
        st.plotly_chart(fig_region, use_container_width=True)
    
    # Segunda linha de gráficos
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("📊 Top 10 Produtos")
        
        top_products = df_filtered.groupby('id_produto')['receita'].sum().sort_values(ascending=False).head(10).reset_index()
        top_products['id_produto'] = 'Produto ' + top_products['id_produto'].astype(str)
        
        fig_products = px.bar(
            top_products,
            x='receita',
            y='id_produto',
            orientation='h',
            title='Produtos com Maior Receita',
            labels={'receita': 'Receita (R$)', 'id_produto': 'Produto'}
        )
        fig_products.update_traces(marker_color='#2ca02c')
        fig_products.update_layout(yaxis={'categoryorder': 'total ascending'})
        
        st.plotly_chart(fig_products, use_container_width=True)
    
    with col4:
        st.subheader("🏷️ Vendas por Categoria")
        
        sales_by_category = df_filtered.groupby('categoria')['receita'].sum().sort_values(ascending=False).reset_index()
        
        fig_category = px.bar(
            sales_by_category,
            x='categoria',
            y='receita',
            title='Receita por Categoria',
            labels={'receita': 'Receita (R$)', 'categoria': 'Categoria'}
        )
        fig_category.update_traces(marker_color='#ff7f0e')
        
        st.plotly_chart(fig_category, use_container_width=True)
    
    # Heatmap
    st.subheader("🔥 Heatmap de Vendas")
    
    df_filtered['dia_semana'] = df_filtered['data_venda'].dt.dayofweek
    df_filtered['mes'] = df_filtered['data_venda'].dt.month
    
    heatmap_data = df_filtered.pivot_table(
        values='receita',
        index='dia_semana',
        columns='mes',
        aggfunc='sum',
        fill_value=0
    )
    
    dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=[meses[i-1] for i in heatmap_data.columns],
        y=[dias[i] for i in heatmap_data.index],
        colorscale='YlOrRd',
        hoverongaps=False
    ))
    
    fig_heatmap.update_layout(
        title='Receita por Dia da Semana e Mês',
        xaxis_title='Mês',
        yaxis_title='Dia da Semana'
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Tabela de dados
    with st.expander("📋 Ver Dados Detalhados"):
        st.dataframe(
            df_filtered[['data_venda', 'categoria', 'regiao', 'quantidade', 'preco_unitario', 'receita']]
            .sort_values('data_venda', ascending=False)
            .head(100),
            use_container_width=True
        )
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>Dashboard desenvolvido por Anderson de Lima | 
            <a href='https://github.com/198517'>GitHub</a> | 
            <a href='https://www.linkedin.com/in/anderson-de-lima-analista-de-dados/'>LinkedIn</a>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
