import streamlit as st
import webbrowser

import pandas as pd
import numpy as np
from objects.user import User
from objects.dataframe_class import DataFrame_c
import _pickle as cPickle

st.sidebar.header('Rentabilidad en Bienes Raices')
seleccion = st.sidebar.radio('Tipos de servicio',('Prediccion de alquiler','Inversiones mas rentables'))


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
    df_class = DataFrame_c()
    df = df_class.origin_df('outputs/houses/')
    df['Distrito'] = df['Ubicacion'].apply(df_class.distritos_apply)
    df['Antiguedad del edificio'] = df['Antiguedad del edificio'].apply(df_class.correc_antiquy)
    df['Parque cercano'] = df['Parque cercano'].apply(df_class.correc_near)
    df['Mantenimiento'] = df['Mantenimiento'].apply(df_class.correc_mant)
    df['Parqueo'] = df['Parqueo'].apply(df_class.correc_parking)
    df['Venta'] = df['Venta'].apply(df_class.correc_alquiler)
    df['Metros cuadrados'] = df['Metros cuadrados'].apply(df_class.correc_m2)
    df['Metros cuadrados techados'] = df['Metros cuadrados techados'].apply(df_class.correc_m2)
    df['Dormitorios'] = df['Dormitorios'].apply(df_class.correc_dorms)
    df['Piso en el que se encuentra'] = df['Piso en el que se encuentra'].apply(df_class.correc_floor)

    del df['Piso en el que se encuentra']
    df[['Metros cuadrados','Metros cuadrados techados','Dormitorios']] = df[['Metros cuadrados','Metros cuadrados techados','Dormitorios']].replace('No hay informacion',np.nan)
    df['Metros cuadrados'] = pd.to_numeric(df['Metros cuadrados'])
    df['Metros cuadrados techados'] = pd.to_numeric(df['Metros cuadrados techados'])
    df['Dormitorios'] = pd.to_numeric(df['Dormitorios'])
    df['Parqueo'] = pd.to_numeric(df['Parqueo'])


    df = df[df['Venta'] > 45000]
    st.dataframe(df)






if __name__ == '__main__':
    main()




#
# '''  LINKS IN BUTTONS
#     url = 'https://www.streamlit.io/'
#
#     if st.button('Open browser'):
#         webbrowser.open_new_tab(url)
#    '''




















# #Ttile
# st.title('Titulo')
#
# #Header/subheader/text
# st.header('Header')
# st.subheader('sub-header')
# st.text('Texto')
# st.write()  #can wrtie functions also
#
# #Color text
# st.success('Succes')
# st.info('Informacion')
# st.warning('Warning')
# st.error('Error')
# st.exception('Mensaje de error de codigo')
#
#
# #Widgets (Checkboxs)
# if st.checkbox('Show/Hide'):
#     st.write('Este es un depa')
#
# #radio
# status = st.radio('Cual es tu estado?',('Activo','Inactivo'))
# st.write(status)
#
# #select-box
# variable = st.selectbox('Distrito',['La Molina','Los Olivos','San Isidro','Surco'])
# st.write(f'Seleccionaste {variable}')
#
# #multi select
# ocupacion = st.multiselect('Donde trabajas',['La Molina','Los Olivos','San Isidro','Surco'])
# st.write(ocupacion)
#
# #slider
# edad = st.slider('cual es tu edad',1,90)
#
# #botones
# if st.button('Boton'):
#     st.success('Benee')
#
#
# #Text input
# name = st.text_input('Cual es tu nombre')
#
#
# #progress bar
# import time
# bar = st.progress(0)
# for p in range(10):
#     bar.progress(p+1)
#
# #spinner
# with st.spinner('Esperando'):
#     time.sleep(3)
# st.success('Bravo!')
#
#
# #SIDEBAR
# st.sidebar.header('Nosotros')
# st.sidebar.text('Este es el texto de nosotros')


# @st.cache   #PERFORMANCE IS BETTER (for functions )


#Plot
# st.pyplot()

#DataFframes
# st.dataframe('df')
#Tables

# st.table('df')
