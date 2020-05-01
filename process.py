import pandas as pd
import numpy as np
from objects.dataframe_class import DataFrame_c
from geopy.geocoders import Nominatim
from time import sleep
from tqdm import tqdm
import googlemaps
import os


df = DataFrame_c().origin_df(route = 'outputs/houses/')

df_class = DataFrame_c()
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

df['Venta'] = df['Venta'].fillna(1)
df['Dormitorios'] = df['Dormitorios'].fillna(1)
df[df['Dormitorios'] == 0] = 1

#m2 = m2 techados if m2=nan
df.loc[df['Metros cuadrados'].isnull() == True,'Metros cuadrados'] = df.loc[df['Metros cuadrados'].isnull() == True,'Metros cuadrados techados']

df.dropna(inplace = True)

#Dropping bath and half baths columns
df.drop(axis = 1, columns = ['Medio baños'],inplace = True)
df = df.drop_duplicates()

#not consider unrealistic house prices
df = df[df['Venta'] > 45000]



lon = []
lat = []
for i in tqdm(df['Ubicacion']):
    try:
        geolocator = Nominatim(user_agent = 'app_w')
        location = geolocator.geocode(i,timeout = 2.5)
        if location is None:
            gmaps = googlemaps.Client(key = 'google_api_rent')
            geocode_result = gmaps.geocode(i)
            if geocode_result is None:
                lon.append(np.nan)
                lat.append(np.nan)
            else:
                lon.append(geocode_result[0]['geometry']['location']['lng'])
                lat.append(geocode_result[0]['geometry']['location']['lat'])
        else:
            lon.append(location.longitude)
            lat.append(location.latitude)
    except Exception as e:
        lon.append(np.nan)
        lat.append(np.nan)

for i in df.loc[2,'longitude']



lon
