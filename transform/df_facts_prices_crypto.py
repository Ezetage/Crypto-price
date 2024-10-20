import pandas as pd
import os
import sys

# Se añade el directorio padre al sys.path para permitir la importación de los módulos necesarios
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extract.get_data_api import load_api_key, get_data

# Se define y nombra la función
def generar_dataframe_facts():
    """
    Genera un DataFrame que contiene las columnas de hechos a partir de los datos obtenidos de la API.

    - Carga la API KEY desde el archivo .env.
    - Solicita los datos de la API usando la API KEY.
    - Filtra las columnas 'id', 'last_updated', 'current_price', 'market_cap' y 'market_cap_rank' para formar el DataFrame de hechos.

    Returns:
        pd.DataFrame: Un DataFrame con las columnas seleccionadas para la tabla de hechos.
    """

    api_key = load_api_key()
    data = get_data(api_key)

    # Se crea el DataFrame
    df = pd.DataFrame(data)

    # Se filtran las columnas requeridas para la tabla de hechos
    columnas = ['id', 'last_updated', 'current_price', 'market_cap', 'market_cap_rank']
    df = df[columnas]

    return df

# Se evalua __main__ para ejecución directa e impresión por terminal
if __name__ == "__main__":
    df = generar_dataframe_facts()
    print(df)