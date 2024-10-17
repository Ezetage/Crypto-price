import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from extract.get_data_api import get_data

def run_extract(**kwargs):
    api_key = os.getenv('API_KEY')
    
    extracted_data = get_data(api_key=api_key)
    
    # Se guardan los datos en XCom
    kwargs['ti'].xcom_push(key='extracted_data', value=extracted_data)