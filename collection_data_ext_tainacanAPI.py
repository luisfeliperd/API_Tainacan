import requests
import json
import pandas as pd

dict_endpoint = {
"col_endpoint":"/wp-json/tainacan/v2/collections",
"meta_endpoint":"/wp-json/tainacan/v2/collection/{}/metadata/?perpage={}",
"tax_endpoint":"/wp-json/tainacan/v2/taxonomies",
"item_endpoint":"/wp-json/tainacan/v2/collection/{}/items/?perpage={}&paged={}"}

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

colunas = ['id_instalacao','id_coleção','name','description','creation_date','modification_date','url']
tabelacolecoes = pd.DataFrame(columns=colunas)

for k in instalacoes.keys():
    collection = requests.get(instalacoes[k][0]+dict_endpoint["col_endpoint"]).json()
    for col in collection:
        tabelacolecoes = tabelacolecoes.append({'id_instalacao':instalacoes[k][1],'id_coleção':col["id"],'name':col["name"],
        'description':col["description"],'creation_date':col["creation_date"],'modification_date':col["modification_date"],'url':col["url"]}, ignore_index=True)

tabelacolecoes.to_csv('colecoesIbram.csv')