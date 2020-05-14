# -*- coding: utf-8 -*-
"""
Created on Wed May  6 21:26:15 2020

@author: luisr
"""
#Internal path structure 
import sys
sys.path.append('C://Users//luisr//OneDrive//Área de Trabalho//crossover_ibram')
from dicts import api_access as api, tables
import functions
import pandas as pd
from sqlalchemy import create_engine

mysqlEngine = create_engine('mysql+pymysql://root:Lotus.123@localhost:3306/tainacan_api')
dbConnection = mysqlEngine.connect()

#Truncate Collection and Instalation tables
#functions.truncate_table('colecao')
#functions.truncate_table('instalacao')

#Convert the installation DataFrame to a SQL Table
pd.DataFrame.from_dict(api.install_dict).to_sql('instalacao', dbConnection, if_exists = 'append', chunksize = 1000, index=False)

#Collect data from collection endpoint on Tainacan API per Installation
for i in range(len(api.install_dict['id'])):
    
    #Reset the collection dataframe for each instalation.
    collection_table = pd.DataFrame(columns=tables.dfTables['collection'])
    
    print("Verificando a instalação {}".format(api.install_dict['name'][i]))

    r = functions.try_request(api.install_dict["url"][i]+api.dict_endpoint['col_endpoint'])
    
    if r.json() == []:
        print("Resultado Nulo")
        collection_table = collection_table.append({'id_instalacao':api.install_dict['id'][i],
                                                    'name':"Requisição vazia", 'description':"Requisição vazia",
                                                    'creation_date':"Requisição vazia",'modification_date':"Requisição vazia",
                                                    'url':"Requisição vazia"}, ignore_index=True)
        
    for collection in r.json():
        
        print("Verificando a coleção {}".format(collection['name']))
        #Insert data from API into collection DataFrame
        
        collection_table = collection_table.append({'id_instalacao':api.install_dict['id'][i],
                                                    'name':collection["name"], 'description':collection["description"],
                                                    'creation_date':collection["creation_date"],'modification_date':collection["modification_date"],
                                                    'url':collection["url"]}, ignore_index=True)
    
    #Convert the collection DataFrame to it respective SQL Table
    print("Escrevendo os dados de coleções da instalação {} no Banco de Dados".format(api.install_dict['name'][i]))
    collection_table.to_sql('colecao', dbConnection, if_exists = 'append', chunksize = 1000, index=False)
