import os
import sys

# Se añade el directorio padre al sys.path para permitir la importación de los módulos necesarios
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from load.connection_db import create_redshift_engine
from sqlalchemy import text

def create_calendar_table(engine, schema: str) -> None:
    """
    Crea la tabla calendar_table en la base de datos Redshift si no existe.

    Args:
        engine: Motor de conexión a la base de datos.
    """
    
    def table_exists(table_name: str) -> bool:
        """
        Verifica si la tabla existe en el esquema de la base de datos.

        Args:
            table_name (str): Nombre de la tabla a verificar.

        Returns:
            bool: Verdadero si la tabla existe, Falso si no existe.
        """
        with engine.connect() as connection:
            query = text(
                f"""
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_schema = :schema
                    AND table_name = :table_name
                )
                """
            )
            result = connection.execute(query, {"schema": schema, "table_name": table_name})
            return result.fetchone()[0]

    with engine.connect() as connection:
        # Crear calendar_table si no existe
        if not table_exists("calendar_table"):
            connection.execute(
                text(
                    f"""
                    CREATE TABLE "{schema}".calendar_table (
                        date_column DATE PRIMARY KEY NOT NULL,
                        year INT,
                        month INT,
                        day INT,
                        name_of_month VARCHAR(50)
                    );
                    """
                )
            )
            print("Tabla 'calendar_table' creada exitosamente.")
        else:
            print("La tabla 'calendar_table' ya existe.")

# Se evalua __main__ para ejecución directa e impresión por terminal
if __name__ == "__main__":
    engine, schema = create_redshift_engine()
    create_calendar_table(engine, schema)