# 🔄 Pipeline ETL com Python

## 🎯 Objetivo

Implementar um pipeline completo de ETL (Extract, Transform, Load) para processar dados de vendas de múltiplas fontes e carregar em um data warehouse.

## 🚀 Tecnologias Utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=python&logoColor=white)

## ✨ Funcionalidades

### 📥 Extract (Extração)
- Leitura de arquivos CSV, Excel e JSON
- Conexão com APIs REST
- Extração de bancos de dados SQL
- Validação de dados na origem

### 🔧 Transform (Transformação)
- Limpeza de dados (valores nulos, duplicatas)
- Padronização de formatos
- Enriquecimento de dados
- Cálculo de métricas agregadas
- Validação de qualidade de dados

### 📤 Load (Carga)
- Carga incremental em PostgreSQL
- Upsert (insert ou update)
- Logging de operações
- Tratamento de erros

## 📁 Estrutura do Projeto

```
pipeline-etl/
├── config/
│   └── database.yaml
├── src/
│   ├── extract/
│   │   ├── csv_extractor.py
│   │   ├── api_extractor.py
│   │   └── db_extractor.py
│   ├── transform/
│   │   ├── data_cleaner.py
│   │   ├── data_validator.py
│   │   └── data_enricher.py
│   ├── load/
│   │   └── db_loader.py
│   └── pipeline.py
├── logs/
├── data/
│   ├── raw/
│   ├── processed/
│   └── archive/
├── tests/
├── requirements.txt
└── README.md
```

## 🔄 Fluxo do Pipeline

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   EXTRACT   │ --> │  TRANSFORM   │ --> │    LOAD     │
│             │     │              │     │             │
│ • CSV       │     │ • Limpeza    │     │ • PostgreSQL│
│ • API       │     │ • Validação  │     │ • Upsert    │
│ • Database  │     │ • Agregação  │     │ • Logging   │
└─────────────┘     └──────────────┘     └─────────────┘
```

## 🚀 Como Executar

### Pré-requisitos
```bash
Python 3.8+
PostgreSQL 12+
```

### Configuração

1. Clone o repositório:
```bash
git clone https://github.com/198517/pipeline-etl.git
cd pipeline-etl
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o banco de dados em `config/database.yaml`:
```yaml
database:
  host: localhost
  port: 5432
  database: vendas_dw
  user: seu_usuario
  password: sua_senha
```

4. Execute o pipeline:
```bash
python src/pipeline.py
```

## 📊 Exemplo de Uso

```python
from src.pipeline import ETLPipeline

# Inicializa o pipeline
pipeline = ETLPipeline(config_path='config/database.yaml')

# Executa o pipeline completo
pipeline.run(
    extract_sources=['csv', 'api'],
    transform_rules=['clean', 'validate', 'enrich'],
    load_mode='incremental'
)

# Verifica logs
pipeline.get_execution_log()
```

## 📦 Dependências

```
pandas==2.0.0
sqlalchemy==2.0.0
psycopg2-binary==2.9.0
pyyaml==6.0
requests==2.31.0
python-dotenv==1.0.0
```

## 🎓 Aprendizados

Este projeto demonstra:
- ✅ Arquitetura de pipelines ETL
- ✅ Integração com múltiplas fontes de dados
- ✅ Transformação e limpeza de dados
- ✅ Carga em data warehouse
- ✅ Tratamento de erros e logging
- ✅ Boas práticas de engenharia de dados

## 🔍 Validações Implementadas

- Verificação de tipos de dados
- Validação de valores nulos
- Detecção de duplicatas
- Verificação de integridade referencial
- Validação de regras de negócio

## 📝 Próximos Passos

- [ ] Implementar processamento paralelo
- [ ] Adicionar orquestração com Apache Airflow
- [ ] Implementar data quality checks
- [ ] Adicionar monitoramento com Prometheus
- [ ] Criar testes unitários e de integração

## 👤 Autor

**Anderson de Lima**
- LinkedIn: [anderson-de-lima-analista-de-dados](https://www.linkedin.com/in/anderson-de-lima-analista-de-dados/)
- GitHub: [@198517](https://github.com/198517)

## 📄 Licença

Este projeto está sob a licença MIT.

---

⭐ Se este projeto foi útil para você, considere dar uma estrela!
