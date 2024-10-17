import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from transform.df_facts_prices_crypto import generar_dataframe_facts
from transform.df_dim_crypto import generar_dataframe_dim

# Se define la función para guardar los df en formato parquet
def guardar_parquet(df, filename):
    df.to_parquet(filename, index=False)

# Se corre el flujo de conversión
def run_convertion_parquet():
    try:

        df_facts = generar_dataframe_facts()
        guardar_parquet(df_facts, "fact_data.parquet")
        print("Datos de hechos guardados en 'fact_data.parquet'")

        df_dim = generar_dataframe_dim()
        guardar_parquet(df_dim, "dimention_data.parquet")
        print("Datos de dimensiones guardados en 'dimention_data.parquet'")

        return df_dim, df_dim

    except Exception as error:
        print(error)

# Se evalua __main__ para ejecución directa e impresión por terminal
if __name__ == "__main__":
    extracted_data = {}
    run_convertion_parquet()