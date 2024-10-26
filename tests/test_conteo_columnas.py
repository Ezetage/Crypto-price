import os
import sys


# Se añade el directorio padre al sys.path para permitir la importación de los módulos necesarios
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.count_columns import cantidad_de_columnas

# Se llama al dataframe ya generado e importado
def test_conteo_columnas():
    cantidad_columnas_esperada = 5  #5 es la cantidad de columnas del Dataframe

    cantidad_columnas_actual = cantidad_de_columnas

    # Se espera que la cantidad de columnas reales contadas sea 5, si difiere el test fallará
    assert cantidad_columnas_actual == cantidad_columnas_esperada, f"Se esperaban {cantidad_columnas_esperada} columnas y se encontraron {cantidad_columnas_actual}."