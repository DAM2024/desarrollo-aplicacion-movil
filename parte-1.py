# Programación multiparadigma para las TIC-3.8
# Examen del 8/1/2024
# parte-1.py
# Obtención y tratamiento de datos de AEMET usando Pandas

from typing import Any
import requests
import pandas as pd

def leer_recurso_JSON(**kargs) -> Any:
    """Esta función devuelve el contenido de un recurso obtenido al hacer un GET
    sobre la url 'URL' de AEMET. Necesita recibir la clave del api en 'API_KEY'.

    Returns:
        Any: Diccionario (dict) cuando se recibe un único objeto descrito JSON.
        Lista (list) de diccionarios cuando se reciben múltiples objetos JSON en una lista.
        Se devuelve None si hay un error. Esto es exactamente igual a lo que se ha hecho en clase.
    """
    retVal = None

    headers = {'api_key': kargs['API_KEY']}
    response = requests.get(kargs['URL'], headers=headers)
    if response.status_code == 200:
        retVal = response.json()

    return retVal

# 1. Escribir el código de esta función.
# ESTA FUNCIÓN DEBE MANTENER EL DICCIONARIO COMO ÚNICO PARÁMETRO.
# Usar esta referencia para leer un fichero .csv en un DataFrame: https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
def leer_recurso_DataFrame(**kargs) -> pd.DataFrame:
    """Esta función devuelve un DataFrame de Pandas con la información
    obtenida. Se peude invocar de dos maneras: A) pasando la url como valor de la clave 'URL' y
    la clave del api en 'API_KEY' y B) pasando el nombre del archivo con extensión .csv
    como valor de la clave 'fileName'. ESTA FUNCIÓN DEBE USAR OBLIGATORIAMENTE LA FUNCIÓN leer_recurso_JSON()
    cuando se invoca del modo A.
    
    Returns:
        pd.DataFrame: Este es el DataFrame devuelto. Se devuelve un DataFrame vacío si hay un error. 
    
    """ 

    

    frame_a_devolver = pd.DataFrame()
    if 'URL' in kargs and 'API_KEY' in kargs:
        json_data = leer_recurso_JSON(URL=kargs['URL'], API_KEY=kargs['API_KEY'])
        if json_data is not None and 'datos' in json_data:
            frame_a_devolver = pd.read_json(json_data['datos'])
        elif json_data is not None:
            frame_a_devolver = pd.DataFrame(json_data)
    elif 'fileName' in kargs:
        frame_a_devolver = pd.read_csv(kargs['fileName'])
    return frame_a_devolver
    # Para verificar si un diccionario contiene una clave usar el operando adecuado. Ver https://docs.python.org/3.8/reference/expressions.html#membership-test-operations

    # RELLENAR EL CÓDIGO DE LA FUNCIÓN AQUÍ...
    
    
    



# 2. Obtener la lista de mediciones de estaciones meteorológicas de la AEMET
# del archivo "mediciones-examen.csv".
# Se debe usar la función leer_recurso_DataFrame().


# 3. Obtener la lista de todas las estaciones meteorológicas de la AEMET con su provincia.
# Esto se ha hecho en clase. La referencia está aquí https://opendata.aemet.es/dist/index.html#/valores-climatologicos/Inventario%20de%20estaciones%20(valores%20climatol%C3%B3gicos).
#
# 3.1. Obtener el documento general JSON haciendo un GET de 'url_estaciones' que devuelve
# en el campo 'datos' la url de la que después se deben obtener todas las
# estaciones meteorológicas.
url_estaciones = 'https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones/'
api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkYXZpZC5tZWx0emVyQHVwbS5lcyIsImp0aSI6IjY1NGYyZTA5LWE5ZGMtNDUzNy1iNGQ5LWMzOTg0Njk2MjExZiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjYzODUzOTg3LCJ1c2VySWQiOiI2NTRmMmUwOS1hOWRjLTQ1MzctYjRkOS1jMzk4NDY5NjIxMWYiLCJyb2xlIjoiIn0._pDYjMZcXqiB_S8apsXg79oRm9fMnA8TrFU-0Z1QInc'

#datos_recibidos = leer_recurso_JSON( ...RELLENAR EL PASO DE PARÁMETROS... )
datos_recibidos = leer_recurso_JSON(URL=url_estaciones, API_KEY=api_key)


if datos_recibidos != None:
    # 3.2. Si se ha conseguido obtener el documento general, obtener ahora todas las
    # estaciones meteorológicas con sus provincias como un DataFrame de Pandas
    # haciendo GET sobre la url indicada por el campo 'datos'
    # Se debe usar la función leer_recurso_DataFrame()
    url_datos=datos_recibidos['datos']
    datos_estaciones: pd.DataFrame = leer_recurso_DataFrame(URL=url_datos, API_KEY=api_key)

    if not datos_estaciones.empty:
        # 4. Añadir a datos_mediciones una columna 'provincia' que contenga el nombre de la provincia
        # en que se encuentra cada estación que ha hecho las mediciones. Cada medición de datos_mediciones 
        # dispone del identificador de estación en la columna "idema". En la tabla datosEstaciones cada
        # estación tiene el identificador de estación en la columna "indicativo" y su provincia en la
        # columna "provincia".
        
        # RELLENAR EL CÓDIGO DEL PASO 4 AQUÍ...
        datos_mediciones = leer_recurso_DataFrame(fileName='mediciones-examen.csv')
        datos_mediciones = datos_mediciones.sort_values(by=['idema', 'fint']).drop_duplicates(subset='idema', keep='last')

        datos_mediciones = pd.merge(datos_mediciones, datos_estaciones[['indicativo', 'provincia']], left_on='idema', right_on='indicativo', how='left')

        datos_mediciones.to_csv('mediciones-examen-provincia.csv', index=False)

        # 5. Escribir datos_mediciones con la nueva columna "provincia" rellenada
        # en el fichero 'mediciones-examen-provincia.csv' usando el método DataFrame.to_csv().
        # Ver referencia: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html#pandas-dataframe-to-csv
        # NO SE DEBE ESCRIBIR LA COLUMNA 'index' DEL DataFrame EN EL ARCHIVO.
        
        # RELLENAR EL CÓDIGO DEL PASO 5 AQUÍ...



    else:
        print('El DataFrame "datos_estaciones" está vacío.')
else:
    print('La variable "datos_recibidos" no contiene un DataFrame.')