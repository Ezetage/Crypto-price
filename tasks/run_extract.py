import os
import sys

# Se añade el directorio padre al sys.path para permitir la importación de los módulos necesarios
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extract.get_data_api import get_data

def run_extract(**kwargs):
    """
    Función que extrae datos de una API y los almacena en XCom para su uso posterior en el flujo de trabajo de Airflow.

    Args:
        **kwargs: Argumentos adicionales, incluyendo el contexto de ejecución de Airflow.

    Raises:
        Exception: Si hay un problema al obtener los datos de la API.
    """

    api_key = os.getenv('API_KEY')
    
    extracted_data = get_data(api_key=api_key)
    
    # Se guardan los datos en XCom
    kwargs['ti'].xcom_push(key='extracted_data', value=extracted_data)