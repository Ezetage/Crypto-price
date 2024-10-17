import os
import sys
import logging
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from load.connection_db import create_redshift_engine
from load.load_tables_in_db import run_load_parquet_redshift

def run_load(**kwargs):
    try:
        # Crear el motor de conexión a Redshift
        engine, schema = create_redshift_engine()
        if engine is None:
            print("No se pudo crear el motor de Redshift.")
            return
        
        # Obtener los DataFrames desde XCom
        ti = kwargs['ti']
        transformed_df_dim = ti.xcom_pull(task_ids='run_transform', key='transformed_df_dim')
        transformed_df_fact = ti.xcom_pull(task_ids='run_transform', key='transformed_df_fact')
        
        # Loguear la información de los DataFrames
        logging.basicConfig(level=logging.INFO)
        
        # Captura el horario de carga
        load_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logging.info(f"Datos cargados en Redshift en el horario: {load_time}")
        
        # Log de las tablas que se están cargando
        logging.info("Tabla Dimensiones (transformed_df_dim) a cargar:\n%s", transformed_df_dim.head())
        logging.info("Tabla Hechos (transformed_df_fact) a cargar:\n%s", transformed_df_fact.head())
        
        # Ejecutar el proceso de carga
        run_load_parquet_redshift()

        print("Proceso de carga completado con éxito.")

    except Exception as e:
        print(f"Error en la tarea de carga: {e}")
        raise
