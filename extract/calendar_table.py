import pandas as pd

# Genero una lista de fechas desde el primero de enero de 2024 hasta el 31 de diciembre de 2024
date_range = pd.date_range(start='2024-01-01', end='2024-12-31')

# Creo la tabla calendario a través de un df
calendar_df = pd.DataFrame({
    'date_column': date_range,
    'year': date_range.year,
    'month': date_range.month,
    'day': date_range.day,
    'name_of_month': date_range.strftime('%B') # %B de la función strftime permite traer el nombre del mes correspondiente a una fecha
})

# Imprimo por terminal para corroborar
print(calendar_df)