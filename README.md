# Crypto-price:

Este proyecto esta diseñado para realizar el seguimiento del precio en tiempo real de las 50 criptomonedas con mayor capitalización de mercado, para la injesta de datos se utilizo la API de la plataforma CoinGecko y Python es el lenguaje de programación seleccionado para procesar los datos y gestionarlos con otras tecnologías.

## Tecnologías y herramientas:

- Python: Lenguaje de programación seleccionado para el procesamiento de los datos y su gestión.
- Apache Airflow: Para la planificación y automatización de las tareas.
- Docker: Para contenerizar el proyecto y asegurar su correcta ejecución en diferentes entornos.
- Redshift: Para almacenar y consultar grandes volúmenes de datos relacionados con el mercado de criptomonedas.
- Pandas: Para el procesamiento y análisis de datos.
- Archivos Parquet: Para el almacenamiento eficiente de grandes volúmenes de datos.
- SQLAlchemy: Para manejar la conexión y gestión de la base de datos Redshift.

## Arquitectura del proyecto:

### Pipeline ETL:

   - *Extract:* Extrae la información en formato JSON a través de una solicitud GET a la API de CoinGecko, utilizando la biblioteca `requests` de Python.
         
      - `get_data_api.py`: Script de extracción de información cruda en formato JSON sobre las 50 criptomonedas con más capitalización de mercado ['id', 'name', 'symbol', 'current_price', 'last_updated', 'image', 'market_cap', 'market_cap_rank', 'market_cap_change_percentage_24h', 'total_volume', 'high_24h', 'low_24h', entre otros]

   - *Transform:* Procesa los datos extraídos, transformándolos en DataFrames utilizando la biblioteca Pandas. Posteriormente, los datos son transformados y        guardados en archivos de formato Parquet, optimizados para su almacenamiento y consulta eficiente.

      - `df_dim_crypto.py`: Script que procesa la información extraída y filtra los datos necesarios para generar el dataframe que abastecerá la *dim_table* en el posterior modelado de datos en Redshift. ['id', 'symbol', 'name'].
      - `df_facts_prices_crypto.py`: Script que procesa la información extraída y filtra los datos necesarios para generar el dataframe que abastecerá la *fact_table* en el posterior modelado de datos en Redshift. ['id', 'last_updated', 'current_price', 'market_cap', 'market_cap_rank'].
      - `df_calendar_table.py`: Script que crea el dataframe de una tabla calendario con rango de fechas desde el 1 de Enero del 2024 hasta el 31 de Diciembre del 2024 y que abastecerá la *calendar_table* en el posterior modelado de datos en Redshift ['date_column', 'year', 'month', 'day', 'name_of_month'].
      - `create_table_calendar.py`: Script que crea la *calendar_table* vacía dentro de la base de datos de Redshift en el esquema seleccionado, indicando los tipos de datos a cada columna y definiendo la clave pimaria.
      - `convertion_parquet.py`: Script que convierte los dataframes `df_dim_crypto.py`, `df_facts_prices_crypto.py` y `df_calendar_table.py` a formatos Parquet.

   - *Load:* Se conecta a la base de datos en Amazon Redshift utilizando `SQLAlchemy`, y carga los datos transformados en el esquema correspondiente. Este módulo gestiona la inserción de los archivos Parquet en tablas previamente definidas en la base de datos.

      - `connnection_db.py`: Script auxiliar que crea un motor de SQLAlchemy para realizar la conexión hacia la base de datos de Redshift.
      - `load_tables_in_db.py`: Script que carga los archivos Parquet ya generados, en la base de datos de Redshift.

### Automatización con Apache Airflow:

   - *Tasks:* Define las tareas individuales de extracción, transformación y carga (ETL) utilizando Airflow. Utiliza XCom para la transferencia de datos entre tareas, asegurando la correcta dependencia y flujo de datos entre las etapas del pipeline.

      - `run_extract.py`: Script donde se define la tarea de Extracción y guarda dichos datos en XCom
      - `run_transform.py`: Script donde se define la tarea de Transformación y guarda dichos datos en XCom
      - `run_load.py`: Script donde se define la tarea de Carga y guarda dichos datos en XCom
      - `run_update.py`: Script donde se define una tarea adicional que agrega dos columnas llamadas *date_column* y *time_column* a la *fact_table* y las actualiza

   - *Dags:* Orquesta la ejecución de las tareas en un flujo de trabajo definido en Airflow. Organiza las tareas de manera secuencial y dependiente, automatizando todo el proceso de extracción, transformación y carga de datos.

      - `dag_etl`: Script que orquesta la ejecución de las tareas definidas en *Tasks*, secuenciales y dependientes:
        `run_extract.py` >>  `run_transform.py` >> `run_load.py` >> `run_update.py`

