"""
Pipeline ETL Principal

Autor: Anderson de Lima
Data: Janeiro 2026
"""

import logging
from datetime import datetime
from pathlib import Path
import yaml
from typing import List, Dict

from extract.csv_extractor import CSVExtractor
from extract.api_extractor import APIExtractor
from transform.data_cleaner import DataCleaner
from transform.data_validator import DataValidator
from load.db_loader import DatabaseLoader


# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/pipeline_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class ETLPipeline:
    """Pipeline ETL completo para processamento de dados de vendas."""
    
    def __init__(self, config_path: str):
        """
        Inicializa o pipeline ETL.
        
        Args:
            config_path: Caminho para arquivo de configuração
        """
        self.config = self._load_config(config_path)
        self.execution_log = []
        
        logger.info("Pipeline ETL inicializado")
        
    def _load_config(self, config_path: str) -> Dict:
        """Carrega configurações do arquivo YAML."""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    
    def extract(self, sources: List[str]) -> Dict:
        """
        Fase de extração de dados.
        
        Args:
            sources: Lista de fontes de dados ('csv', 'api', 'db')
            
        Returns:
            Dicionário com dados extraídos
        """
        logger.info("=== INICIANDO FASE DE EXTRAÇÃO ===")
        extracted_data = {}
        
        try:
            if 'csv' in sources:
                logger.info("Extraindo dados de CSV...")
                csv_extractor = CSVExtractor(self.config.get('csv_path'))
                extracted_data['csv'] = csv_extractor.extract()
                logger.info(f"✅ CSV extraído: {len(extracted_data['csv'])} registros")
            
            if 'api' in sources:
                logger.info("Extraindo dados de API...")
                api_extractor = APIExtractor(self.config.get('api_url'))
                extracted_data['api'] = api_extractor.extract()
                logger.info(f"✅ API extraída: {len(extracted_data['api'])} registros")
            
            self.execution_log.append({
                'fase': 'extract',
                'status': 'success',
                'timestamp': datetime.now(),
                'records': sum(len(df) for df in extracted_data.values())
            })
            
            return extracted_data
            
        except Exception as e:
            logger.error(f"❌ Erro na extração: {str(e)}")
            self.execution_log.append({
                'fase': 'extract',
                'status': 'error',
                'timestamp': datetime.now(),
                'error': str(e)
            })
            raise
    
    def transform(self, data: Dict, rules: List[str]) -> Dict:
        """
        Fase de transformação de dados.
        
        Args:
            data: Dados extraídos
            rules: Regras de transformação ('clean', 'validate', 'enrich')
            
        Returns:
            Dados transformados
        """
        logger.info("=== INICIANDO FASE DE TRANSFORMAÇÃO ===")
        transformed_data = {}
        
        try:
            for source, df in data.items():
                logger.info(f"Transformando dados de {source}...")
                
                if 'clean' in rules:
                    logger.info("Aplicando limpeza de dados...")
                    cleaner = DataCleaner()
                    df = cleaner.clean(df)
                    logger.info(f"✅ Dados limpos: {len(df)} registros")
                
                if 'validate' in rules:
                    logger.info("Validando dados...")
                    validator = DataValidator()
                    df, validation_report = validator.validate(df)
                    logger.info(f"✅ Validação concluída: {validation_report['valid_records']} registros válidos")
                
                transformed_data[source] = df
            
            self.execution_log.append({
                'fase': 'transform',
                'status': 'success',
                'timestamp': datetime.now(),
                'records': sum(len(df) for df in transformed_data.values())
            })
            
            return transformed_data
            
        except Exception as e:
            logger.error(f"❌ Erro na transformação: {str(e)}")
            self.execution_log.append({
                'fase': 'transform',
                'status': 'error',
                'timestamp': datetime.now(),
                'error': str(e)
            })
            raise
    
    def load(self, data: Dict, mode: str = 'incremental') -> None:
        """
        Fase de carga de dados.
        
        Args:
            data: Dados transformados
            mode: Modo de carga ('incremental', 'full')
        """
        logger.info("=== INICIANDO FASE DE CARGA ===")
        
        try:
            loader = DatabaseLoader(self.config['database'])
            
            total_records = 0
            for source, df in data.items():
                logger.info(f"Carregando dados de {source}...")
                records_loaded = loader.load(df, mode=mode)
                total_records += records_loaded
                logger.info(f"✅ {records_loaded} registros carregados de {source}")
            
            logger.info(f"✅ CARGA CONCLUÍDA: {total_records} registros totais")
            
            self.execution_log.append({
                'fase': 'load',
                'status': 'success',
                'timestamp': datetime.now(),
                'records': total_records
            })
            
        except Exception as e:
            logger.error(f"❌ Erro na carga: {str(e)}")
            self.execution_log.append({
                'fase': 'load',
                'status': 'error',
                'timestamp': datetime.now(),
                'error': str(e)
            })
            raise
    
    def run(self, extract_sources: List[str], transform_rules: List[str], load_mode: str = 'incremental') -> None:
        """
        Executa o pipeline ETL completo.
        
        Args:
            extract_sources: Fontes de dados para extração
            transform_rules: Regras de transformação
            load_mode: Modo de carga
        """
        start_time = datetime.now()
        logger.info("="*50)
        logger.info("INICIANDO PIPELINE ETL")
        logger.info("="*50)
        
        try:
            # Extract
            extracted_data = self.extract(extract_sources)
            
            # Transform
            transformed_data = self.transform(extracted_data, transform_rules)
            
            # Load
            self.load(transformed_data, load_mode)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info("="*50)
            logger.info(f"✅ PIPELINE CONCLUÍDO COM SUCESSO")
            logger.info(f"⏱️  Tempo de execução: {duration:.2f} segundos")
            logger.info("="*50)
            
        except Exception as e:
            logger.error("="*50)
            logger.error(f"❌ PIPELINE FALHOU: {str(e)}")
            logger.error("="*50)
            raise
    
    def get_execution_log(self) -> List[Dict]:
        """Retorna o log de execução do pipeline."""
        return self.execution_log


if __name__ == "__main__":
    # Exemplo de uso
    pipeline = ETLPipeline(config_path='config/database.yaml')
    
    pipeline.run(
        extract_sources=['csv'],
        transform_rules=['clean', 'validate'],
        load_mode='incremental'
    )
    
    # Exibe log de execução
    print("\n📋 Log de Execução:")
    for log in pipeline.get_execution_log():
        print(log)
