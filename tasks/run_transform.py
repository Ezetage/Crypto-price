import os
import sys
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from transform.convertion_parquet import generar_dataframe_dim, generar_dataframe_facts

def run_transform(**kwargs):
    # Se obtienen los datos extraídos de la API
    extracted_data = kwargs['ti'].xcom_pull(task_ids='run_extract', key='extracted_data')
    
    # Se generan los df de dimensiones y de hechos
    transformed_df_dim = generar_dataframe_dim()
    transformed_df_fact = generar_dataframe_facts()
    
    # Se guardan ambos df en XCom
    kwargs['ti'].xcom_push(key='transformed_df_dim', value=transformed_df_dim)
    kwargs['ti'].xcom_push(key='transformed_df_fact', value=transformed_df_fact)
    
    # Configura el logger
    logging.basicConfig(level=logging.INFO)
    
    # Log de las tablas transformadas
    logging.info("Tabla Dimensiones (transformed_df_dim):\n%s", transformed_df_dim.head())
    logging.info("Tabla Hechos (transformed_df_fact):\n%s", transformed_df_fact.head())
    
    # Se convierten los df a .parquet
    transformed_df_dim.to_parquet('dimention_data.parquet')
    transformed_df_fact.to_parquet('fact_data.parquet')