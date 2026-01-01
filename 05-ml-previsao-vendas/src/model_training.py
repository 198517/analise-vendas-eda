"""
Módulo para treinamento de modelos de previsão de vendas.

Autor: Anderson de Lima
Data: Janeiro 2026
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
from typing import Tuple, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SalesForecaster:
    """Classe para treinar e avaliar modelos de previsão de vendas."""
    
    def __init__(self, model_type: str = 'xgboost'):
        """
        Inicializa o forecaster.
        
        Args:
            model_type: Tipo de modelo ('linear', 'random_forest', 'xgboost')
        """
        self.model_type = model_type
        self.model = self._initialize_model()
        self.is_trained = False
        
    def _initialize_model(self):
        """Inicializa o modelo baseado no tipo especificado."""
        models = {
            'linear': LinearRegression(),
            'random_forest': RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            ),
            'xgboost': XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42,
                n_jobs=-1
            )
        }
        
        if self.model_type not in models:
            raise ValueError(f"Modelo {self.model_type} não suportado")
        
        return models[self.model_type]
    
    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cria features para o modelo.
        
        Args:
            df: DataFrame com coluna 'data_venda' e 'receita'
            
        Returns:
            DataFrame com features criadas
        """
        df = df.copy()
        df['data_venda'] = pd.to_datetime(df['data_venda'])
        df = df.sort_values('data_venda')
        
        # Features temporais
        df['ano'] = df['data_venda'].dt.year
        df['mes'] = df['data_venda'].dt.month
        df['dia'] = df['data_venda'].dt.day
        df['dia_semana'] = df['data_venda'].dt.dayofweek
        df['trimestre'] = df['data_venda'].dt.quarter
        df['semana_ano'] = df['data_venda'].dt.isocalendar().week
        df['is_weekend'] = (df['dia_semana'] >= 5).astype(int)
        
        # Lags
        for lag in [1, 7, 14, 30]:
            df[f'lag_{lag}'] = df['receita'].shift(lag)
        
        # Rolling statistics
        for window in [7, 14, 30]:
            df[f'rolling_mean_{window}'] = df['receita'].rolling(window=window).mean()
            df[f'rolling_std_{window}'] = df['receita'].rolling(window=window).std()
        
        # Remove NaN criados pelos lags e rolling
        df = df.dropna()
        
        logger.info(f"✅ Features criadas: {df.shape[1]} colunas")
        
        return df
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series) -> None:
        """
        Treina o modelo.
        
        Args:
            X_train: Features de treino
            y_train: Target de treino
        """
        logger.info(f"🚀 Treinando modelo {self.model_type}...")
        
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        logger.info("✅ Modelo treinado com sucesso")
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Faz previsões.
        
        Args:
            X: Features para previsão
            
        Returns:
            Array com previsões
        """
        if not self.is_trained:
            raise ValueError("Modelo não treinado. Execute train() primeiro.")
        
        predictions = self.model.predict(X)
        
        return predictions
    
    def evaluate(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """
        Avalia o modelo.
        
        Args:
            y_true: Valores reais
            y_pred: Valores preditos
            
        Returns:
            Dicionário com métricas
        """
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        
        metrics = {
            'rmse': rmse,
            'mae': mae,
            'r2': r2,
            'mape': mape
        }
        
        logger.info("📊 Métricas de Avaliação:")
        logger.info(f"   RMSE: {rmse:.2f}")
        logger.info(f"   MAE: {mae:.2f}")
        logger.info(f"   R²: {r2:.4f}")
        logger.info(f"   MAPE: {mape:.2f}%")
        
        return metrics
    
    def get_feature_importance(self, feature_names: list) -> pd.DataFrame:
        """
        Retorna a importância das features.
        
        Args:
            feature_names: Lista com nomes das features
            
        Returns:
            DataFrame com importância das features
        """
        if self.model_type == 'linear':
            importance = np.abs(self.model.coef_)
        else:
            importance = self.model.feature_importances_
        
        feature_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        return feature_importance
    
    def save_model(self, filepath: str) -> None:
        """
        Salva o modelo treinado.
        
        Args:
            filepath: Caminho para salvar o modelo
        """
        if not self.is_trained:
            raise ValueError("Modelo não treinado")
        
        joblib.dump(self.model, filepath)
        logger.info(f"✅ Modelo salvo em {filepath}")
    
    def load_model(self, filepath: str) -> None:
        """
        Carrega um modelo salvo.
        
        Args:
            filepath: Caminho do modelo salvo
        """
        self.model = joblib.load(filepath)
        self.is_trained = True
        logger.info(f"✅ Modelo carregado de {filepath}")


def time_series_split_evaluation(df: pd.DataFrame, model_type: str = 'xgboost', n_splits: int = 5) -> Dict:
    """
    Avalia modelo usando Time Series Split.
    
    Args:
        df: DataFrame com dados
        model_type: Tipo de modelo
        n_splits: Número de splits
        
    Returns:
        Dicionário com resultados
    """
    forecaster = SalesForecaster(model_type=model_type)
    df_features = forecaster.create_features(df)
    
    # Separa features e target
    feature_cols = [col for col in df_features.columns if col not in ['data_venda', 'receita']]
    X = df_features[feature_cols]
    y = df_features['receita']
    
    # Time Series Split
    tscv = TimeSeriesSplit(n_splits=n_splits)
    
    results = []
    
    for fold, (train_idx, test_idx) in enumerate(tscv.split(X), 1):
        logger.info(f"\n📊 Fold {fold}/{n_splits}")
        
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        
        # Treina
        forecaster = SalesForecaster(model_type=model_type)
        forecaster.train(X_train, y_train)
        
        # Prediz
        y_pred = forecaster.predict(X_test)
        
        # Avalia
        metrics = forecaster.evaluate(y_test, y_pred)
        metrics['fold'] = fold
        results.append(metrics)
    
    # Média das métricas
    results_df = pd.DataFrame(results)
    mean_metrics = results_df.mean()
    
    logger.info("\n📊 Métricas Médias (Cross-Validation):")
    logger.info(f"   RMSE: {mean_metrics['rmse']:.2f}")
    logger.info(f"   MAE: {mean_metrics['mae']:.2f}")
    logger.info(f"   R²: {mean_metrics['r2']:.4f}")
    logger.info(f"   MAPE: {mean_metrics['mape']:.2f}%")
    
    return {
        'results_by_fold': results_df,
        'mean_metrics': mean_metrics.to_dict()
    }


if __name__ == "__main__":
    # Exemplo de uso
    # Gera dados de exemplo
    dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
    np.random.seed(42)
    
    df = pd.DataFrame({
        'data_venda': dates,
        'receita': np.random.randint(1000, 5000, len(dates)) + \
                   np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 500
    })
    
    # Avalia modelo com Time Series Split
    results = time_series_split_evaluation(df, model_type='xgboost', n_splits=5)
