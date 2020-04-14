# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 16:50:14 2020

@author: Luis
"""
#Internal path structure
import sys
sys.path.append('') 
from dicts import api_access as api, inbcm, tables

import pandas as pd
import time
import requests
from sqlalchemy import create_engine

mysqlEngine = create_engine('mysql+pymysql://root:xxxx@localhost:3306/tainacan_api')
dbConnection = mysqlEngine.connect()
                                                                    ##Instalações e Coleções##

#Convert the installation DataFrame to a SQL Table
pd.DataFrame.from_dict(api.install_dict).to_sql('instalacao', dbConnection, if_exists = 'append', chunksize = 1000, index=False)

#Collect data from collection endpoint on Tainacan API per Installation
for i in range(len(api.install_dict['id'])):

    #Reset the collection dataframe for each instalation.
    collection_table = pd.DataFrame(columns=tables.dfTables['collection'])
    
    print("Verificando a instalação {}".format(api.install_dict['name'][i]))
    
    #Use try and except to avoid bad requests to API endpoint.
    try:
        for collection in requests.get(api.install_dict["url"][i]+api.dict_endpoint['col_endpoint']).json():
            
            print("Verificando a coleção {}".format(collection['name']))
        
            #Insert data from API into collection DataFrame
            collection_table = collection_table.append({'id_instalacao':api.install_dict['id'][i],'id':collection["id"],
                                                        'name':collection["name"], 'description':collection["description"],
                                                        'creation_date':collection["creation_date"],'modification_date':collection["modification_date"],
                                                        'url':collection["url"]}, ignore_index=True)
    except:
        print("Erro na requisição da instalação {}, tentendo novamente em 1 minuto".format(api.install_dict['name'][i]))
        time.sleep(60)
        
        for collection in requests.get(api.install_dict["url"][i]+api.dict_endpoint['col_endpoint']).json():
            
            
            print("Verificando a coleção {}".format(collection['name']))
            collection_table = collection_table.append({'id_instalacao':api.install_dict['id'][i],'id':collection["id"],
                                                        'name':collection["name"], 'description':collection["description"],
                                                        'creation_date':collection["creation_date"],'modification_date':collection["modification_date"],
                                                        'url':collection["url"]}, ignore_index=True)
    time.sleep(10)
    
    #Convert the collection DataFrame to it respective SQL Table
    print("Escrevendo os dados de coleções da instalação {} no Banco de Dados".format(api.install_dict['name'][i]))
    collection_table.to_sql('colecao', dbConnection, if_exists = 'append', chunksize = 1000, index=False)


                                                                        ##Taxonomias##
#Collect data from taxonomy endpoint on Tainacan API per Installation
for i in range(len(api.install_dict['id'])):
    
    #Reset the taxonomy dataframe for each instalation.
    taxonomies_table = pd.DataFrame(columns=tables.dfTables['taxonomy'])
    
    print("Verificando a instalação {}".format(api.install_dict['name'][i]))
    
    taxonomy_resp = requests.get(api.install_dict['url'][i]+api.dict_endpoint['tax_endpoint']).json()
    time.sleep(10)
    paged = 0
    
    #The response of API came in a interval of 10 results perpage, we used while to interate between the result pages, until there is no more result to show
    while taxonomy_resp != []:
        
        paged += 1
        print("Verificando a página {} de taxonomias".format(paged))
        taxonomy_resp = requests.get(api.install_dict['url'][i]+api.dict_endpoint['tax_endpoint']+"/?paged={}".format(paged)).json()
        
        time.sleep(5)       
        
        for taxonomy in taxonomy_resp:
                        
            taxonomies_table = taxonomies_table.append({'id':taxonomy['id'], 'name':taxonomy['name'], 'description': taxonomy['description'], 'allow_insert': taxonomy['allow_insert']}, ignore_index=True)
            
            print("Verificando a taxonomia {}".format(taxonomy['vame']))
            
    #Convert the taxonomy DataFrame to it respective SQL Table
    print("Escrevendo os dados de taxonomias da instalação {} no Banco de Dados".format(api.install_dict['name'][i]))
    taxonomies_table.to_sql('taxonomia', dbConnection, if_exists = 'append', chunksize = 1000, index=False)


                                                                            ##Termos##

#Collect data from terms endpoint on Tainacan API per Installation
for i in range(len(api.install_dict['id'])):
    
    print("Verificando a Instalação {}".format(api.install_dict['name'][i]))
    
    #Terms are get by taxonomies, so we need to repeat the process of getting taxonomy data above
    taxonomy_resp = requests.get(api.install_dict['url'][i]+api.dict_endpoint['tax_endpoint']).json()
    time.sleep(10)
    paged = 0
    
    while taxonomy_resp != []:
        paged += 1
        
        print("Verificando a página {} de taxonomias".format(paged))
        
        taxonomy_resp = requests.get(api.install_dict['url'][i]+api.dict_endpoint['tax_endpoint']+"/?paged={}".format(paged)).json()
        time.sleep(5)
        
        
        for taxonomy in taxonomy_resp:
            
            print("Verificando os termos taxonomia {}".format(taxonomy['name']))
            
            #Reset terms Dataframe for every installation
            terms_table = pd.DataFrame(columns=tables.dfTables['term'])
            
            term_resp = requests.get(api.install_dict['url'][i]+api.dict_endpoint["term_endpoint"].format(taxonomy['id'])).json()
            time.sleep(10)
            
            print("Verificando {} termos".format(len(term_resp)))
            
            for term in term_resp:
                terms_table = terms_table.append({'id_taxonomia':taxonomy['id'],'id': term['id'],'name': term['name'],'description': term['description'], 'url': term['url'], 'url_imagem':term['header_image'], 'parent':term['parent']}, ignore_index=True)
            
            #Convert the terms DataFrame to it respective SQL Table
            print("Escrevendo os termos da taxonomia {} no Banco de Dados".format(taxonomy['name']))
            terms_table.to_sql('termos', dbConnection, if_exists = 'append', chunksize = 1000, index=False)
    

                                                        ##Relação Instalacao, Taxonomia e Coleção##
                                                        
#Some taxonomies arent designated to collections, so we need to made a relationship table for installations, collections and taxonomies

#Create installation, collection and taxonomy relation dataframe
inst_col_tax_table = pd.DataFrame(columns=tables.dfTables['inst_col_tax'])

#Collect data from installation, collection and taxonomy endpoint on Tainacan API per Installation
for i in range(len(api.install_dict['id'])):
    
    print("Verificando a Instalação {}".format(api.install_dict['name'][i]))
    
    taxonomy_resp = requests.get(api.install_dict['url'][i]+api.dict_endpoint['tax_endpoint']).json()
    time.sleep(10)
    paged = 0
    
    #Relation between taxonomies and collection are get by taxonomy endpoint, so we need to repeat the process of get taxonomy data from API.
    while taxonomy_resp != []:
        
        paged += 1
        taxonomy_resp = requests.get(api.install_dict['url'][i]+api.dict_endpoint['tax_endpoint']+"/?paged={}".format(paged)).json()
        time.sleep(7)
        
        print("Verificando a página {}".format(paged))
        
        print("Quantidade de Taxonomias {}".format(len(taxonomy_resp)))
        
        for taxonomy in taxonomy_resp:
            
            #Check if a taxonomy have collections using it
            if len(taxonomy['collections_ids']) > 0:
                
                for collection in taxonomy['collections_ids']:
                    inst_col_tax_table = inst_col_tax_table.append({'id_taxonomia':taxonomy['id'], 'id_colecao':collection, 'id_instalacao':api.install_dict['id'][i]}, ignore_index=True)
                    
            else:
                inst_col_tax_table = inst_col_tax_table.append({'id_taxonomia':taxonomy['id'], 'id_instalacao':api.install_dict['id'][i]}, ignore_index=True)

print("Escrevendo dados da relação entre instalação, coleções e taxonomia no Banco de Dados")
#Convert the relationship DataFrame to it respective SQL Table
inst_col_tax_table.to_sql('inst_col_tax', dbConnection, if_exists = 'append', chunksize = 1000, index=False)

                                                                        ##Metadados##
                                                                        
#Collect data from metadata endpoint on Tainacan API per Installation
for i in range(len(api.install_dict['id'])):
    
   #Reset metadata Dataframe for every installation
    metadata_table = pd.DataFrame(columns=tables.dfTables['metadata'])
    
    print("Verificando a Instalação {}".format(api.install_dict['name'][i]))
    
    collections_resp = requests.get(api.install_dict['url'][i]+api.dict_endpoint["col_endpoint"]).json()
    time.sleep(10)
    
    #Metadata data are get by collections, so we need to repeat ethe processes of access collection endpoint
    for collection in collections_resp:

        print("Verificando a coleção {}".format(collection['name']))

        metadata_resp = requests.get(api.install_dict['url'][i]+api.dict_endpoint["meta_endpoint"].format(collection["id"]), params= {'perpage':'200'}).json()
        time.sleep(5)

        print("Verificando {} metadados".format(len(metadata_resp)))

        for metadata in metadata_resp:
            
            metadata_table = metadata_table.append({'id_instalacao' : api.install_dict['id'][i],
                'id_colecao' : collection["id"],'id':metadata["id"],'name':metadata["name"],
                'description':metadata["description"],'metadata_type':metadata["metadata_type"],'required':metadata["required"],
                'collection_key':metadata["collection_key"],'multiple':metadata["multiple"],'display':metadata["display"],
                'semantic_uri':metadata["semantic_uri"]}, ignore_index=True)
    
    #Convert the metadata DataFrame to it respective SQL Table
    print("Escrevendo os dados de metadado da instalação {} no Banco de Dados".format(api.install_dict['name'][i]))
    metadata_table.to_sql('metadado', dbConnection, if_exists = 'append', chunksize = 1000, index=False)
