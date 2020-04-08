import requests
import json
import pandas as pd
import time

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
taxonomy_endpoint = "/wp-json/tainacan/v2/taxonomies"
colunas = ['collections_ids','id','name','description','allow_insert']
tabelataxonomies = pd.DataFrame(columns=colunas)

for k in instalacoes.keys():
    resp = requests.get(instalacoes[k][0]+taxonomy_endpoint).json()
    time.sleep(3)
    paged = 0

    while resp != []:
        paged += 1
        resp = requests.get(instalacoes[k][0]+taxonomy_endpoint+"/?paged={}".format(paged)).json()
        time.sleep(3)
        for taxonomy in resp:
            tabelataxonomies = tabelataxonomies.append({'collections_ids': "|".join([str(integer) for integer in taxonomy['collections_ids']]),'id':taxonomy['id'], 'name':taxonomy['name'], 'description': taxonomy['description'], 'allow_insert': taxonomy['allow_insert']}, ignore_index=True)
            
            
print(tabelataxonomies)
tabelataxonomies.to_csv('taxonomies.csv')