import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from transform.df_facts_prices_crypto import generar_dataframe_facts

# Se define y nombra la función
def conteo_columnas(df):
    return df.shape[1]  # shape 1 devuelve la cantidad de columnas del Dataframe

# Se llama al dataframe ya generado e importado
df = generar_dataframe_facts()

cantidad_de_columnas = conteo_columnas(df)

print (cantidad_de_columnas)