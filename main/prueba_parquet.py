import pandas as pd
from get_data_api import load_api_key, get_data
from df_facts_prices_crypto import generar_dataframe_facts
from df_dim_crypto import generar_dataframe_dim

# Función para guardar DataFrames en formato .parquet
def save_to_parquet(df, filename):
    df.to_parquet(filename, index=False)  # Guardar como archivo .parquet

# Función principal para ejecutar el flujo
def main():
    try:
        # Generar DataFrame de hechos y guardarlo en .parquet
        df_facts = generar_dataframe_facts()
        save_to_parquet(df_facts, "datos_hechos.parquet")
        print("Datos de hechos guardados en 'datos_hechos.parquet'")

        # Generar DataFrame de dimensiones y guardarlo en .parquet
        df_dim = generar_dataframe_dim()
        save_to_parquet(df_dim, "datos_dimensiones.parquet")
        print("Datos de dimensiones guardados en 'datos_dimensiones.parquet'")

    except Exception as error:
        print(error)

# Evaluación de __main__ para ejecución directa
if __name__ == "__main__":
    main()