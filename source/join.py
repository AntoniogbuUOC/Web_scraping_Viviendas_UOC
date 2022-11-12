import os

import pandas as pd

from scrappingFunctions import join_data

if __name__=='__main__':
    # Se unen todos los csv generados anteriormente en uno solo
    dfGeneral = pd.DataFrame()
    listaFicheros = os.listdir('data/')
    for fichero in listaFicheros:
        print(fichero)
        dfFichero = pd.read_csv('data/'+fichero)
        dfGeneral = pd.concat([dfGeneral, dfFichero], axis=0)
        os.remove('data/'+fichero)
    dfGeneral.to_csv('../dataset/Viviendas_Madrid_Oeste.csv')
    #data = join_data(lista_localidad)
    #data.to_csv('../data/Casas_data.csv')
