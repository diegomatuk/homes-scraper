import streamlit as st
import webbrowser
import pydeck as pdk
import plotly.graph_objects as go

import pandas as pd
import numpy as np
from objects.user import User
import plotly.express as px

from objects.dataframe_class import DataFrame_c
import _pickle as cPickle

st.sidebar.header('Rentabilidad en Bienes Raices')
seleccion = st.sidebar.radio('Tipos de servicio',('Prediccion de alquiler','Inversiones mas rentables'))



@st.cache
def load_data():
    a = pd.read_csv('outputs/output_houses.csv')
    try:
        del a['Unnamed: 0']
        del a['Unnamed: 0.1']
        del a['Unnamed: 0.1.1']
    except:
        pass
    del a['new_longitude']
    del a['new_latitude']
    return a


def chart(df):
    top = df.sort_values(by = 'rentabilidad',ascending = False)
    all_layer = pdk.Layer(
            type="ScatterplotLayer",
            data=df,
            get_position="[longitude, latitude]",
            radius_scale=6,
            get_radius=23,
            elevation_scale = 100,
            get_fill_color=[200, 30, 0, 160],
            pickable = True,
            get_line_color=[0, 0, 0],
            opacity = 0.75,
            radiusMinPixels = 2,
            radiusMaxPixels = 45,

    )
    color = pdk.Layer(
            type="ScatterplotLayer",
            data=top.iloc[:3,:],
            get_position="[longitude, latitude]",
            radius_scale=6,
            get_radius=23,
            opacity = 0.75,
            elevation_scale = 100,
            pickable = True,
            get_fill_color = [7, 114, 255],
            radiusMinPixels = 3.5,
            radiusMaxPixels = 45,
    )
    midpoint = (np.average(df['latitude']), np.average(df['longitude']))
    view = pdk.ViewState(latitude = midpoint[0], longitude= midpoint[1], zoom=10, bearing=0, pitch=0)

    return pdk.Deck(map_style='mapbox://styles/mapbox/light-v9',initial_view_state= view,layers=[all_layer,color])



def print_st(row,key):
    temp = pd.DataFrame({'Ubicacion': [row['Ubicacion']],'Metros Cuadrados': [row['Metros cuadrados']],
                    'Estacionamientos':[row.Parqueo],'Dormitorios':[row.Dormitorios],
                    'Años de antiguedad':[row['Antiguedad del edificio']],
                    'Precio de Venta': ['S/{0:,.0f}'.format(row.Venta)],
                    'Rentabilidad prevista': ["{0:.3%}".format(row.rentabilidad)]})


    # st.plotly_chart(fig)
    st.table(temp)
    if st.button('Ir al anuncio',key = key):
        webbrowser.open_new_tab(row['Link Pagina'])



def print_data(df):
    top = df.sort_values(by = 'rentabilidad')
    data = top.iloc[:3,:]
    # st.write(f'Distrito:{data['Ubicacion']}')
    st.write()

def main():
    if seleccion == 'Prediccion de alquiler':
        prediccion_alq() #PAGE 1
    elif seleccion == 'Inversiones mas rentables':
        rentabilidad()  #PAGE 2




def prediccion_alq():
    st.header('¿A cuanto debería alquilar mi depa?')
    st.write('''Para saber a cuanto deberias alquilar tu propiedad,
                hemos creado un modelo basado en mas de 10,000 registros existentes.
                Esto te va a permitir tener una idea de como valoriza el mercado tu casa/depa!.
                Pero para eso tenemos que saber un poco del mismo :)   ''')

    distrito = st.selectbox('¿En que distrito se encuentra?',User().distritos)
    m2 = st.number_input('¿Cuantos m² totales tiene?',value = 0,min_value = 0,step =1)
    m2_techados = st.number_input('¿Cuantos de estos m² son techados?',value = 0,min_value = 0,step = 1)

    if m2 < m2_techados:
        st.warning('Los m² totales tienen que ser iguales o mayores que los m² techados ')

    else:
        parqueo = st.number_input('Cantidad de estacionamientos',value = 0,min_value = 0,step = 1)
        dormitorios = st.number_input('Numero de dormitorios',value = 0,min_value = 0,step = 1)
        antiguedad = st.number_input('Antigüedad (en años) del edificio/casa',value = 0,min_value = 0,step = 1)
        parque = st.radio('¿Tiene un parque cerca? Puede ser interno o no',('Si','No'))

        if parque == 'Si':
            parque = 1
        else:
            parque = 0

        tipo = st.radio('Casa o Departamento',('Casa','Departamento'))
        cant_pisos = st.selectbox('¿Cuántos pisos tiene?',[1,2,3,4,5])
        if tipo == 'Casa':
            piso = 1

        elif tipo == 'Departamento':
            piso = st.slider('Que piso se encuentra',1,25)


    prediccion = User().compute(m2 = m2, m2_techados = m2_techados,parking = parqueo,dorms = dormitorios,
                                antiguedad = antiguedad,park_near = parque,floor = piso, mantenimiento = 0,
                                cant_pisos = cant_pisos,type = tipo, distrito = distrito)

    upper_lim = round(np.exp(prediccion[0] + 0.2774),0)
    lower_lim = round(np.exp(prediccion[0]))

    st.markdown(f'''<h1 style='text-align: center; color: red;'>Lo podrias alquilar entre:
                    S/ {int(lower_lim)} y {int(upper_lim)}</h1>''',unsafe_allow_html=True)


def rentabilidad():

    df = load_data()
    df['rentabilidad'] = pd.to_numeric(df['rentabilidad'])
    df = df[df['rentabilidad'] < 0.5]

    points = df[['latitude','longitude']]
    distrito = st.multiselect('Escoge un distrito',df['Distrito'].unique())
    puntos = df[df['Distrito'].isin(distrito)]

    if not distrito:
        st.pydeck_chart(chart(df))
        top = df.sort_values(by = 'rentabilidad',ascending = False)
        for i in range(1,4):
            rand_str = lambda n: ''.join([random.choice(string.lowercase) for i in xrange(n)])
            print_st(top.iloc[i],str(i))

    else:
        st.pydeck_chart(chart(puntos))
        top = puntos.sort_values(by = 'rentabilidad',ascending = False)
        for i in range(1,4):
            print_st(top.iloc[i],str(i))





    # ola = df.iloc[:1,:]
    # ola['html'] = ["<img src='" + r['Link imagen']
    #     + """' style='display:block;margin-left:auto;margin-right:auto;border:0;'><div style='text-align:center'>"""
    #     + "<br>" + "</div>"
    #     for ir, r in ola.iterrows()]
    #
    # #show the list of images as a dataframe
    # st.write(ola[['html']].to_html(escape=False), unsafe_allow_html=True)













if __name__ == '__main__':
    main()
