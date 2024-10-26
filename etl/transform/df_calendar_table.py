import pandas as pd

def calendar_table():
    """
    Genera un DataFrame con datos del calendario.

    Returns:
        pd.DataFrame: DataFrame con la tabla de calendario.
    """
    # Se genera una lista de fechas desde el primero de enero de 2024 hasta el 31 de diciembre de 2024
    date_range = pd.date_range(start='2024-01-01', end='2024-12-31')

    # Se crea la tabla calendario a través de un DataFrame
    calendar_df = pd.DataFrame({
        'date_column': date_range.strftime('%Y-%m-%d'),             # Columna de fecha en formato yyyy-mm-dd
        'year': date_range.year,                                    # Columna de año en formato yyyy
        'month': date_range.month,                                  # Columna de mes en formato m
        'day': date_range.day,                                      # Columna de día en formato d
        'name_of_month': date_range.strftime('%B')                  # Nombre del mes correspondiente
    })

    return calendar_df

# Prueba de la función
if __name__ == "__main__":
    df_calendar = calendar_table()
    print(df_calendar)