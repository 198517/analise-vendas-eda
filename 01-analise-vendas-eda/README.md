# 📊 Análise Exploratória de Vendas

## 🎯 Objetivo

Realizar uma análise exploratória completa de dados de vendas de uma empresa fictícia, extraindo insights valiosos para tomada de decisão de negócio.

## 🚀 Tecnologias Utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=python&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)

## 📁 Estrutura do Projeto

```
analise-vendas-eda/
├── data/
│   ├── vendas.csv
│   └── README.md
├── notebooks/
│   └── analise_exploratoria.ipynb
├── src/
│   ├── data_processing.py
│   └── visualization.py
├── images/
│   └── (gráficos gerados)
├── requirements.txt
└── README.md
```

## 📊 Análises Realizadas

### 1. Análise Descritiva
- Estatísticas básicas dos dados
- Distribuição de vendas por período
- Análise de valores (média, mediana, desvio padrão)

### 2. Análise Temporal
- Tendências de vendas ao longo do tempo
- Sazonalidade
- Comparação ano a ano

### 3. Análise por Categoria
- Produtos mais vendidos
- Categorias com maior faturamento
- Análise de margem de lucro

### 4. Análise Geográfica
- Vendas por região
- Performance por estado/cidade
- Mapa de calor de vendas

### 5. Análise de Clientes
- Segmentação de clientes
- Análise RFM (Recency, Frequency, Monetary)
- Clientes mais valiosos

## 🔍 Principais Insights

1. **Sazonalidade**: Vendas aumentam 35% no último trimestre do ano
2. **Top Produtos**: 20% dos produtos representam 80% do faturamento (Princípio de Pareto)
3. **Regiões**: Sudeste concentra 45% das vendas totais
4. **Clientes**: 15% dos clientes geram 60% da receita
5. **Tendência**: Crescimento médio de 12% ao ano

## 📈 Visualizações

O projeto inclui visualizações profissionais:
- Gráficos de linha para tendências temporais
- Gráficos de barras para comparações
- Heatmaps para correlações
- Box plots para análise de distribuição
- Gráficos de pizza para proporções

## 🚀 Como Executar

### Pré-requisitos
```bash
Python 3.8+
```

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/198517/analise-vendas-eda.git
cd analise-vendas-eda
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o Jupyter Notebook:
```bash
jupyter notebook notebooks/analise_exploratoria.ipynb
```

## 📦 Dependências

```
pandas==2.0.0
numpy==1.24.0
matplotlib==3.7.0
seaborn==0.12.0
jupyter==1.0.0
```

## 📊 Dataset

O dataset contém informações de vendas com as seguintes colunas:
- `data_venda`: Data da transação
- `id_produto`: Identificador do produto
- `categoria`: Categoria do produto
- `quantidade`: Quantidade vendida
- `preco_unitario`: Preço por unidade
- `valor_total`: Valor total da venda
- `regiao`: Região da venda
- `id_cliente`: Identificador do cliente

## 🎓 Aprendizados

Este projeto demonstra:
- ✅ Limpeza e preparação de dados
- ✅ Análise exploratória de dados (EDA)
- ✅ Visualização de dados
- ✅ Storytelling com dados
- ✅ Extração de insights de negócio
- ✅ Boas práticas de documentação

## 📝 Próximos Passos

- [ ] Adicionar análise de correlação avançada
- [ ] Implementar análise de coorte
- [ ] Criar dashboard interativo
- [ ] Adicionar previsão de vendas

## 👤 Autor

**Anderson de Lima**
- LinkedIn: [anderson-de-lima-analista-de-dados](https://www.linkedin.com/in/anderson-de-lima-analista-de-dados/)
- GitHub: [@198517](https://github.com/198517)

## 📄 Licença

Este projeto está sob a licença MIT.

---

⭐ Se este projeto foi útil para você, considere dar uma estrela!
