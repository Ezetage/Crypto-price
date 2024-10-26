import pandas as pd
import os
import sys

# Se añade el directorio padre al sys.path para permitir la importación de los módulos necesarios
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extract.get_data_api import load_api_key, get_data

# Se define como función el script
def generar_dataframe_dim():
    """
    Genera un DataFrame que contiene las columnas de dimensiones a partir de los datos obtenidos de la API.

    - Carga la API KEY desde el archivo .env.
    - Solicita los datos a la API utilizando la API KEY.
    - Filtra las columnas 'id', 'symbol' y 'name' para formar el DataFrame de dimensiones.

    Returns:
        pd.DataFrame: Un DataFrame con las columnas seleccionadas para la tabla de dimensiones.
    """

    api_key = load_api_key()
    data = get_data(api_key)

    # Se crea el Dataframe
    df = pd.DataFrame(data)

    # Se filtran las columnas requeridas para la tabla de dimensiones
    columnas = ['id', 'symbol', 'name']
    df = df[columnas]

    return df

# Se evalua __main__ para ejecución directa e impresión por terminal
if __name__ == "__main__":
    df = generar_dataframe_dim()
    print(df)