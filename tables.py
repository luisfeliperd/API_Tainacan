# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 11:01:23 2020

@author: Luis
"""

dfTables = {
        'collection':['id_instalacao','id','name','description','creation_date','modification_date','url'],
        'taxonomy':['id','name','description','allow_insert'],
        'term':['id_taxonomia','id','name','description','url', 'url_imagem', 'parent'],
        'inst_col_tax':['id_instalacao','id_colecao','id_taxonomia'],
        'metadata':['id_instalacao','id_colecao','id','name','description','metadata_type','required','collection_key', 'multiple','display','semantic_uri']
        }
