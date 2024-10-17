import os
import sys
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tasks.run_extract import run_extract
from tasks.run_transform import run_transform
from tasks.run_load import run_load

# Se definen los argumentos
default_args = {
    'owner': 'airflow',
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
    'start_date': datetime(2024, 10, 1),
}

# Definición del DAG
with DAG(
    'dag_etl',
    default_args=default_args,
    description='DAG simplificado con tasks externos para extraer, transformar y cargar dos DataFrames',
    schedule="59 23 * * *",
    catchup=True,
) as dag:
    
    # Tarea para extraer los datos
    extract_task = PythonOperator(
        task_id='run_extract',
        python_callable=run_extract,
    )

    # Tarea para generar los df y convertirlos a .parquet
    transform_task = PythonOperator(
        task_id='run_transform',
        python_callable=run_transform,
    )

    # Tarea para cargar los df en redshift
    load_task = PythonOperator(
        task_id='run_load',
        python_callable=run_load,
    )

# Definición del flujo de tareas
extract_task >> transform_task >> load_task
