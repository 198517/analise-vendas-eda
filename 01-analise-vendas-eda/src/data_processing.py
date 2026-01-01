"""
Módulo para processamento e limpeza de dados de vendas.

Autor: Anderson de Lima
Data: Janeiro 2026
"""

import pandas as pd
import numpy as np
from typing import Tuple, List


class DataProcessor:
    """Classe para processar e limpar dados de vendas."""
    
    def __init__(self, filepath: str):
        """
        Inicializa o processador de dados.
        
        Args:
            filepath: Caminho para o arquivo CSV de vendas
        """
        self.filepath = filepath
        self.df = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Carrega os dados do arquivo CSV.
        
        Returns:
            DataFrame com os dados carregados
        """
        self.df = pd.read_csv(self.filepath)
        print(f"✅ Dados carregados: {self.df.shape[0]} linhas, {self.df.shape[1]} colunas")
        return self.df
    
    def clean_data(self) -> pd.DataFrame:
        """
        Realiza limpeza dos dados.
        
        Returns:
            DataFrame limpo
        """
        if self.df is None:
            raise ValueError("Dados não carregados. Execute load_data() primeiro.")
        
        # Remove duplicatas
        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates()
        removed_duplicates = initial_rows - len(self.df)
        
        # Remove valores nulos
        self.df = self.df.dropna()
        
        # Converte data para datetime
        self.df['data_venda'] = pd.to_datetime(self.df['data_venda'])
        
        # Remove valores negativos
        self.df = self.df[self.df['quantidade'] > 0]
        self.df = self.df[self.df['preco_unitario'] > 0]
        
        print(f"✅ Dados limpos: {removed_duplicates} duplicatas removidas")
        print(f"✅ Total de linhas após limpeza: {len(self.df)}")
        
        return self.df
    
    def create_features(self) -> pd.DataFrame:
        """
        Cria features adicionais para análise.
        
        Returns:
            DataFrame com novas features
        """
        # Extrai componentes de data
        self.df['ano'] = self.df['data_venda'].dt.year
        self.df['mes'] = self.df['data_venda'].dt.month
        self.df['trimestre'] = self.df['data_venda'].dt.quarter
        self.df['dia_semana'] = self.df['data_venda'].dt.dayofweek
        self.df['nome_mes'] = self.df['data_venda'].dt.month_name()
        
        # Calcula métricas
        self.df['receita'] = self.df['quantidade'] * self.df['preco_unitario']
        
        print("✅ Features criadas com sucesso")
        
        return self.df
    
    def get_summary_statistics(self) -> pd.DataFrame:
        """
        Retorna estatísticas descritivas dos dados.
        
        Returns:
            DataFrame com estatísticas
        """
        return self.df.describe()
    
    def get_sales_by_period(self, period: str = 'M') -> pd.DataFrame:
        """
        Agrupa vendas por período.
        
        Args:
            period: Período de agregação ('D', 'W', 'M', 'Q', 'Y')
            
        Returns:
            DataFrame com vendas agregadas
        """
        sales_by_period = self.df.groupby(
            pd.Grouper(key='data_venda', freq=period)
        ).agg({
            'receita': 'sum',
            'quantidade': 'sum',
            'id_cliente': 'nunique'
        }).reset_index()
        
        sales_by_period.columns = ['periodo', 'receita_total', 'quantidade_total', 'clientes_unicos']
        
        return sales_by_period
    
    def get_top_products(self, n: int = 10) -> pd.DataFrame:
        """
        Retorna os produtos mais vendidos.
        
        Args:
            n: Número de produtos a retornar
            
        Returns:
            DataFrame com top produtos
        """
        top_products = self.df.groupby('id_produto').agg({
            'receita': 'sum',
            'quantidade': 'sum'
        }).sort_values('receita', ascending=False).head(n)
        
        return top_products
    
    def get_sales_by_region(self) -> pd.DataFrame:
        """
        Retorna vendas por região.
        
        Returns:
            DataFrame com vendas por região
        """
        sales_by_region = self.df.groupby('regiao').agg({
            'receita': 'sum',
            'quantidade': 'sum',
            'id_cliente': 'nunique'
        }).sort_values('receita', ascending=False)
        
        sales_by_region.columns = ['receita_total', 'quantidade_total', 'clientes_unicos']
        
        return sales_by_region
    
    def calculate_rfm(self) -> pd.DataFrame:
        """
        Calcula análise RFM (Recency, Frequency, Monetary).
        
        Returns:
            DataFrame com scores RFM
        """
        # Data de referência (última data no dataset)
        reference_date = self.df['data_venda'].max()
        
        rfm = self.df.groupby('id_cliente').agg({
            'data_venda': lambda x: (reference_date - x.max()).days,  # Recency
            'id_produto': 'count',  # Frequency
            'receita': 'sum'  # Monetary
        }).reset_index()
        
        rfm.columns = ['id_cliente', 'recency', 'frequency', 'monetary']
        
        # Cria scores (1-5)
        rfm['r_score'] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
        rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
        rfm['m_score'] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])
        
        # Score RFM combinado
        rfm['rfm_score'] = rfm['r_score'].astype(str) + rfm['f_score'].astype(str) + rfm['m_score'].astype(str)
        
        return rfm


if __name__ == "__main__":
    # Exemplo de uso
    processor = DataProcessor('../data/vendas.csv')
    df = processor.load_data()
    df = processor.clean_data()
    df = processor.create_features()
    
    print("\n📊 Estatísticas Descritivas:")
    print(processor.get_summary_statistics())
    
    print("\n🏆 Top 10 Produtos:")
    print(processor.get_top_products(10))
    
    print("\n🌍 Vendas por Região:")
    print(processor.get_sales_by_region())