![dag](https://github.com/user-attachments/assets/ca0ee71b-da4a-40ad-8acf-c2b4d648722c)

### Tests unitarios:

   - *Testing:* Creación de tests unitarios que verifican la funcionalidad de las funciones de manera individual, utilizando `Pytest` y `Mock`.

      - `count_columns`: Script auxiliar que cuenta las columnas del dataframe fact
      - `test_conteo_columnas`: Verifica que el valor de `count_columns` sea siempre igual a un valor esperado, en este caso = 5, ya que efectivamente estas son la cantidad de columnas que debe de traer el df fact, si difiere, el test fallará y nos dará a conocer que algo anda mal en la creación de dicho dataframe.
      - `test_manejo_de_errores`: Verifica que la función get_data maneje de forma correcta una respuesta exitosa (código de estado 200), un error de solicitud incorrecto (código de estado 400) y un error de clave incorrecta (código de estado 401)

### Archivos de configuración:

   - *Crypto Price:*

      - *README.md:* Documento principal que describe el propósito del proyecto, las herramientas utilizadas, la arquitectura general y las instrucciones necesarias para la instalación, configuración y ejecución del proyecto.

      - *requirements.txt:* Archivo que especifica las dependencias de Python necesarias para el correcto funcionamiento del proyecto. Incluye las versiones de las bibliotecas utilizadas, tales como Pandas, SQLAlchemy, requests, entre otras. Este archivo facilita la instalación de dependencias mediante pip.

      - *docker-compose.yml:* Define los servicios de Docker para el despliegue del entorno completo del proyecto. Especifica los contenedores que deben ejecutarse (como Airflow, Redis, PostgreSQL/Redshift) y sus configuraciones. Permite la orquestación de múltiples contenedores para asegurar la correcta ejecución del pipeline.

      - *dockerfile:* Archivo utilizado para crear una imagen Docker personalizada del proyecto. Define las instrucciones para instalar las dependencias y configurar el entorno dentro del contenedor, garantizando que el entorno de desarrollo sea consistente en diferentes máquinas.

## Modelado de datos:

Cuenta con una Tabla de Hechos, otra de Dimensiones y una de Calendario.
Con este modelado, donde sus Primary Keys y Foreing keys están bien definidas, nos aseguramos de que a la hora de querer analizar los datos, sea sencillo y eficaz.

![modelado](https://github.com/user-attachments/assets/32ebfb18-fc56-419c-9c3d-baa5de53e61c)

## Run Crypto Price:

1. Instalacion:
- Docker --> https://www.docker.com/products/docker-desktop/
- Airflow --> https://airflow.apache.org/
- Python --> https://www.python.org/downloads/

2. Clonar repositorio:
    ```bash
    git clone https://github.com/Ezetage/Crypto-price.git
    ```

3. Creación de entorno virtual: No es necesaria la ejecución con el entorno virtual activado pero si recomendado.
    ```bash
    Python -m venv env
    comando para activar entorno virtual: .\env\Scripts\Activate
    comando para desactivar entorno virtual: deactivate
    ```

4. Instalación de dependencias:
    ```bash
   pip install -r requirements.txt
    ```

5. Teniendo instalado y abierto Docker desktop:

- Creamos el contenedor y la imagen:
   ```bash
   docker-compose build
    ```
- Damos de alta el servidor: Con el primer comando (recomendado) no se verán los logs por terminal.

   ```bash
   docker-compose up -d
   docker-compose up
    ```

6. Si todo anduvo bien, habremos deployado Airflow con Docker. Verificamos la conexión a Airflow accediendo a su web service:

- http://localhost:8080/ 
- Usuario predeterminado: airflow
- Contraseña predeterminada: airflow

7. Configurar variables de entorno:

- Antes de correr cualquier Script, crear un archivo .env con las siguientes variables:

   ```bash
   AIRFLOW_UID=50000
   API_KEY=API KEY CoinGecko
   REDSHIFT_USERNAME=Usuario de Redshift
   REDSHIFT_PASSWORD=Contraseña de Redshift
   REDSHIFT_HOST=Host de Redshift
   REDSHIFT_PORT=Puerto de la base de datos
   REDSHIFT_DB=Nombre de la base de datos de Redshift
   REDSHIFT_SCHEMA=Esquema dentro de la base de datos Redshift
   ```

8. Tests:

- Para ejecutar los tests en forma local, correr el comando:
   ```bash
   pytest -v
   ```
   
- Configuración de Github Secrets:

Los Tests unitarios corren en cada Push y Pull request, configurado en el run.tests.yml de la carpeta github workflows

Para esto es necesario definir Secrets en el perfil de Github con la API KEY de CoinGecko