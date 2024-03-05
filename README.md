![Pandas](https://img.shields.io/badge/-Pandas-333333?style=flat&logo=pandas)
![Numpy](https://img.shields.io/badge/-Numpy-333333?style=flat&logo=numpy)
![Matplotlib](https://img.shields.io/badge/-Matplotlib-333333?style=flat&logo=matplotlib)
![Seaborn](https://img.shields.io/badge/-Seaborn-333333?style=flat&logo=seaborn)
![Scikitlearn](https://img.shields.io/badge/-Scikitlearn-333333?style=flat&logo=scikitlearn)
![FastAPI](https://img.shields.io/badge/-FastAPI-333333?style=flat&logo=fastapi)
![Docker](https://img.shields.io/badge/-Docker-333333?style=flat&logo=docker)
![Render](https://img.shields.io/badge/-Render-333333?style=flat&logo=render)
![Python](https://img.shields.io/badge/-Python-333333?style=flat&logo=python)

# Proyecto Integrador MLOps Steam 


## Introducción

Este proyecto es un ejercicio práctico para una API de consultas acerca de la plataforma de videojuegos Steam y un modelo de aprendizaje automático para un sistema de recomendación de videojuegos.

¡Gracias por ver mi proyecto!

## Contexto

Steam es una plataforma de distribución digital de videojuegos desarrollada por Valve Corporation. Fue lanzada en septiembre de 2003 como una forma para Valve de proveer actualizaciones automáticas a sus juegos, pero finalmente se amplió para incluir juegos de terceros. Cuenta con más de 325 millones de usuarios y más de 25.000 juegos en su catálogo. Es importante tener en cuenta que las cifras publicadas por SteamSpy son hasta el año 2017, porque a principios de 2018 Steam limitó la forma de obtener estadísticas, por eso no hay datos tan precisos.

## Datos

Para este proyecto se proporcionaron tres archivos JSON:

* **user_reviews.json.gz**  dataset que contiene las reseñas que los usuarios han dejado sobre los juegos que consumen, además de datos adicionales como si recomiendan o no ese juego, emoticones de gracioso y estadísticas de si el comentario fue útil o no para otros usuarios. También presenta el id del usuario que comenta con su url del perfil y el id del juego que comenta.

* **users_items.json.gz** dataset que contiene información sobre los juegos (ítemes) que poseen los usuarios, así como el tiempo acumulado que cada usuario jugó a un determinado juego.

* **steam_games.json.gz** dataset que contiene datos relacionados con los juegos en sí, como los título, el desarrollador, los precios, características técnicas, etiquetas, entre otros datos.

En el documento [Diccionario de datos](https://github.com/ga-romu/PI-MLOps-steam-recs/blob/main/notebooks/00_raw_data_dictonary.md) se encuetran los detalles de cada una de las variables de los conjuntos de datos.

## Proceso

### Transformaciones

Se procesaron los tres conjuntos de datos mediante un proceso de extracción, transformación y carga (ETL). Todos tenían una estructura anidada en algunas de sus columnas, las cuales contenían diccionarios o listas de diccionarios. Para convertir las claves de estos diccionarios en columnas, se implementaron diferentes estrategias. Posteriormente, se completaron valores nulos en variables relevantes para el proyecto. También se eliminaron columnas con una cantidad significativa de valores nulos o que no aportaban valor al proyecto, con el objetivo de optimizar el rendimiento de la API y considerar las limitaciones de almacenamiento en la implementación. Las transformaciones se llevaron a cabo utilizando la biblioteca Pandas.

Puedes ver los detalles del ETL en este [enlace](https://github.com/ga-romu/PI-MLOps-steam-recs/blob/main/notebooks/01_ETL.ipynb) 

### Feature engineering

Uno de los pedidos para este proyecto fue aplicar un análisis de sentimiento a los reviews de los usuarios. Para ello se creó una nueva columna llamada 'sentiment_analysis' que reemplaza a la columna que contiene los reviews donde clasifica los sentimientos de los comentarios con la siguiente escala:

* 0 si es negativo,
* 1 si es neutral
* 2 si es positivo.

Dado que el objetivo de este proyecto es realizar una prueba de concepto, se realiza un análisis de sentimiento básico utilizando VADER que es una biblioteca de procesamiento de lenguaje natural (NLP) en Python. El objetivo de esta metodología es asignar un valor numérico a un texto, en este caso a los comentarios que los usuarios dejaron para un juego determinado, para representar si el sentimiento expresado en el texto es negativo, neutral o positivo. 

* En la función 'analyze_sentiment':

    Si la puntuación es inferior a -0.05, la categoría se establece como 0 (negativa).
    Si la puntuación es superior a 0.05, la categoría se establece como 2 (positiva).
    En caso contrario, la categoría se establece como 1 (neutral).

Puedes ver los detalles del desarrollo [aquí](https://github.com/ga-romu/PI-MLOps-steam-recs/blob/main/notebooks/02_Feature_engineer.ipynb)

### Análisis exploratorio de los datos

Se realizó un análisis exploratorio de datos (EDA) a los tres conjuntos de datos que pasaron por el proceso de extracción, transformación y carga (ETL). El objetivo era identificar las variables relevantes para la construcción del modelo de recomendación. Se utilizaron las librerías Pandas para la manipulación de datos, Matplotlib y Seaborn para la visualización.

Puedes ver el detalle del análisis [aquí](https://github.com/ga-romu/PI-MLOps-steam-recs/blob/main/notebooks/03_EDA.ipynb)

### Modelo de aprendizaje automático

Se creó un modelo de aprendizaje automático para un sistema de recomendación de juegos.El modelo creado tiene una relación ítem-ítem, esto es, toma un juego y crea una lista de cinco juegos basada en la similitud. 

Para generar este modelo se adoptaron algoritmos basados en la memoria, los que abordan el problema del **filtrado colaborativo** utilizando toda la base de datos, tratando de encontrar usuarios similares al usuario activo (es decir, los usuarios para los que se les quiere recomendar) y utilizando sus preferencias para predecir las valoraciones del usuario activo.

La similitud entre los juegos (item_similarity) fue calculada a través de **similitud del coseno** que es una medida comúnmente utilizada para evaluar la similitud entre dos vectores en un espacio multidimensional. En el contexto de sistemas de recomendación y análisis de datos, la similitud del coseno se utiliza para determinar cuán similares son dos conjuntos de datos o elementos, y se calcula utilizando el coseno del ángulo entre los vectores que representan esos datos o elementos.

Puedes ver el desarrollo de este modelo [aquí](https://github.com/ga-romu/PI-MLOps-steam-recs/blob/main/notebooks/05_ML_recs_model.ipynb).

### Desarrollo de API

El desarrolo de la API fue hecho mediante el framework FastAPI. Para optimizar el rendimiento de la memoria RAM, he optado por crear datasets independientes por cada función, puedes encontrar las versiones en parquet de estos datsets [aqui](https://github.com/ga-romu/PI-MLOps-steam-recs/tree/main/data)

Con los datasets específicos he podido crear las siguientes funciones:

* **developer**: Esta función recibe como parámetro 'developer', que es la empresa desarrolladora del juego, y devuelve la cantidad de items que desarrolla dicha empresa y el porcentaje de contenido Free por año por sobre el total que desarrolla.


* **userdata**: Esta función tiene por parámentro 'user_id' y devulve la cantidad de dinero gastado por el usuario, el porcentaje de recomendaciones que realizó sobre la cantidad de reviews que se analizan y la cantidad de items que consume el mismo.

* **userforgenre**: Esta función recibe como parámetro el género de un videojuego y devuelve el top 5 de los usuarios con más horas de juego en el género ingresado, indicando el id del usuario y el url de su perfil.

* **best_developer_year**:  Esta función recibe como parámetro un año, de la columna 'release_year' y retorna el top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado.

* ** developer_reviews_analysis: Esta función recibe como parámetro el nombre de un desarrollador, retornando un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo

* **game_recommend**: Esta función recibe como parámetro el nombre de un juego y devuelve una lista con 5 juegos recomendados similares al ingresado.


Puedes ver el desarrollo de las funciones de consultas generales [aquí](https://github.com/ga-romu/PI-MLOps-steam-recs/blob/main/notebooks/04_API_functions.ipynb). 

Puedes ver el desarrollo de las funciones del modelo de recomendación [aquí](https://github.com/ga-romu/PI-MLOps-steam-recs/blob/main/notebooks/05_ML_recs_model.ipynb)

El código para generar la API se encuentra en el archivo [main.py](https://github.com/ga-romu/PI-MLOps-steam-recs/blob/main/main.py) y las funciones para su funcionamiento se encuentran en [api_functions](https://github.com/ga-romu/PI-MLOps-steam-recs/blob/main/api_functions.py). 

En caso de querer ejecutar la API desde localHost debes seguir los siguientes pasos:

- Clonar el proyecto  `git clone https://github.com/ga-romu/PI-MLOps-steam-recs`.
- Preparación del entorno de trabajo en Visual Studio Code:
    * Crear entorno: `python -m venv env`
    * Ingresar al entorno:  `venv\bin\activate`
    * Instalar dependencias: `pip install -r requirements.txt`
    * Actualizar pip según requerimientos: `pip install -upgrade pip`
- Ejecutar el archivo main.py desde consola activando uvicorn: `uvicorn main:app --reload`
- En la consola hacer Ctrl + clic sobre la dirección `http://XXX.X.X.X:XXXX` 
- Una vez en el navegador, escribir `/docs` a continuación de la dirección para acceder a ReDoc.
- En cada una de las funciones hacer clic en *Try it out* y luego introducir el dato que requiera o utilizar los ejemplos por defecto. Finalmente Ejecutar y observar la respuesta.

### Despliegue en Render

Para el despliegue de la API se seleccionó la plataforma Render que es una nube unificada para crear y ejecutar aplicaciones y sitios web, permitiendo el despliegue automático desde GitHub. Para esto se siguieron estos pasos:

- Generación de un Dockerfile cuya imagen es Python 3.11.7. Esto se hace porque Render usa por defecto Python 3.7, lo que no es compatible con las versiones de las librerías trabajadas en este proyecto, por tal motivo, se optó por desplegar el proyecto dentro de este contenedor. Se puede ver el detalle del documento [Dockerfile](https://github.com/ga-romu/PI-MLOps-steam-recs/blob/main/Dockerfile).
- Se generó un servicio nuevo  en `render.com`, conectado al presente repositorio y utilizando Docker como Runtime.
- Finalmente, el servicio queda corriendo en [https://pi-mlops-steam-recs.onrender.com](https://pi-mlops-steam-recs.onrender.com).

### Video

En este [video](https://drive.google.com/file/d/10az0K50LXkxSI1NAFrdK6F2On0zgqZlz/view) explico brevemente este proyecto mostrando el funcionamiento de la API.






