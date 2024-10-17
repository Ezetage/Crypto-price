import os
import urllib.parse
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Cargando variables de entorno
load_dotenv()

def create_redshift_engine():
    """
    Crea un motor de SQLAlchemy para conectarse a una base de datos de Redshift.
    
    Returns:
        Engine: Un objeto Engine de SQLAlchemy conectado a la base de datos de Redshift.
    """
    # Cargando credenciales desde .env
    REDSHIFT_DB = os.getenv('REDSHIFT_DB')
    REDSHIFT_USERNAME = os.getenv('REDSHIFT_USERNAME')
    REDSHIFT_PASSWORD = urllib.parse.quote_plus(os.getenv('REDSHIFT_PASSWORD'))  # Manejo de caracteres especiales
    REDSHIFT_HOST = os.getenv('REDSHIFT_HOST')
    REDSHIFT_PORT = os.getenv('REDSHIFT_PORT')
    REDSHIFT_SCHEMA = os.getenv('REDSHIFT_SCHEMA')

    # Creando motor de SQLAlchemy
    engine = create_engine(
        f'postgresql+psycopg2://{REDSHIFT_USERNAME}:{REDSHIFT_PASSWORD}@{REDSHIFT_HOST}:{REDSHIFT_PORT}/{REDSHIFT_DB}'
    )
    return engine, REDSHIFT_SCHEMA