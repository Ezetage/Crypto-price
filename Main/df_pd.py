import pandas as pd
from main.get_data_api import load_api_key, get_data

#Se define como función el script
def generar_dataframe():

    api_key = load_api_key()
    data = get_data(api_key)

    #Se crea el Dataframe
    df = pd.DataFrame(data)

    #Se filtran las columnas requeridas
    columnas = ['id', 'symbol', 'name', 'last_updated', 'current_price', 'market_cap', 'market_cap_rank']
    df = df[columnas]

    return df

#Se evalua __main__ para ejecución directa e impresión por terminal
if __name__ == "__main__":
    df = generar_dataframe()
    print(df)