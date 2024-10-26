import os
import sys

# Se añade el directorio padre al sys.path para permitir la importación de los módulos necesarios
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.transform.df_facts_prices_crypto import generar_dataframe_facts

# Se define y nombra la función
def conteo_columnas(df):
    """
    Cuenta la cantidad de columnas en el DataFrame proporcionado.

    Args:
        df (DataFrame): El DataFrame del cual se desea contar las columnas.

    Returns:
        int: La cantidad de columnas en el DataFrame.
    """
    
    return df.shape[1]  # shape 1 devuelve la cantidad de columnas del Dataframe

# Se llama al dataframe ya generado e importado
df = generar_dataframe_facts()

cantidad_de_columnas = conteo_columnas(df)

print (cantidad_de_columnas)