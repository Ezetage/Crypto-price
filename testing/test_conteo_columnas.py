import pytest
from main.conteo_columnas import cantidad_de_columnas

#Se llama al dataframe ya generado e importado
def test_conteo_columnas():
    expected_columns = 5  #5 es la cantidad de columnas del Dataframe

    actual_columns = cantidad_de_columnas

    #Se espera que la cantidad de columnas reales contadas sea 7, si difiere el test fallará
    assert actual_columns == expected_columns, f"Se esperaban {expected_columns} columnas y se encontraron {actual_columns}."