import pandas as pd
import os
import sys

# Se añade el directorio padre al sys.path para permitir la importación de los módulos necesarios
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transform.df_facts_prices_crypto import generar_dataframe_facts
from transform.df_dim_crypto import generar_dataframe_dim
from transform.df_calendar_table import calendar_table

# Se define la función para guardar los df en formato parquet
def guardar_parquet(df, filename):
    """
    Guarda el DataFrame en un archivo .parquet.

    Args:
        df (DataFrame): El DataFrame que se desea guardar.
        filename (str): Nombre del archivo de salida (incluye extensión .parquet).
    """

    df.to_parquet(filename, index=False)

# Se corre el flujo de conversión
def run_convertion_parquet():
    """
    Ejecuta el flujo completo de conversión de los DataFrames generados a archivos .parquet.

    Llama a las funciones que generan los DataFrames de hechos y dimensiones, luego guarda los resultados en archivos .parquet y los imprime por consola.

    Raises:
        Exception: Si ocurre algún error durante la generación de los DataFrames o al guardar 
        los archivos .parquet. se captura la excepción y se propaga (raise)
    """

    try:

        df_facts = generar_dataframe_facts()
        guardar_parquet(df_facts, "fact_table.parquet")
        print("Datos de hechos guardados en 'fact_table.parquet'")

        df_dim = generar_dataframe_dim()
        guardar_parquet(df_dim, "dimension_table.parquet")
        print("Datos de dimensiones guardados en 'dimention_table.parquet'")

        df_calendar = calendar_table()
        guardar_parquet(df_calendar, "calendar_table.parquet")
        print("Tabla calendario guardada en calendar_table.parquet")
        
        return df_facts, df_dim, df_calendar

    except Exception as e:
        print(f"Error en la conversión: {e}")
        raise

# Se evalua __main__ para ejecución directa e impresión por terminal
if __name__ == "__main__":
    extracted_data = {}
    run_convertion_parquet()