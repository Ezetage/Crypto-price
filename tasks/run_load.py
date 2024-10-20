import os
import sys

# Se añade el directorio padre al sys.path para permitir la importación de los módulos necesarios
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from load.connection_db import create_redshift_engine
from load.load_tables_in_db import run_load_parquet_redshift

def run_load(**kwargs):
    """
    Función que maneja la carga de DataFrames en Amazon Redshift.

    Args:
        **kwargs: Argumentos adicionales, incluyendo el contexto de ejecución de Airflow.

    Raises:
        Exception: Si ocurre un error en el proceso de carga o conexión a la base de datos.
    """
        
    try:
        # Se crea el motor de conexión a Redshift
        engine, schema = create_redshift_engine()
        if engine is None:
            print("No se pudo crear el motor de Redshift.")
            return
        
        # Se obtienen los DataFrames desde XCom
        ti = kwargs['ti']
        transformed_df_dim = ti.xcom_pull(task_ids='run_transform', key='transformed_df_dim')
        transformed_df_fact = ti.xcom_pull(task_ids='run_transform', key='transformed_df_fact')
        transformed_calendar_date = ti.xcom_pull(task_ids='run_transform', key='transformed_calendar_date')

        # Se ejecuta el proceso de carga
        run_load_parquet_redshift()

        print("Proceso de carga completado con éxito.")

    except Exception as e:
        print(f"Error en la tarea de carga: {e}")
        raise
