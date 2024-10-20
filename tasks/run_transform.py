import os
import sys

# Se añade el directorio padre al sys.path para permitir la importación de los módulos necesarios
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transform.convertion_parquet import generar_dataframe_dim, generar_dataframe_facts, calendar_table
from transform.create_table_calendar import create_calendar_table
from load.connection_db import create_redshift_engine

def run_transform(**kwargs):
    """
    Función que transforma los datos extraídos de la API en DataFrames y los guarda en formato .parquet.

    Args:
        **kwargs: Argumentos adicionales, incluyendo el contexto de ejecución de Airflow.

    Raises:
        Exception: Si hay un problema al obtener los datos de XCom o al generar los DataFrames.
    """

    # Se obtiene el motor de conexión a Redshift
    engine, schema = create_redshift_engine()
    
    # Se crea la tabla calendario si no existe
    create_calendar_table(engine, schema)

    # Se obtienen los datos extraídos de la API
    extracted_data = kwargs['ti'].xcom_pull(task_ids='run_extract', key='extracted_data')
    
    # Se generan los df de dimensiones y de hechos
    transformed_df_dim = generar_dataframe_dim()
    transformed_df_fact = generar_dataframe_facts()
    transformed_calendar_date = calendar_table()
    
    # Se guardan ambos df en XCom
    kwargs['ti'].xcom_push(key='transformed_df_dim', value=transformed_df_dim)
    kwargs['ti'].xcom_push(key='transformed_df_fact', value=transformed_df_fact)
    kwargs['ti'].xcom_push(key='transformed_calendar_date', value=transformed_calendar_date)
    
    # Se convierten los df a .parquet
    transformed_df_dim.to_parquet('dimention_data.parquet')
    transformed_df_fact.to_parquet('fact_data.parquet')
    transformed_calendar_date.to_parquet('calendar_table.parquet')