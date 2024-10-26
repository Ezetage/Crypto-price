import os
import sys
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Se añade el directorio padre al sys.path para permitir la importación de los módulos necesarios
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tasks.run_extract import run_extract
from tasks.run_transform import run_transform
from tasks.run_load import run_load
from tasks.run_update import run_update

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
    description='DAG para la ejecución de tareas en forma secuencial, donde se extraerán los datos, se transformarán, se cargaran a la base de datos de Redshift (ETL) y se actualizarán las nuevas columnas creadas de date y time llamando a la función run_update',
    schedule="59 23 * * *", # Se programa la ejecución utilizando una expresión CRON, en este caso, el flujo se ejecutará todos los días a las 23:59 hs
    catchup=False,
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

        # Tarea para actualizar las columnas de fecha y hora
    update_task = PythonOperator(
        task_id='update_date_time',
        python_callable=run_update,
    )

# Definición del flujo de tareas
extract_task >> transform_task >> load_task >> update_task
