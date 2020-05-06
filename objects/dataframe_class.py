import pandas as pd
import numpy as np



class DataFrame_c():
    def __init__(self, dataframe = None):
        self.dataframe = dataframe


    def origin_df(self,route):
        import os
        routes = os.listdir(route)
        d_df = pd.read_csv(route + f'/{routes[0]}')
        for i in routes[1:]:
            tempdf = pd.read_csv(route + f'{i}')
            d_df = d_df.append(tempdf)
        del d_df['Unnamed: 0']
        return d_df


    def data_to_numeric(self,df,series):
        return pd.to_numeric(df[series])

    def distritos_apply(self,x):
        a = [i.strip() for i in x.split(',')]
        x = ''
        for i in a:
            x+=i
        temp = ['Ancon','Ancón', 'Ate Vitarte','Barranco','Breña',
                'Carabayllo','Chaclacayo','Chorrillos','Cieneguilla','Comas','El Agustino','Independencia','La Molina',
                'Jesus Maria','Jesús María','La Victoria','Lince','Los Olivos','Lurigancho','Lurin','Lurín','Magdalena del Mar',
                'Miraflores','Pachacamac','Pucusana','Pueblo Libre','Puente Piedra','Punta Hermosa','Punta Negra',
                'Rimac','Rímac','San Bartolo','San Borja','San Isidro','San Juan de Lurigancho','San Juan de Miraflores',
                'San Luis','San Martin de Porres','San Miguel','Santa Anita','Santa Maria del Mar','Santa María del Mar',
                'Santa Rosa','Santiago de Surco','Surquillo','Villa el Salvador','Villa Maria del Triunfo','Asia','Mala','Cañete',
                'Magdalena','San Martín de Porres','San Antonio','Villa María del Triunfo','Callao']
        for district in temp:
            if district.upper() in x.upper():
                return district
    #CORRECTING THE REST OF THE DATA
    #Squared meters
    def correc_m2(self,x):
        return x.split('m²')[0]

    #Parking
    def correc_parking(self,x):
        if x == 'No hay informacion':
            return 1
        else:
            return x.split('Estacionamientos')[0]
    #half_baths
    def correc_half_baths(self,x):
        pass
    #
    def correc_dorms(self,x):
        return (x.split('Dormitorios')[0])
    #
    def correc_antiquy(self,x):
        temp = x.split('Antigüedad')
        if x == 'No hay informacion':
            return np.nan
        elif x == 'En construcciónAntigüedad':
            return 0
        elif x == 'A estrenarAntigüedad':
            return 0
        elif int(temp[0]):
            return int(temp[0])

    #
    def correc_near(self,x):
        if x == 'No hay informacion':
            return 0
        elif x != 'No hay informacion':
            return 1
    #Corerct floor data
    def correc_floor(self,x):
        import random as rnd
        if x!= 'No hay informacion':
            return int(x.split('Piso en el que se encuentra:')[1].strip())
        elif x == 'No hay informacion':
            return 5 + rnd.randint(-3,3)

    #correct renatl data
    def correc_alquiler(self,x):
        if 'S/' in x:
            return int(x.split('S/')[1].strip().replace(',',''))
        elif x == 'Consultar precio':
            return np.nan
        elif 'USD' in x:
            return 3.4*int(x.split('USD')[1].strip().replace(',',''))

    #Correct the manteniance data
    def correc_mant(self,x):
        if x == 'No Mantenience':
            return 1
        elif x!= 'No Mantenience':
            return float(x.replace(',',''))

    def num_floors(self,x):
        if x['Tipo'] == 'Casa':
            return np.ceil(x['Dormitorios']/4)
        else:
            return np.ceil(x['Dormitorios']/3)

    def pred_alquiler(self,x):
        pred = User().compute(m2 = x['Metros cuadrados'],
                            m2_techados = x['Metros cuadrados techados'],
                            parking = x['Parqueo'],dorms = x['Dormitorios'],
                            antiguedad = x['Antiguedad del edificio'],
                            park_near = x['Parque cercano'], floor = 1,
                            mantenimiento = x['Mantenimiento'], cant_pisos = 1,type = 'Casa',
                            distrito = x['Distrito'])
        return int(np.exp(pred))


    def imp_alcabala(self,x):
        if x['Antiguedad del edificio'] > 0:
            if x['Venta'] < 10 * (4300):
                return 0
            else:
                return (x['Venta'] - 10*(4300)) * 0.03
        else:
            return 0





DataFrame_c().origin_df('outputs/houses/')
