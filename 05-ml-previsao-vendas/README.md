# 🤖 Previsão de Vendas com Machine Learning

## 🎯 Objetivo

Desenvolver um modelo de Machine Learning para prever vendas futuras utilizando dados históricos, aplicando técnicas de séries temporais e algoritmos de regressão.

## 🚀 Tecnologias Utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)

## ✨ Funcionalidades

### 📊 Análise Exploratória
- Análise de tendências e sazonalidade
- Detecção de outliers
- Análise de correlação
- Decomposição de séries temporais

### 🤖 Modelos Implementados
- Linear Regression
- Random Forest Regressor
- XGBoost
- Prophet (Facebook)
- ARIMA/SARIMA

### 📈 Avaliação de Modelos
- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)
- MAPE (Mean Absolute Percentage Error)
- R² Score

## 📁 Estrutura do Projeto

```
ml-previsao-vendas/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   ├── 01_exploratory_analysis.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_model_evaluation.ipynb
├── src/
│   ├── data_preprocessing.py
│   ├── feature_engineering.py
│   ├── model_training.py
│   └── model_evaluation.py
├── models/
│   └── (modelos salvos)
├── requirements.txt
└── README.md
```

## 🔍 Metodologia

### 1. Preparação dos Dados
```python
# Feature Engineering
- Variáveis temporais (dia, mês, ano, dia da semana)
- Lags (vendas dos últimos N dias)
- Rolling statistics (médias móveis)
- Variáveis sazonais
- Encoding de variáveis categóricas
```

### 2. Divisão dos Dados
```python
# Time Series Split
- Treino: 70% dos dados
- Validação: 15% dos dados
- Teste: 15% dos dados
```

### 3. Treinamento de Modelos
```python
# Modelos treinados
- Baseline (média móvel)
- Linear Regression
- Random Forest
- XGBoost
- Prophet
```

## 📊 Resultados

### Comparação de Modelos

| Modelo | RMSE | MAE | MAPE | R² |
|--------|------|-----|------|-----|
| Baseline | 1250.50 | 980.30 | 15.2% | 0.65 |
| Linear Regression | 1100.20 | 850.40 | 12.8% | 0.72 |
| Random Forest | 950.80 | 720.60 | 10.5% | 0.81 |
| **XGBoost** | **880.40** | **680.20** | **9.2%** | **0.85** |
| Prophet | 920.30 | 710.50 | 10.1% | 0.83 |

**Melhor Modelo**: XGBoost com R² de 0.85

## 🚀 Como Executar

### Pré-requisitos
```bash
Python 3.8+
```

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/198517/ml-previsao-vendas.git
cd ml-previsao-vendas
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute os notebooks na ordem:
```bash
jupyter notebook notebooks/
```

4. Ou execute o script de treinamento:
```bash
python src/model_training.py
```

## 💻 Exemplo de Uso

```python
from src.model_training import SalesForecaster

# Inicializa o forecaster
forecaster = SalesForecaster(model_type='xgboost')

# Treina o modelo
forecaster.train(X_train, y_train)

# Faz previsões
predictions = forecaster.predict(X_test)

# Avalia o modelo
metrics = forecaster.evaluate(y_test, predictions)
print(f"RMSE: {metrics['rmse']:.2f}")
print(f"R²: {metrics['r2']:.2f}")

# Salva o modelo
forecaster.save_model('models/xgboost_model.pkl')
```

## 📦 Dependências

```
pandas==2.0.0
numpy==1.24.0
scikit-learn==1.3.0
xgboost==2.0.0
prophet==1.1.0
matplotlib==3.7.0
seaborn==0.12.0
jupyter==1.0.0
```

## 📈 Features Utilizadas

### Temporais
- Ano, mês, dia
- Dia da semana
- Trimestre
- Semana do ano
- É fim de semana?
- É feriado?

### Lags
- Vendas dos últimos 7 dias
- Vendas dos últimos 30 dias
- Vendas do mesmo dia da semana anterior

### Rolling Statistics
- Média móvel (7, 14, 30 dias)
- Desvio padrão móvel
- Mínimo e máximo móvel

### Sazonais
- Indicadores de sazonalidade mensal
- Indicadores de sazonalidade trimestral

## 🎓 Aprendizados

Este projeto demonstra:
- ✅ Feature engineering para séries temporais
- ✅ Treinamento de múltiplos modelos de ML
- ✅ Avaliação e comparação de modelos
- ✅ Otimização de hiperparâmetros
- ✅ Validação cruzada para séries temporais
- ✅ Interpretação de resultados
- ✅ Deploy de modelos

## 📊 Visualizações

O projeto inclui:
- Gráficos de tendência histórica
- Decomposição de séries temporais
- Comparação de previsões vs valores reais
- Importância de features
- Análise de resíduos

## 📝 Próximos Passos

- [ ] Implementar ensemble de modelos
- [ ] Adicionar mais features externas (clima, eventos)
- [ ] Criar API para servir previsões
- [ ] Implementar retreinamento automático
- [ ] Adicionar monitoramento de drift

## 👤 Autor

**Anderson de Lima**
- LinkedIn: [anderson-de-lima-analista-de-dados](https://www.linkedin.com/in/anderson-de-lima-analista-de-dados/)
- GitHub: [@198517](https://github.com/198517)

## 📄 Licença

Este projeto está sob a licença MIT.

---

⭐ Se este projeto foi útil para você, considere dar uma estrela!
