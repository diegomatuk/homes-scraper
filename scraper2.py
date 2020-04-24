import bs4 as bs
import urllib.request
from tqdm import tqdm

import json
import pandas as pd
import numpy as np
import time


location = []
type = []


m2 = []
m2_techados = []
baths = []
parking = []
half_baths = []
dorms = []
antiquy_building = []

park_near = []
condo = []
floor = []
alquiler = []
mant = []
link_pagina = []
link_image = []
num_contact = []

all = [location,type,m2,m2_techados,baths,parking,half_baths,
        dorms,antiquy_building,park_near,condo,floor,alquiler,mant,link_pagina,
        link_image,num_contact]


def check(lista,palabra,lista_apend,verbosa = False):
    if palabra not in juntar(lista):
        lista_apend.append('No hay informacion')
    for i in lista:
        if palabra.upper() in i.upper():
            lista_apend.append(i)
            if verbosa:
                break

def juntar(lista):
    string = ''
    for i in lista:
        string += i
    return string


#LOOP FOR PAGINATION
num = [i for i in range(1,51) ]
for number in tqdm(num):
    proyectos = urllib.request.urlopen(f'https://urbania.pe/buscar/alquiler-de-casas-en-lima?page={number}')
    soup = bs.BeautifulSoup(proyectos,'lxml')
    posting_card = soup.find_all('div',class_ = 'posting-card')
    temp = []
    for i in tqdm(posting_card):
        anuncio = i.find_all('a',class_ = 'go-to-posting')
        referencia = anuncio[0]['href']
        temp.append(anuncio[0]['href'])  #se le tiene que sumar a urbania para scrapear el resto como .format

        #CREATING A SCRAPER FOR THE URL OF THE EXACT HOUSE (EXTRACTING MORE VARIABLES)
        request2 = urllib.request.urlopen(f'https://urbania.pe{referencia}')
        soup2 = bs.BeautifulSoup(request2,'lxml')
        time.sleep(2)
        #Page/Image Link (V2)
        link_pagina.append(f'https://urbania.pe{referencia}')


        #Image links (V1)
        temp_link_image = list(i.find_all('div',class_ = 'posting-gallery-slider'))
        temp_link_image = temp_link_image[0].script

        temp_link_image = temp_link_image.text.replace('\n','').replace('\t','').split('=')

        if len(temp_link_image) > 1:
            try:
                temp_link_image = temp_link_image[1].split(',')[0].split(' ')[3][1:-1]
                link_image.append(temp_link_image)
            except:
                temp_link_image = temp_link_image[1].split(',')[0]
                link_image.append(temp_link_image)
        else:
            link_image.append(' ')


        #Prices (V1)
        preg_despues = i.find_all('span',class_ = 'ask-price')
        cost = i.find_all('span', class_ = 'first-price')
        if len(cost) > 0:
            alquiler.append(cost[0].text)
            # print(idx,'precio')
        elif len(preg_despues) > 0:
            alquiler.append(preg_despues[0].text)


        #EXACT LOCATION OF HOUSE (V1)
        lugar = i.find_all('div',class_ = 'posting-header')
        for locations in lugar:
            location.append(locations.find('span').text.replace('\n','').replace('\t',''))


        aa = ['stotal','scubierta','bano','cochera','dormitorio','toilete','antiguedad']
        clases = [f'icon-f-{aa[i]}' for i in range(0,len(aa))]

        temp2_house = []

        #ENTERING THE LINK OF THE HOUSE (V2)
        for i in (soup2.find_all('li',class_ = 'icon-feature')):
            temp2_house.append(i.text.replace('\n','').replace('\t',''))

        if len(temp2_house) > 0:
            check(temp2_house,'Superficie total',m2)
            check(temp2_house,'Superficie techada',m2_techados)
            # check(temp2_house,'Baños',baths)
            check(temp2_house,'Estacionamientos',parking)
            check(temp2_house,'Dormitorios',dorms)
            check(temp2_house,'Medio baño',half_baths)
            check(temp2_house,'Antigüedad',antiquy_building)
            #Baths
            for i in temp2_house:
                if 'Baño' in i:
                    if (len(i.split(' '))) < 2:
                        baths.append(i.split(' '))

        else:
            m2.append(np.nan)
            m2_techados.append(np.nan)
            baths.append(np.nan)
            parking.append(np.nan)
            dorms.append(np.nan)
            half_baths.append(np.nan)
            antiquy_building.append(np.nan)

        #MANTEINENCE
        mantenience = soup2.find_all('div',class_ = 'block-expensas')
        if len(mantenience) > 0:
            mant.append(mantenience[0].text.split(' ')[-1])
        else:
            mant.append('No Mantenience')

        #FLOOR AND PARK NEARBY
        temp_floor = []
        for i in soup2.find_all('ul',class_ = 'section-bullets'):
            for j in i:
                if j != '\n':
                    temp_floor.append(j.text)
        check(temp_floor,'Piso en el que se encuentra: ',floor)
        check(temp_floor,'Parque',park_near,verbosa = True)
        time.sleep(3)





#############NO TOCAR

#
# del link_pagina[-1]
len(link_pagina)


[len(i) for i in all]


df = pd.DataFrame({'Ubicacion':location,'Metros cuadrados':m2,'Metros cuadrados techados':m2_techados,
                'Baños':baths,'Parqueo':parking,'Medio baños':half_baths,'Dormitorios':dorms,'Antiguedad del edificio':antiquy_building,
                'Parque cercano':park_near,'Piso en el que se encuentra':floor,'Alquiler':alquiler,'Mantenimiento':mant,
                'Link Pagina':link_pagina,'Link imagen':link_image})


# baths.append('Error en no se donde (arreglar)')

df.shape

df.to_csv('Datos/Datos_casas')



prueba = urllib.request.urlopen('https://urbania.pe/inmueble/alquiler-de-departamento-en-cercado-de-miraflores-miraflores-3-dormitorios-ascensor-13475320')
prueba2 = bs.BeautifulSoup(prueba,'lxml')


69/73
#PARK NEARBY AND FLOOR
