import os
import sys
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
    
    # Se convierten los df a .parquet
    transformed_df_dim.to_parquet('dimention_data.parquet')
    transformed_df_fact.to_parquet('fact_data.parquet')