#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
import json
from collections import defaultdict


# In[3]:


instalacao = {"Museu Victor Meirelles":"http://museuvictormeirelles.acervos.museus.gov.br/"}

collection_endpoint = "wp-json/tainacan/v2/collections"
items_endpoint = "wp-json/tainacan/v2/collection/{}/items"


# In[8]:


collection_resp = requests.get(instalacao['Museu Victor Meirelles']+collection_endpoint).json()
paged = 0

for collection in collection_resp:
    
    items_resp = requests.get(instalacao['Museu Victor Meirelles']+items_endpoint.format(collection['id'])).json()
    
    print("ID da coleção:", collection['id'])
    
    #Itera pelas páginas de itens, até não existir mais itens na página
    while items_resp != []:
        paged+=1
        
        items_resp = requests.get(instalacao['Museu Victor Meirelles']+items_endpoint.format(collection['id']), {'paged':paged}).json()
        
        for item in items_resp['items']:
            
            print("Item:", item['id'])
            #Coleta os metadados estruturais do item
            print(collection['id'], item['id'], item['title'], item['description'], item['creation_date'],item['modification_date'])
            
            metadata_dict = defaultdict(list)
            
            for metadata in item['metadata'].keys():
                
                print("Metadata:", item['metadata'][metadata]['name'])
                #Acompanhar as excessões: existem valores que são strings, dicionários e listas
                value_list = []
                
                if type(item['metadata'][metadata]['value']) == list:
                    value_list = []
                    
                    for valor in item['metadata'][metadata]['value']:
                        
                        if type(valor) == dict:
                            value_list.append(valor['name'])
                            
                        elif type(valor) == str:
                            value_list.append(valor)
                        
                elif type(item['metadata'][metadata]['value']) == dict:
                    value_list.append(item['metadata'][metadata]['value']['name'])
                
                elif type(item['metadata'][metadata]['value']) == str:
                    value_list.append(item['metadata'][metadata]['value'])
                
                else:
                    value_list.append("")
                    
                metadata_dict[item['metadata'][metadata]['id']].append("||".join(value_list))


# In[ ]:




