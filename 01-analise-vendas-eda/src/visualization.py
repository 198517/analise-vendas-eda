"""
Módulo para visualização de dados de vendas.

Autor: Anderson de Lima
Data: Janeiro 2026
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Optional, Tuple


# Configurações de estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


class SalesVisualizer:
    """Classe para criar visualizações de dados de vendas."""
    
    def __init__(self, df: pd.DataFrame, figsize: Tuple[int, int] = (12, 6)):
        """
        Inicializa o visualizador.
        
        Args:
            df: DataFrame com dados de vendas
            figsize: Tamanho padrão das figuras
        """
        self.df = df
        self.figsize = figsize
        
    def plot_sales_trend(self, save_path: Optional[str] = None):
        """
        Plota tendência de vendas ao longo do tempo.
        
        Args:
            save_path: Caminho para salvar a imagem (opcional)
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Agrupa por mês
        monthly_sales = self.df.groupby(
            pd.Grouper(key='data_venda', freq='M')
        )['receita'].sum()
        
        ax.plot(monthly_sales.index, monthly_sales.values, 
                marker='o', linewidth=2, markersize=6)
        ax.set_title('Tendência de Vendas Mensais', fontsize=16, fontweight='bold')
        ax.set_xlabel('Período', fontsize=12)
        ax.set_ylabel('Receita Total (R$)', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Formata eixo Y
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x/1000:.0f}K'))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
        
    def plot_top_products(self, n: int = 10, save_path: Optional[str] = None):
        """
        Plota os produtos mais vendidos.
        
        Args:
            n: Número de produtos a exibir
            save_path: Caminho para salvar a imagem (opcional)
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        top_products = self.df.groupby('id_produto')['receita'].sum().sort_values(ascending=False).head(n)
        
        ax.barh(range(len(top_products)), top_products.values, color='steelblue')
        ax.set_yticks(range(len(top_products)))
        ax.set_yticklabels([f'Produto {pid}' for pid in top_products.index])
        ax.set_xlabel('Receita Total (R$)', fontsize=12)
        ax.set_title(f'Top {n} Produtos por Receita', fontsize=16, fontweight='bold')
        ax.invert_yaxis()
        
        # Adiciona valores nas barras
        for i, v in enumerate(top_products.values):
            ax.text(v, i, f' R$ {v/1000:.1f}K', va='center')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
        
    def plot_sales_by_region(self, save_path: Optional[str] = None):
        """
        Plota vendas por região.
        
        Args:
            save_path: Caminho para salvar a imagem (opcional)
        """
        fig, ax = plt.subplots(figsize=(10, 10))
        
        sales_by_region = self.df.groupby('regiao')['receita'].sum().sort_values(ascending=False)
        
        colors = sns.color_palette('husl', len(sales_by_region))
        wedges, texts, autotexts = ax.pie(
            sales_by_region.values,
            labels=sales_by_region.index,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )
        
        # Melhora a legibilidade
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(12)
            autotext.set_fontweight('bold')
        
        ax.set_title('Distribuição de Vendas por Região', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
        
    def plot_sales_heatmap(self, save_path: Optional[str] = None):
        """
        Plota heatmap de vendas por mês e dia da semana.
        
        Args:
            save_path: Caminho para salvar a imagem (opcional)
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Cria pivot table
        heatmap_data = self.df.pivot_table(
            values='receita',
            index='dia_semana',
            columns='mes',
            aggfunc='sum'
        )
        
        # Nomes dos dias da semana
        dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        heatmap_data.index = [dias[i] for i in heatmap_data.index]
        
        sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax, cbar_kws={'label': 'Receita (R$)'})
        ax.set_title('Heatmap de Vendas: Dia da Semana vs Mês', fontsize=16, fontweight='bold')
        ax.set_xlabel('Mês', fontsize=12)
        ax.set_ylabel('Dia da Semana', fontsize=12)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
        
    def plot_distribution(self, column: str, save_path: Optional[str] = None):
        """
        Plota distribuição de uma variável.
        
        Args:
            column: Nome da coluna a plotar
            save_path: Caminho para salvar a imagem (opcional)
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histograma
        ax1.hist(self.df[column], bins=30, color='steelblue', edgecolor='black', alpha=0.7)
        ax1.set_title(f'Distribuição de {column}', fontsize=14, fontweight='bold')
        ax1.set_xlabel(column, fontsize=12)
        ax1.set_ylabel('Frequência', fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # Box plot
        ax2.boxplot(self.df[column], vert=True)
        ax2.set_title(f'Box Plot de {column}', fontsize=14, fontweight='bold')
        ax2.set_ylabel(column, fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
        
    def plot_correlation_matrix(self, save_path: Optional[str] = None):
        """
        Plota matriz de correlação.
        
        Args:
            save_path: Caminho para salvar a imagem (opcional)
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Seleciona apenas colunas numéricas
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        corr_matrix = self.df[numeric_cols].corr()
        
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                    center=0, ax=ax, square=True, linewidths=1)
        ax.set_title('Matriz de Correlação', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
        
    def create_dashboard(self, save_path: Optional[str] = None):
        """
        Cria um dashboard com múltiplas visualizações.
        
        Args:
            save_path: Caminho para salvar a imagem (opcional)
        """
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # 1. Tendência de vendas
        ax1 = fig.add_subplot(gs[0, :])
        monthly_sales = self.df.groupby(pd.Grouper(key='data_venda', freq='M'))['receita'].sum()
        ax1.plot(monthly_sales.index, monthly_sales.values, marker='o', linewidth=2)
        ax1.set_title('Tendência de Vendas Mensais', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Receita (R$)')
        ax1.grid(True, alpha=0.3)
        
        # 2. Top produtos
        ax2 = fig.add_subplot(gs[1, 0])
        top_products = self.df.groupby('categoria')['receita'].sum().sort_values(ascending=False).head(5)
        ax2.bar(range(len(top_products)), top_products.values, color='steelblue')
        ax2.set_xticks(range(len(top_products)))
        ax2.set_xticklabels(top_products.index, rotation=45, ha='right')
        ax2.set_title('Top 5 Categorias', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Receita (R$)')
        
        # 3. Vendas por região
        ax3 = fig.add_subplot(gs[1, 1])
        sales_by_region = self.df.groupby('regiao')['receita'].sum()
        ax3.pie(sales_by_region.values, labels=sales_by_region.index, autopct='%1.1f%%')
        ax3.set_title('Vendas por Região', fontsize=14, fontweight='bold')
        
        # 4. Distribuição de receita
        ax4 = fig.add_subplot(gs[2, 0])
        ax4.hist(self.df['receita'], bins=30, color='coral', edgecolor='black', alpha=0.7)
        ax4.set_title('Distribuição de Receita', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Receita (R$)')
        ax4.set_ylabel('Frequência')
        
        # 5. Vendas por trimestre
        ax5 = fig.add_subplot(gs[2, 1])
        quarterly_sales = self.df.groupby('trimestre')['receita'].sum()
        ax5.bar(quarterly_sales.index, quarterly_sales.values, color='green', alpha=0.7)
        ax5.set_title('Vendas por Trimestre', fontsize=14, fontweight='bold')
        ax5.set_xlabel('Trimestre')
        ax5.set_ylabel('Receita (R$)')
        
        fig.suptitle('Dashboard de Análise de Vendas', fontsize=18, fontweight='bold', y=0.995)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()


if __name__ == "__main__":
    # Exemplo de uso
    import sys
    sys.path.append('..')
    from src.data_processing import DataProcessor
    
    processor = DataProcessor('../data/vendas.csv')
    df = processor.load_data()
    df = processor.clean_data()
    df = processor.create_features()
    
    visualizer = SalesVisualizer(df)
    
    print("📊 Gerando visualizações...")
    visualizer.plot_sales_trend()
    visualizer.plot_top_products()
    visualizer.plot_sales_by_region()
    visualizer.create_dashboard()
