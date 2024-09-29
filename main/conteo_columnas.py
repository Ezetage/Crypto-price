from main.df_pd import generar_dataframe

def conteo_columnas(df):
    return df.shape[1]  #shape 1 devuelve la cantidad de columnas del Dataframe

df = generar_dataframe()

cantidad_de_columnas = conteo_columnas(df)

print (cantidad_de_columnas)