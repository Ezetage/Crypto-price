import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from load.connection_db import create_redshift_engine

# Lectura y parametrización para carga de tablas .parquet en redshift
def load_parquet_redshift(parquet_file: str, table_name: str, redshift_engine, schema: str, if_exists: str):
    try:

        with redshift_engine.connect() as connection:
            parquet_df = pd.read_parquet(parquet_file)
            parquet_df.to_sql(table_name, con=connection, schema=schema, if_exists=if_exists, index=False)
        print(f"Tabla '{table_name}' cargada exitosamente en Redshift.")
    
    except Exception as e:
        print(f"Error al cargar {parquet_file} en Redshift: {str(e)}")
        raise
            
# Se corre el flujo de carga de las tablas a redshift
def run_load_parquet_redshift():
    try:
        engine, schema = create_redshift_engine()
        if engine is None:
            return
        
        load_parquet_redshift('dimention_data.parquet', 'dimention_table', engine, schema, if_exists='replace')
        load_parquet_redshift('fact_data.parquet', 'fact_table', engine, schema, if_exists='append')

    except Exception as e:
        print(f"Error en el proceso principal: {e}")
        raise

# Se evalua __main__ para ejecución directa e impresión por terminal
if __name__ == "__main__":
    run_load_parquet_redshift()