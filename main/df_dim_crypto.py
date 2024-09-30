import pandas as pd
from main.get_data_api import load_api_key, get_data

#Se define como función el script
def generar_dataframe_dim():

    api_key = load_api_key()
    data = get_data(api_key)

    #Se crea el Dataframe
    df = pd.DataFrame(data)

    #Se filtran las columnas requeridas para la tabla de dimensiones
    columnas = ['id', 'symbol', 'name']
    df = df[columnas]

    return df

#Se evalua __main__ para ejecución directa e impresión por terminal
if __name__ == "__main__":
    df = generar_dataframe_dim()
    print(df)