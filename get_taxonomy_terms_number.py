import requests
import time
from collections import OrderedDict
import numpy as np
import plotly.graph_objects as go

instalacoes= {
    
    "Museu Victor Meirelles":"http://museuvictormeirelles.acervos.museus.gov.br",
    "Museu Histórico Nacional":"http://mhn.acervos.museus.gov.br",
    "Museu do Diamante":"http://museudodiamante.acervos.museus.gov.br",
    "Museu do Ouro":"http://museudoouro.acervos.museus.gov.br",
    "Museu Regional Casa dos Ottoni":"http://museuregionalcasadosottoni.acervos.museus.gov.br",
    "Museu de Itaipu":"http://museudearqueologiadeitaipu.museus.gov.br",
    "Funarte":"http://www.funarte.gov.br",
    "Museu do Índio":"http://tainacan.museudoindio.gov.br",
}


items_endpoint = '/wp-json/tainacan/v2/items'
collections_endpoint = '/wp-json/tainacan/v2/collections'
taxonomies_endpoint = '/wp-json/tainacan/v2/taxonomies'
terms_endpoint = '/wp-json/tainacan/v2/taxonomy/{}/terms'

#Para cada request é utilizado um try/except caso haja uma desconexão ou limitação da API. 

#Dicionário para armazenar os resultados.
result_dict = {}

#Para cada instalação do docionário de instalações
for instalacao in instalacoes.keys():
    
    #Indica que para cada instalação o valor do dicionário será outro dicionario, com o nome da taxonomia como chave e o numero de termos como valor.
    result_dict[instalacao] = {}
    
    #Faz um primeiro request geral para recuperar o total de páginas.
    try:
        response_page = requests.get(instalacoes[instalacao]+taxonomies_endpoint)
    except:
        time.sleep(10)
        response_page = requests.get(instalacoes[instalacao]+taxonomies_endpoint)
                            
    #Para cada página no intervalor de páginas retornado pelo total_pages.
    for page in range(int(response_page.headers['X-WP-TotalPages'])):
        
        try:
            response = requests.get(instalacoes[instalacao]+taxonomies_endpoint, params = {'paged':page+1})
        except:
            imte.sleep(10)
            response = requests.get(instalacoes[instalacao]+taxonomies_endpoint, params = {'paged':page+1})
            
        #para cada taxonomia resultante do ultimo request
        for taxonomy in response.json():
                                 
            #Pula a taxonomia padrão do Creative Commons.
            if taxonomy['name'] == 'Licenças (Creative Commons)':
                continue
            else:
                try:                 
                    terms_resp = requests.get(instalacoes[instalacao]+terms_endpoint.format(taxonomy['id']))
                except:
                    time.sleep(10)
                    terms_resp = requests.get(instalacoes[instalacao]+terms_endpoint.format(taxonomy['id']))
                
                print(instalacao, taxonomy['name'])
                result_dict[instalacao][taxonomy['name']] = len(terms_resp.json())


#Cria um dricionário ordenado para cada dicionário de cada museu resultante do processo anterior
museu = OrderedDict(sorted(result_dict['Museu do Índio'].items(), key=lambda x: x[1]))

#parametriza o gráfico no matplotlib
taxonomias = list(museu.keys())
valores = list(museu.values())

fig = go.Figure(data=[go.Bar(x=taxonomias, y=valores, text=valores, textposition='auto')])

fig.update_layout(title='Nº de Itens por Taxonomias', xaxis_tickfont_size=14,yaxis=dict(title='Nº de Itens',
        titlefont_size=16, tickfont_size=14))
                  
fig.show()
