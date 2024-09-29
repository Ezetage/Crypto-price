import requests
import os
from dotenv import load_dotenv

#Carga de la API_KEY
def load_api_key():
    load_dotenv("C:\\Users\\Eze\\Desktop\\Crypto price\\Main\\API_KEY.env")
    api_key = os.getenv("API_KEY")
    if api_key is None:
        raise ValueError("La API KEY no está definida en el archivo .env")
    return api_key

#Solicitud a la API y devolución de datos
def get_data(api_key):
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50&sparkline=false&price_change_percentage=24h&locale=es&precision=2&x_cg_demo_api_key={api_key}"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    #Manejo de errores    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 400:
        raise Exception("Error: 400 - Bad Request")
    elif response.status_code == 401:
        raise Exception("Error: 401 - API Key incorrecta")
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

#Se evalua __main__ para ejecución directa e impresión por terminal
if __name__ == "__main__":
    try:
        api_key = load_api_key()
        data = get_data(api_key)
        print(data)
    except Exception as error:
        print(error)