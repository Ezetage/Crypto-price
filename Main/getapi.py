import requests
import os
from dotenv import load_dotenv

#Se carga el archivo API_KEY.env
load_dotenv("C:\\Users\\Eze\\Desktop\\Crypto price\\Main\\API_KEY.env")

#Se obtiene la Api Key del archivo API_KEY.env ya generado
api_key = os.getenv("API_KEY")

#Se evalúa si la api Key está correctamente configurada, caso contrario arrojará el texto definido para el error
if api_key is None:
    raise ValueError("La API KEY no está definida en el archivo .env")

#Si la api Key fue correctamente configurada, nos arrojará el json
url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50&sparkline=false&price_change_percentage=24h&locale=es&precision=2&x_cg_demo_api_key={api_key}"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

if response.status_code == 200:

    print(response.json())
else:
    print(f"Error: {response.status_code} - {response.text}")