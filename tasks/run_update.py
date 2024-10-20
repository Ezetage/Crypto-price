import pandas as pd
import os
import sys

# Se añade el directorio padre al sys.path para permitir la importación de los módulos necesarios
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from load.connection_db import create_redshift_engine

def run_update():
    """
    Actualiza las columnas de fecha y hora en la tabla de Redshift.

    Raises:
        Exception: Si ocurre algún error durante la actualización.
    """

    try:
        engine, schema = create_redshift_engine()
        if engine is None:
            return
        
        with engine.connect() as connection:
            connection.execute("""
                UPDATE "2024_ezequiel_guinazu_schema"."fact_table"
                SET date_column = CAST(SUBSTRING(last_updated FROM 1 FOR 10) AS date);
            """)
            connection.execute("""
                UPDATE "2024_ezequiel_guinazu_schema"."fact_table"
                SET time_column = CAST(SUBSTRING(last_updated FROM 12 FOR 8) AS time);
            """)
        print("Columnas de fecha y hora actualizadas exitosamente en la tabla 'fact_table'.")

    except Exception as e:
        print(f"Error al actualizar la tabla en Redshift: {str(e)}")
        raise
