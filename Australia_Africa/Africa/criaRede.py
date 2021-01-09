# -*- coding: utf-8 -*-
''' Neste codigo, sao criadas redes para cada mes 
    considerando grids com celulas de 0.5 lat e 
    0.5 long (redes para serem comparadas com a Australia)
'''

import os
import math
import pandas as pd
from igraph import Graph

# diretorio para resultados e dados
rd = os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))
rd = rd + '/Resultados e Dados/Australia_Africa/Africa'

''' leitura dos arquivos '''

# fire_archive_M6_135342.csv contem dados de 2003-01-01 ate 2019-12-01
df = pd.read_csv(rd + r'/csv/fire_archive_M6_135342.csv')

# eventos contem apenas os dados com confiabilidade maior ou igual a 75%
ev = df.loc[df['confidence'] >= 75]
del df

eventos = pd.concat([ev], sort = True, ignore_index = True)
del ev

# apaga colunas para termos mais memoria
del eventos['instrument']
del eventos['brightness']
del eventos['scan']
del eventos['track']
del eventos['acq_time']
del eventos['satellite']
del eventos['version']
del eventos['bright_t31']
del eventos['frp']
del eventos['daynight']
del eventos['type']

# latitude varia de -12 a -8.07
lat_i = -12
lat_f = 8.07

# longitude varia de 14 a 34
long_i = 14
long_f = 34

# alpha eh a altura da celula do grid (latitude)
alpha = 0.5

# beta eh a largura da celula do grid (longitude)
beta = 0.5

# a eh o numero de posicoes na latitude
a = math.ceil( (lat_f - lat_i)/alpha )

# b eh o numero de posicoes na longitude
b = math.ceil( (long_f - long_i)/beta )

# recebe  a coordenada d e a componente x ou y e retorna o
# indice da celula correspondente
def indiceCelula(d, L):
    if L == 'x':
        c = math.floor( (d - long_i)/beta )
        if c >= b:
            return b - 1
        else:
            return c
    if L == 'y':
        c = math.floor( (d - lat_i)/alpha )
        if c >= a:
            return a - 1
        else:
            return c
    else: 
        return -1
    
# recebe o indice x da celula e retorna a longitude do seu centro
def centroIndiceLong(x):
    if x < 0 or x >= b:
        return -1
    else:
        return long_i + beta*(x + 0.5)
    
# recebe o indice y da celula e retorna a latitude do seu centro
def centroIndiceLat(y):
    if y < 0 or y >= a:
        return -1
    else:
        return lat_i + alpha*(y + 0.5)
    
# adiciona uma coluna para guardar a celula de cada evento no grid
celula = ['-1,-1'] * (eventos.index.max() + 1)
eventos['celula'] = celula
del celula

# percorre todas as linhas calculando a celula no grid do evento
for index_label, row_series in eventos.iterrows():
    x = row_series['longitude']
    y = row_series['latitude']
    cx = indiceCelula(x, 'x')
    cy = indiceCelula(y, 'y')
    c = str(cx) + ',' + str(cy)
    eventos.at[index_label, 'celula'] = c
del x, y, cx, cy, c

''' construcao dos grafos '''

# criacao da lista com nomes do vertices do grafos
nomesVertices = []
for i in range(a):
    for j in range(b):
        nome = str(j) + ',' + str(i)
        nomesVertices.append(nome)
        
# listas para longitude e latitude do centro de cada celula baseado no seu nome
longitudeCentro = []
for i in nomesVertices:
    long = i.split(',')[0]
    c = centroIndiceLong(float(long))
    longitudeCentro.append(c)

latitudeCentro = []
for i in nomesVertices:
    lat = i.split(',')[1]
    c = centroIndiceLat(float(lat))
    latitudeCentro.append(c)
    
del long, lat, c

# listas com datas e celulas do eventos
datas = [i for i in eventos['acq_date']]
celulas = [i for i in eventos['celula']]
del eventos

# dicionario com nome dos meses
meses = {
    "01" : "Jan",
    "02" : "Fev",
    "03" : "Mar",
    "04" : "Abr",
    "05" : "Mai",
    "06" : "Jun",
    "07" : "Jul",
    "08" : "Ago",
    "09" : "Set",
    "10" : "Out",
    "11" : "Nov",
    "12" : "Dez"
}

def mes(m):
    return meses[m]

N = len(celulas)
celulaAnterior = celulas[0]
g = Graph(a*b)
numGrafo = 1

dataAtual = datas[0].split('-')
dataGrafo = datas[0].split('-')
g.vs['name'] = nomesVertices
g.vs['longitude'] = longitudeCentro
g.vs['latitude'] = latitudeCentro

for i in range(1, N): # comeca no segundo evento
    dataAtual = datas[i].split('-') # divide em tres strings: ano, mes, dia
    if dataGrafo[1] != dataAtual[1]:
        # guarda algumas informacoes sobre o grafo
        g.vs['longitude'] = longitudeCentro
        g.vs['latitude'] = latitudeCentro
        g.write_gml(rd + r'/grafosMes/grafo' + str(numGrafo) + '_' + mes(dataGrafo[1]) + '-' + dataGrafo[0] + '.gml')
        numGrafo += 1
        del g
        dataGrafo = dataAtual
        g = Graph(a*b)
        g.vs['name'] = nomesVertices
    if celulas[i] != celulaAnterior and not g.are_connected(celulas[i], celulaAnterior):
        g.add_edge(celulas[i], celulaAnterior) # cria aresta
    celulaAnterior = celulas[i]
    if i == N-1:
        g.vs['longitude'] = longitudeCentro
        g.vs['latitude'] = latitudeCentro
        g.write_gml(rd + r'/grafosMes/grafo' + str(numGrafo) + '_' + mes(dataGrafo[1]) + '-' + dataGrafo[0] + '.gml')
        del g
        
''' criacao do dataframe com coordenadas de cada vertice '''
cv = {
      'vertice' : nomesVertices,
      'longitude' : longitudeCentro,
      'latitude' : latitudeCentro
}

# cria um dataframe com os dados do dicionario
coordenadasVertice = pd.DataFrame(cv)
del cv

# salva um arquivo com o dataframe
coordenadasVertice.to_csv(rd + r'/csv/coordenadasVertice.csv')