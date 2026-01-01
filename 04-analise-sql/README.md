# 📊 Análise de Dados com SQL

## 🎯 Objetivo

Demonstrar expertise em SQL através de queries complexas para análise de negócio, incluindo CTEs, window functions, subqueries e otimização de consultas.

## 🚀 Tecnologias Utilizadas

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 📁 Estrutura do Projeto

```
analise-sql/
├── schema/
│   └── create_tables.sql
├── queries/
│   ├── 01_analise_vendas.sql
│   ├── 02_analise_clientes.sql
│   ├── 03_analise_produtos.sql
│   ├── 04_window_functions.sql
│   └── 05_queries_complexas.sql
├── data/
│   └── sample_data.sql
├── notebooks/
│   └── sql_analysis.ipynb
└── README.md
```

## 📊 Análises Implementadas

### 1. Análise de Vendas
- Vendas totais por período
- Crescimento mês a mês (MoM)
- Análise de sazonalidade
- Ranking de produtos

### 2. Análise de Clientes
- Segmentação RFM
- Análise de coorte
- Lifetime Value (LTV)
- Taxa de retenção

### 3. Análise de Produtos
- Produtos mais vendidos
- Análise de margem
- Cross-selling
- Análise ABC

### 4. Window Functions
- Running totals
- Moving averages
- Ranking e percentis
- Lead/Lag analysis

## 🔍 Exemplos de Queries

### Análise de Crescimento MoM
```sql
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', data_venda) AS mes,
        SUM(valor_total) AS receita_total
    FROM vendas
    GROUP BY 1
)
SELECT 
    mes,
    receita_total,
    LAG(receita_total) OVER (ORDER BY mes) AS receita_mes_anterior,
    ROUND(
        ((receita_total - LAG(receita_total) OVER (ORDER BY mes)) / 
         LAG(receita_total) OVER (ORDER BY mes) * 100), 2
    ) AS crescimento_percentual
FROM monthly_sales
ORDER BY mes;
```

### Análise RFM
```sql
WITH rfm_calc AS (
    SELECT 
        id_cliente,
        CURRENT_DATE - MAX(data_venda) AS recency,
        COUNT(DISTINCT id_venda) AS frequency,
        SUM(valor_total) AS monetary
    FROM vendas
    GROUP BY id_cliente
),
rfm_scores AS (
    SELECT 
        id_cliente,
        recency,
        frequency,
        monetary,
        NTILE(5) OVER (ORDER BY recency DESC) AS r_score,
        NTILE(5) OVER (ORDER BY frequency) AS f_score,
        NTILE(5) OVER (ORDER BY monetary) AS m_score
    FROM rfm_calc
)
SELECT 
    id_cliente,
    r_score,
    f_score,
    m_score,
    r_score + f_score + m_score AS rfm_total,
    CASE 
        WHEN r_score >= 4 AND f_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal Customers'
        WHEN r_score >= 4 AND f_score <= 2 THEN 'Promising'
        WHEN r_score <= 2 AND f_score >= 4 THEN 'At Risk'
        ELSE 'Others'
    END AS segmento
FROM rfm_scores
ORDER BY rfm_total DESC;
```

### Top Produtos com Participação
```sql
WITH produto_vendas AS (
    SELECT 
        p.nome_produto,
        p.categoria,
        SUM(v.quantidade) AS total_vendido,
        SUM(v.valor_total) AS receita_total
    FROM vendas v
    JOIN produtos p ON v.id_produto = p.id_produto
    GROUP BY p.nome_produto, p.categoria
),
total_geral AS (
    SELECT SUM(receita_total) AS receita_total_geral
    FROM produto_vendas
)
SELECT 
    pv.nome_produto,
    pv.categoria,
    pv.total_vendido,
    pv.receita_total,
    ROUND((pv.receita_total / tg.receita_total_geral * 100), 2) AS participacao_percentual,
    SUM(ROUND((pv.receita_total / tg.receita_total_geral * 100), 2)) 
        OVER (ORDER BY pv.receita_total DESC) AS participacao_acumulada
FROM produto_vendas pv
CROSS JOIN total_geral tg
ORDER BY pv.receita_total DESC
LIMIT 20;
```

## 🎓 Conceitos Demonstrados

- ✅ Common Table Expressions (CTEs)
- ✅ Window Functions (ROW_NUMBER, RANK, NTILE, LAG, LEAD)
- ✅ Subqueries correlacionadas
- ✅ JOINs complexos
- ✅ Agregações avançadas
- ✅ Funções de data e tempo
- ✅ CASE statements
- ✅ Otimização de queries

## 🚀 Como Executar

### Pré-requisitos
```bash
PostgreSQL 12+
```

### Setup

1. Clone o repositório:
```bash
git clone https://github.com/198517/analise-sql.git
cd analise-sql
```

2. Crie o banco de dados:
```bash
psql -U postgres -c "CREATE DATABASE vendas_db;"
```

3. Execute o schema:
```bash
psql -U postgres -d vendas_db -f schema/create_tables.sql
```

4. Carregue dados de exemplo:
```bash
psql -U postgres -d vendas_db -f data/sample_data.sql
```

5. Execute as queries:
```bash
psql -U postgres -d vendas_db -f queries/01_analise_vendas.sql
```

## 📊 Schema do Banco de Dados

```sql
-- Tabela de Vendas
CREATE TABLE vendas (
    id_venda SERIAL PRIMARY KEY,
    data_venda DATE NOT NULL,
    id_cliente INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,
    valor_total DECIMAL(10,2) NOT NULL
);

-- Tabela de Clientes
CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    cidade VARCHAR(50),
    estado VARCHAR(2),
    data_cadastro DATE NOT NULL
);

-- Tabela de Produtos
CREATE TABLE produtos (
    id_produto SERIAL PRIMARY KEY,
    nome_produto VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    preco DECIMAL(10,2) NOT NULL
);
```

## 👤 Autor

**Anderson de Lima**
- LinkedIn: [anderson-de-lima-analista-de-dados](https://www.linkedin.com/in/anderson-de-lima-analista-de-dados/)
- GitHub: [@198517](https://github.com/198517)

## 📄 Licença

Este projeto está sob a licença MIT.

---

⭐ Se este projeto foi útil para você, considere dar uma estrela!
