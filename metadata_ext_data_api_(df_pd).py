#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import pandas as pd


# In[2]:


dict_endpoint = {
"col_endpoint":"/wp-json/tainacan/v2/collections",
"meta_endpoint":"/wp-json/tainacan/v2/collection/{}/metadata/?perpage={}",
"tax_endpoint":"/wp-json/tainacan/v2/taxonomies",
"item_endpoint":"/wp-json/tainacan/v2/collection/{}/items/?perpage={}&paged={}"}


# In[3]:


instalacoes= {    
    "Museu Victor Meirelles":["http://museuvictormeirelles.acervos.museus.gov.br","1"],
    "Museu Histórico Nacional":["http://mhn.acervos.museus.gov.br","2"],
    "Museu do Diamante":["http://museudodiamante.acervos.museus.gov.br","3"],
    "Museu do Ouro":["http://museudoouro.acervos.museus.gov.br","4"],
    "Museu Regional Casa dos Ottoni":["http://museuregionalcasadosottoni.acervos.museus.gov.br","5"],
    "Museu de Itaipu":["http://museudearqueologiadeitaipu.museus.gov.br","6"],
    "Museu das Bandeiras":["http://museusibramgoias.acervos.museus.gov.br/","7"],
    "Museu das Missões":["http://museudasmissoes.acervos.museus.gov.br/","8"]
}


# In[4]:


colunas = ['id_instalacao','collection_id','id_metadado','name','description','metadata_type','required','collection_key',
           'multiple','display','semantic_uri']

tabelametadados = pd.DataFrame(columns=colunas)


# In[7]:


for k in instalacoes.keys():
    
    print(k)
    collections = requests.get(instalacoes[k][0]+dict_endpoint["col_endpoint"]).json()
   
    for collection in collections:
                        
        metadata = requests.get(instalacoes[k][0]+dict_endpoint["meta_endpoint"].format(collection["id"],
        len(collection["metadata_order"]))).json()
        
        for meta in metadata:
            
            tabelametadados = tabelametadados.append({'id_instalacao' : instalacoes[k][1],
                'collection_id' : collection["id"],'id_metadado':meta["id"],'name':meta["name"],
                'description':meta["description"],'metadata_type':meta["metadata_type"],'required':meta["required"],
                'collection_key':meta["collection_key"],'multiple':meta["multiple"],'display':meta["display"],
                'semantic_uri':meta["semantic_uri"]}, ignore_index=True)


# In[8]:


tabelametadados.to_csv('metadadosIbram2.csv')

