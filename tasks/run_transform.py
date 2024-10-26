import os
import sys

# Se añade el directorio padre al sys.path para permitir la importación de los módulos necesarios
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.transform.conversion_to_parquet import calendar_table, generar_dataframe_dim, generar_dataframe_facts
from etl.transform.create_table_calendar import create_calendar_table
from etl.load.connection_db import create_redshift_engine

def run_transform(**kwargs):
    """
    Función que transforma los datos extraídos de la API en DataFrames y los guarda en formato .parquet y .sql.

    Args:
        **kwargs: Argumentos adicionales, incluyendo el contexto de ejecución de Airflow.

    Raises:
        Exception: Si hay un problema al obtener los datos de XCom
    """

    # Se obtiene el motor de conexión a Redshift
    engine, REDSHIFT_SCHEMA = create_redshift_engine()
    
    # Se crea la tabla calendario si no existe
    create_calendar_table(engine, REDSHIFT_SCHEMA)

    # Se obtienen los datos extraídos de la API
    extracted_data = kwargs['ti'].xcom_pull(task_ids='run_extract', key='extracted_data')
    
    # Se generan los df de dimensiones y de hechos
    transformed_df_dim = generar_dataframe_dim()
    transformed_df_fact = generar_dataframe_facts()
    transformed_calendar_date = calendar_table()
    
    # Se guardan los DataFrames en archivos Parquet
    dim_path = 'dimension_table.parquet'
    fact_path = 'fact_table.parquet'
    calendar_path = 'calendar_table.parquet'
    
    transformed_df_dim.to_parquet(dim_path)
    transformed_df_fact.to_parquet(fact_path)
    transformed_calendar_date.to_parquet(calendar_path)
    
    # Se guardan las rutas de los archivos en XCom
    kwargs['ti'].xcom_push(key='dim_path', value=dim_path)
    kwargs['ti'].xcom_push(key='fact_path', value=fact_path)
    kwargs['ti'].xcom_push(key='calendar_path', value=calendar_path)
