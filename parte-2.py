# Programación multiparadigma para las TIC
# Examen del 8/1/2024
# parte-2.py
# Visualización de datos de AEMET usando Panel

import param
import pandas as pd
import panel as pn
import geoviews as gv
from holoviews import opts

# El programa principal está definido después de la clase MedicionesAEMET

class MedicionesAEMET(param.Parameterized):

    provincia = param.Selector(label='Provincia seleccionada') # Provincia de la estación para ser visualizada. Si es 'TODAS' entonces se visualizan todas las estaciones.
    mostrar_nieve = param.Boolean(False, label='visualizar solo estaciones que registran nieve')  # nieve
    altura = param.Integer(0, label='Altura mínima') # Altura mínima que debe tener la estación para ser visualizada.
    # Ver referencia para parámetro de tipo booleano: https://param.holoviz.org/reference.html#param.__init__.Boolean


    # ¡¡¡ESTE MÉTODO NO TIENE QUE MODIFICARSE!!!
    def __generar_texto_lecturas(self):
        lecturas = []
        for _, row in self.__datosMediciones.iterrows():
            lect = ()
            lect += ('L',) if row['prec'] > 0 else ()
            lect += ('V',) if row['vv'] > 30*1000/60/60 else ()
            lect += ('B',) if row['vis'] < 1 else ()
            lect += ('N',) if row['nieve'] > 0 else ()
            lecturas.append(','.join(lect))
        self.__datosMediciones['lecturas'] = lecturas

    def __init__(self, datosMediciones: pd.DataFrame, **kwargs):
        super().__init__(**kwargs)
        self.__datosMediciones = datosMediciones.copy()
        self.__generar_texto_lecturas()

        # 2. Establecer la lista de provincias disponibles.
        # Añadir a la lista el elemento 'TODAS' en primera posición
        # para visualizar todas las mediciones de todas las provincias.
        lista_provincias = ['TODAS']+sorted(self.__datosMediciones['provincia'].unique().tolist())
        self.param['provincia'].objects=lista_provincias
      


        self.param['provincia'].objects = lista_provincias # No es necesario cambiar esto
        MedicionesAEMET.provincia = 'TODAS' # Valor inicial. No es necesario cambiar esto

        # 3. Establecer el rango de valores admitidos por el parámetro altura.
        
        # RELLENAR EL CÓDIGO AQUÍ...
        max_altura = int(self.__datosMediciones['alt'].max())
        min_altura = int(self.__datosMediciones['alt'].min())
        self.param['altura'].bounds=(min_altura,max_altura)
        rango = (int(min_altura), int(max_altura)) # No es necesario cambiar esto      
        MedicionesAEMET.param['altura'].bounds = rango # No es necesario cambiar esto 

   
    def __filtrar_datos_a_visualizar(self) -> pd.DataFrame:
        # 4. Elegir qué mediciones de estaciones meteorológicas visualizar
        # de acuerdo a los valores de los parámetros elegidos.
        datos_a_visualizar = self.__datosMediciones
        if self.provincia != 'TODAS':
            datos_a_visualizar=datos_a_visualizar[datos_a_visualizar['provincia']==self.provincia]
        datos_a_visualizar=datos_a_visualizar[datos_a_visualizar['alt']>=self.altura]
        if self.mostrar_nieve:
            datos_a_visualizar = datos_a_visualizar[datos_a_visualizar['lecturas'].str.contains('N', na=False)]

        return datos_a_visualizar
      


    

    # ¡¡¡ESTE MÉTODO NO TIENE QUE MODIFICARSE!!!
    def plot(self, **kwargs):
        
        datos_a_visualizar = self.__filtrar_datos_a_visualizar()
        
        mapa = gv.tile_sources.OSM
        dict_opts = dict(width=1000, height=600)
        mapa = mapa.options(**dict_opts)
        
        labels = gv.Labels(datos_a_visualizar, kdims=['lon', 'lat'], vdims='lecturas').opts(
            opts.Labels(text_font_size='20pt', yoffset=1000))
        puntos = gv.Points(datos_a_visualizar, ['lon', 'lat']).opts(size=10, tools=['hover'])
        overlay = puntos * labels
        overlay.opts(
            opts.Labels(text_font_size='20pt', yoffset=1000),
            opts.Points(color='blue', size=5))

        return mapa if puntos.shape[0] == 0 else mapa * overlay


# 1. Obtener la lista de mediciones de estaciones meteorológicas de la AEMET
# en un DataFrame. Usar el archivo "mediciones-examen-provincia.csv"
# con la nueva columna "provincia" rellenada generado en el ejercicio 1.
# En caso de no disponer del archivo del ejercicio 1, usar
# el archivo "mediciones-examen-provincia-aportado.csv" que se proporciona.
# Usar esta referencia para hacerlo: https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
datosMediciones = pd.read_csv('mediciones-examen-provincia.csv')


componente = MedicionesAEMET(datosMediciones, name="Estaciones meteorologicas")
claves_lectura = "<b>Claves de lectura:<br>L: lluvia<br>V: viento fuerte<br>B: niebla<br>N: nieve</b>"
toggle_nieve = pn.widgets.Toggle(name='Mostrar solo nieve', button_type='success')
toggle_nieve.link(componente,value='solo_nieve')
c_l = pn.widgets.StaticText(value=claves_lectura, align=('center', 'center'), style={'font-size': "25px"})
layout = pn.Column(pn.Row(componente.param, componente.plot), c_l)
layout.show()















