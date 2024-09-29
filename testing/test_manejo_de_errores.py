import pytest
import requests
from unittest.mock import patch
from main.get_data_api import get_data

def test_conexión_200():
    #Conexión exitosa
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'data': 'mocked data'}
        
        api_key = "api_key_valida"
        result = get_data(api_key)
        
        assert result == {'data': 'mocked data'}
        mock_get.assert_called_once()

def test_conexión_400():
    #Conexión sin éxito, bad request
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 400
        
        api_key = "api_key_valida"
        
        with pytest.raises(Exception) as excinfo:
            get_data(api_key)
        
        assert str(excinfo.value) == "Error: 400 - Bad Request"
        mock_get.assert_called_once()

def test_conexión_401():
    #Conexión sin éxito, clave incorrecta
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 401
        
        api_key = "api_key_invalida"
        
        with pytest.raises(Exception) as excinfo:
            get_data(api_key)
        
        assert str(excinfo.value) == "Error: 401 - API Key incorrecta"
        mock_get.assert_called_once()