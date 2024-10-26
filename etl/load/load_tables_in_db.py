import pandas as pd
import os
import sys

# Se añade el directorio padre al sys.path para permitir la importación de los módulos necesarios
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from load.connection_db import create_redshift_engine

def load_parquet_redshift(parquet_file: str, table_name: str, redshift_engine, schema: str, if_exists: str):
    """
    Carga un archivo .parquet en una tabla de Redshift.

    Args:
        parquet_file (str): Ruta del archivo .parquet a cargar.
        table_name (str): Nombre de la tabla en Redshift.
        redshift_engine: Motor de conexión a Redshift.
        schema (str): Esquema en el que se insertarán los datos.
        if_exists (str): Comportamiento si la tabla ya existe ('replace', 'append', etc.).

    Raises:
        Exception: Si ocurre algún error durante la carga en Redshift.
    """

    try:
        with redshift_engine.connect() as connection:
            parquet_df = pd.read_parquet(parquet_file)
            parquet_df.to_sql(table_name, con=connection, schema=schema, if_exists=if_exists, index=False)
        print(f"Tabla '{table_name}' cargada exitosamente en Redshift.")
    
    except Exception as e:
        print(f"Error al cargar {parquet_file} en Redshift: {str(e)}")
        raise

def table_is_empty(engine, table_name: str, schema: str) -> bool:
    """
    Verifica si una tabla está vacía en Redshift.

    Args:
        engine: Motor de conexión a Redshift.
        table_name (str): Nombre de la tabla a verificar.
        schema (str): Esquema donde buscar la tabla.

    Returns:
        bool: Verdadero si la tabla está vacía, Falso en caso contrario.
    """

    with engine.connect() as connection:
        result = connection.execute(f'SELECT COUNT(*) FROM "{schema}"."{table_name}"')
        count = result.scalar()
        return count == 0  # Devuelve True si la tabla está vacía

# Se ejecuta el flujo de carga de las tablas a redshift
def run_load_parquet_redshift():
    """
    Ejecuta la carga de archivos .parquet a las tablas de Redshift.

    Se conecta a Redshift usando el motor y carga los archivos .parquet en las
    tablas correspondientes ('dimention_table', 'fact_table' y 'calendar_table' si está vacía).
    
    Raises:
        Exception: Si ocurre algún error en el proceso de carga de las tablas.
    """

    try:
        engine, REDSHIFT_SCHEMA = create_redshift_engine()
        if engine is None:
            return
        
        # Se verifica si la tabla calendario tiene datos, si tiene datos, no se cargará nada, si no tiene, se cargarán los datos del calendar_table.parquet en la misma
        if table_is_empty(engine, 'calendar_table', REDSHIFT_SCHEMA):
            load_parquet_redshift('calendar_table.parquet', 'calendar_table', engine, REDSHIFT_SCHEMA, if_exists='append')
            print("Datos cargados en la tabla calendario.")
        else:
            print("La tabla calendario ya tiene datos. No se realizará ninguna carga.")

        load_parquet_redshift('dimension_table.parquet', 'dimension_table', engine, REDSHIFT_SCHEMA, if_exists='replace')
        load_parquet_redshift('fact_table.parquet', 'fact_table', engine, REDSHIFT_SCHEMA, if_exists='append')

    except Exception as e:
        print(f"Error en el proceso principal: {e}")
        raise

# Se evalúa __main__ para ejecución directa e impresión por terminal
if __name__ == "__main__":
    run_load_parquet_redshift()