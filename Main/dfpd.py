import pandas as pd
import getapi

#Llamado al Script original y almacenado el variable
data = getapi.response.json()

#Creación del dataframe
df = pd.DataFrame(data)

#Filtro de columnas
columnas = ['id', 'symbol', 'name', 'last_updated', 'current_price', 'market_cap', 'market_cap_rank']
df = df[columnas]

print(df)