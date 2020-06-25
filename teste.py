# -*- coding: utf-8 -*-
''' Neste codigo, sao criados arquivos csv
    com media e variancia de degree, media de betweenness,
    media de closeness, entropia, numero de vertices e arestas
    para as redes mensais da amazonia e australia
'''

import os
import math
import re
from igraph import Graph

# retorna a substring de s entre os separadores i e f
def substringEntreChars(s, i, f):
	sub = s[s.find(i)+1 : s.find(f)]
	return sub

# funcao para ordenar nomes de arquivos
def ordenaNomesArquivos(f):
	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
	return sorted(f, key = alphanum_key)

long_i = 113
long_f = 154

lat_i = -44
lat_f = -10

def Cx(x):
    return math.floor((x - long_i)*2)

def Cy(y):
    return math.floor((y-lat_i)*2)

# diretorio para resultados e dados
rd = os.path.dirname(os.getcwd())
rdAu = rd + '/Resultados e Dados/Australia'

# leitura dos arquivos gml dos grafos da Australia
fAu = os.listdir(rdAu + "/grafosMes") # lista com os nomes dos grafos
fAu = ordenaNomesArquivos(fAu) # ordena os nomes cronologicamente

# pega o primeiro grafo para fazer o teste
arquivo = fAu[0]
   
# abre o grafo
g = Graph.Read_GML(rdAu + "/LatLong05/grafosMes/" + arquivo)

print(g.summary())

labelsToInclude = []

for y in range(34, 66):
    for x in range(14, 64):
        labelsToInclude.append(str(x) + ',' + str(y))

verticesToDelete = []

for v in g.vs:
    if v['name'] not in labelsToInclude:
        verticesToDelete.append(v.index)

g.delete_vertices(verticesToDelete)

print(g.summary())
