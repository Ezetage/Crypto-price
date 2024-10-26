import pandas as pd
import os
import sys

# Añadir el directorio padre a sys.path para importar los módulos necesarios
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.load.connection_db import create_redshift_engine

def run_update():
    """
    Crea y actualiza las columnas de fecha y hora en la tabla de Redshift.

    Raises:
        Exception: Si ocurre algún error durante la actualización.
    """

    try:
        engine, REDSHIFT_SCHEMA = create_redshift_engine()
        if engine is None:
            return

        with engine.connect() as connection:
            # Verificar si la columna date_column existe, en caso contrario, se crea
            result = connection.execute(f"""
                SELECT 1 
                FROM information_schema.columns 
                WHERE table_schema = '{REDSHIFT_SCHEMA}' 
                AND table_name = 'fact_table' 
                AND column_name = 'date_column'
            """).fetchone()
            
            if result is None:
                connection.execute(f"""
                    ALTER TABLE "{REDSHIFT_SCHEMA}"."fact_table"
                    ADD COLUMN date_column DATE;
                """)

            # Verificar si la columna time_column existe, en caso contrario, se crea
            result = connection.execute(f"""
                SELECT 1 
                FROM information_schema.columns 
                WHERE table_schema = '{REDSHIFT_SCHEMA}' 
                AND table_name = 'fact_table' 
                AND column_name = 'time_column'
            """).fetchone()
            
            if result is None:
                connection.execute(f"""
                    ALTER TABLE "{REDSHIFT_SCHEMA}"."fact_table"
                    ADD COLUMN time_column TIME;
                """)

            # Actualizar las columnas date_column y time_column
            connection.execute(f"""
                UPDATE "{REDSHIFT_SCHEMA}"."fact_table"
                SET date_column = (last_updated::timestamp)::date;
            """)
            connection.execute(f"""
                UPDATE "{REDSHIFT_SCHEMA}"."fact_table"
                SET time_column = (last_updated::timestamp)::time;
            """)

            print("Columnas de fecha y hora actualizadas exitosamente en la tabla 'fact_table'.")

    except Exception as e:
        print(f"Error al actualizar la tabla en Redshift: {str(e)}")
        raise
