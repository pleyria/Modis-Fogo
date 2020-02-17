# -*- coding: utf-8 -*-

import math
import numpy as np
import pandas as pd
from igraph import *
from igraph import Graph

''' leitura dos arquivos '''

# fire_nrt_M6_94041.csv contem dados de 2019-10-01 ate 2019-12-01
df = pd.read_csv(r'csv\fire_archive_M6_94041.csv')
# eventos1 contem apenas os dados com confiabilidade maior ou igual a 75%
eventos1 = df.loc[df['confidence'] >= 75]
del df

# fire_archive_M6_94041.csv contem dados de 2003-01-01 ate 2019-09-30
df = pd.read_csv(r'csv\fire_nrt_M6_94041.csv')
# eventos2 contem apenas os dados com confiabilidade maior ou igual a 75%
eventos2 = df.loc[df['confidence'] >= 75]
del df

# eventos comtem a concatenacao de eventos1 e eventos2
eventos = pd.concat([eventos1, eventos2], sort = True, ignore_index = True)
del eventos1
del eventos2

del eventos['instrument'] # apaga coluna para termos mais memoria

''' calculo das celulas do grid '''

# latitude varia de -15 a 5
lat_i = -15
lat_f = 5

# longitude varia de -70 a -50
long_i = -70
long_f = -50

# estudamos uma area quadrada de 20x20
# divimos a area em um grid 30x30 
n = 30
# cada celula do grid eh um quadrado de lado l
l = (lat_f - lat_i)/n

# recebe a coordenada d e a componente x ou y e retorna o 
# indice da celula correspondente '''
def indiceCelula(d, L):
    if L == 'x':
        c = math.floor( (d - long_i)/l )
        if c >= n:
            return n - 1
        else:
            return c
    if L == 'y':
        c = math.floor( (d - lat_i)/l )
        if c >= n:
            return n - 1
        else:
            return c
    else:
        return -1

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

''' construcao dos grafos '''

# criacao da lista com os nomes dos vertices dos grafos
nomesVertices = []
for i in range(n):
    for j in range(n):
        nome = str(j) + ',' + str(i)
        nomesVertices.append(nome)

# listas com datas e celulas dos eventos
datas = [x for x in eventos['acq_date']]
celulas = [x for x in eventos['celula']]
del eventos

N = len(celulas)
dataAtual = datas[0]
celulaAnterior = celulas[0]
numDias = 1
numGrafo = 1

g = Graph(n*n)
g.vs['name'] = nomesVertices

for i in range(1, N): # comeca no segundo evento
    if datas[i] != dataAtual: 
        dataAtual = datas[i]
        numDias += 1 # aumenta um na contagem de dias
        if numDias == 30: # salva o grafo apos 30 dias
            g.write_gml("grafos\grafo" + str(numGrafo) + ".gml")
            numGrafo += 1
            numDias = 1
            del g
            g = Graph(n*n)
            g.vs['name'] = nomesVertices
			continue
    if celulas[i] != celulaAnterior:
        g.add_edge(celulas[i], celulaAnterior) # cria a aresta
    celulaAnterior = celulas[i]
    if i == N-1: # salva o ultimo grafo
        g.write_gml("grafos\grafo" + str(numGrafo) + ".gml")
        del g

