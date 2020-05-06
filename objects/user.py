import pandas as pd
import numpy as np
import _pickle as cPickle




class User():
    def __init__(self,
                m2 = None,
                m2_techados = None,
                parking = None,
                half_baths = None,
                dorms = None,
                antiguedad = None,
                park_near = None,
                floor = None,
                alquiler = None,
                cant_pisos = None,
                distrito = None,
                type = None):
        self.m2 = m2
        self.m2_techados = m2_techados
        self.parking = parking
        self.half_baths = half_baths
        self.dorms = dorms
        self.antiguedad = antiguedad
        self.park_near = park_near
        self.floor = floor
        self.alquiler = alquiler
        self.cant_pisos = cant_pisos
        self.distrito = distrito
        self.type = type
        self.distritos = ['Ancón', 'Ate Vitarte','Barranco','Breña',
                    'Carabayllo','Chaclacayo','Chorrillos','Cieneguilla','Comas','El Agustino','Independencia','La Molina',
                    'Jesús María','La Victoria','Lince','Los Olivos','Lurigancho','Lurín','Magdalena del Mar',
                    'Miraflores','Pachacamac','Pucusana','Pueblo Libre','Puente Piedra','Punta Hermosa','Punta Negra',
                    'Rímac','San Bartolo','San Borja','San Isidro','San Juan de Lurigancho','San Juan de Miraflores',
                    'San Luis','San Martin de Porres','San Miguel','Santa Anita','Santa Maria del Mar','Santa María del Mar',
                    'Santa Rosa','Santiago de Surco','Surquillo','Villa el Salvador','Villa Maria del Triunfo','Asia','Mala','Cañete',
                    'Magdalena','San Martín de Porres','San Antonio','Villa María del Triunfo','Callao']

        self.coefs = pd.read_csv('outputs/lasso_coeficients.csv').iloc[:,1:]


    def replace_dist(self,distrito):
        temp = {'Rímac':'Rimac_Agust_Independen' ,'El Agustino':'Rimac_Agust_Independen', 'Independencia':'Rimac_Agust_Independen',
                    'Cieneguilla':'Cienegui_Pachacam_Lurin' , 'Pachacamac':'Cienegui_Pachacam_Lurin', 'Lurin':'Cienegui_Pachacam_Lurin', 'Lurín':'Cienegui_Pachacam_Lurin',
                    'Villa el Salvador':'Chorrillos_VillaSalvador_VMT','Chorrillos':'Chorrillos_VillaSalvador_VMT','Villa María del Triunfo':'Chorrillos_VillaSalvador_VMT',
                    'Jesús María':'Jesus Maria',
                   'Ancón':'Callao_Luriganch_Ancon_Carabay_PuentePie','Carabayllo':'Callao_Luriganch_Ancon_Carabay_PuentePie','Lurigancho':'Callao_Luriganch_Ancon_Carabay_PuentePie',
                    'Callao':'Callao_Luriganch_Ancon_Carabay_PuentePie',
                    'Puente Piedra':'Callao_Luriganch_Ancon_Carabay_PuentePie'}
        if distrito in temp.keys():
            return temp[distrito],temp
        else:
            return distrito,temp

    def dummy_var_dist(self,distrito):
        distrito,temp = self.replace_dist(distrito)
        lista = [0 for i in range(0,(len(self.distritos) - len(temp)))]
        for ix,i in enumerate(User().coefs.iloc[:,11:].columns.tolist()):
            if distrito in i:
                lista[ix] = 1
        return lista

    def dummy_var_tipo(self,type):
        if type == 'Casa':
            return 1,0
        elif type == 'Departamento':
            return 0,1


    def compute(self,m2,m2_techados,parking,dorms,antiguedad,park_near,floor,mantenimiento,cant_pisos,type,distrito):
        distrito = self.dummy_var_dist(distrito)
        tipo = self.dummy_var_tipo(type)
        data = [m2,m2_techados,parking,dorms,antiguedad,park_near,floor,mantenimiento,cant_pisos]
        data.append(tipo[0])
        data.append(tipo[1])
        data = data + distrito
        with open('outputs/lasso.pkl','rb') as file:
            lasso = cPickle.load(file)



        return lasso.predict([data])

    







user = User()


lista = user.compute(120,120,2,2,0,0,5,480,1,'Departamento','Miraflores')
int(np.exp(lista))
