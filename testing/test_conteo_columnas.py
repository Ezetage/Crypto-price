import pytest
from main.conteo_columnas import cantidad_de_columnas

def test_conteo_columnas():
    expected_columns = 7  #7 es la cantidad de columnas del Dataframe

    actual_columns = cantidad_de_columnas

    #Se espera que la cantidad de columnas reales contadas sea 7, si difiere el test fallará
    assert actual_columns == expected_columns, f"Se esperaban {expected_columns} columnas y se encontraron {actual_columns}."