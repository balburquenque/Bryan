## Librerias ## 
import pandas as pd
## import collections
## import numpy as np
#%%
## Lectura de archivos de demanda hospitales y FNS ##
## El archivo excel contiene dos hojas llamadas "2017" y "2018"
## En la hoja 2017 hay 23 variables y 2053 registros, de los cuales uno de ellos
## no corresponde a información de un producto (el primer registro).
## En la hoja 2018 hay 23 variables y 2051 registros, de los cuales uno de ellos
## no corresponde a información de un producto (el primer registro). 

## Se leen las dos hojas del archivo excel y se almacenan en variables distintas ##
## de tal forma que se ignora la primera fila de ambas hojas y se seleccionan solo ##
## las variables que, en 1era instancia, se consideran relevantes para el estudio##
## es decir, se eligen las variables: Codigo, Descripcion, Unidad, y cada uno de ##
## los meses de consumo (Enero hasta diciembre). 
## DH = Datos Hostipal ##
DH_Los_Andes_2017 = pd.read_excel(r'C:\Users\Bryan\Dropbox\Datos\Datos_Hospital_Los_Andes\CONSUMOS HOSPITAL LOS ANDES 2017-2018.xls',
                                  sheet_name='2017',
                                  usecols="A:O,U,V",
                                  skiprows = [1])

DH_Los_Andes_2018 = pd.read_excel(r'C:\Users\Bryan\Dropbox\Datos\Datos_Hospital_Los_Andes\CONSUMOS HOSPITAL LOS ANDES 2017-2018.xls',
                                  sheet_name='2018',
                                  usecols="A:O,U,V",
                                  skiprows = [1])

## Información sobre las Dataframe ##
DH_Los_Andes_2017.info()
## Las variables Codigo, Descripcion, Unidad, no poseen valores nulos ##
DH_Los_Andes_2018.info()
## Las variables Codigo, Descripcion no poseen valores nulos. ##
## La variable Unidad posee solo 1 valor nulo ##

## Hay valors NA en la demanda de productos durante algunos meses ##
## que serán reemplazados por "0" ##
for i in range(3,15):
    DH_Los_Andes_2017.iloc[:,i].fillna(0, inplace=True)
    DH_Los_Andes_2018.iloc[:,i].fillna(0, inplace=True)

## Agrupación de productos que son iguales y suma de sus demandas por mes ##
Meses = DH_Los_Andes_2017.columns[3:15]
print(Meses)

suma = DH_Los_Andes_2017.groupby(["Codigo","Descripcion","Unidad"], axis=0)[Meses].sum()
suma.reset_index(inplace=True, drop=False)
suma.head()

promedio = DH_Los_Andes_2017.groupby(["Codigo","Descripcion","Unidad"], axis=0)["Precio"].mean()
promedio = promedio.to_frame()
promedio.reset_index(inplace=True, drop=False)
promedio = promedio.drop(["Descripcion","Unidad"], axis=1)

nuevo = suma.set_index("Codigo").join(promedio.set_index("Codigo"))
## OJO: cuando los fusiono se generan nuevas filas, los archivos originales
## tienen solamente 1283 filas, pero el nuevo objeto consta de 1311 !!! 
nuevo.reset_index(inplace=True, drop=False)
nuevo.head()

#no_repetidos = nuevo.duplicated(keep=False)
#nuevo = nuevo[~no_repetidos]

a=1
data=pd.DataFrame(index=Meses)
for k in nuevo["Codigo"]:
    aux= "P"+str(a)
    data[aux]=nuevo.loc[a-1,Meses]
    a=a+1
    

#### Otra posible forma


#DH_Siquiatrico = pd.read_excel(r'C:\Users\Bryan\Dropbox\Datos\Datos_Hospital_Psiquiatrico\CONSUMO HOSPITAL PSIQUIATRICO 2017-2018.xls')
#DH_San_Camilo = pd.read_excel(r'C:\Users\Bryan\Dropbox\Datos\Datos_Hospital_San_Camilo\CONSUMO HOSPITAL SAN CAMILO 2017-2018.xls')
#DFNS_San_HCVB = pd.read_excel(r'C:\Users\Bryan\Dropbox\Datos\Datos_SAN_HCVB\cc_resumen_egresos.xlsx')
#%%
## Ver tipo de información de variables HOSPITAL DE LOS ANDES ##
DH_Los_Andes.info()
##print [x for x, y in collections.Counter(DH_Los_Andes.Codigo).items() if y>1]
codigos_repetidos = []
unicos = []
for x in DH_Los_Andes.Codigo:    
    if x not in unicos:
        unicos.append(x)
    else:
        if x not in codigos_repetidos:
            codigos_repetidos.append(x)
            
print(codigos_repetidos)
duplicados_Los_Andes = DH_Los_Andes.duplicated()
print(DH_Los_Andes.loc[0:])
print(DH_Los_Andes[DH_Los_Andes.Codigo == 1300164])


#%%
## Caso Hospital de los Andes ##
## Se elimina la fila 1 porque no corresponde a información de un producto ##
asdf = DH_Los_Andes.drop([0], axis=0)
print(asdf.loc[1,:])
asdf.head()
