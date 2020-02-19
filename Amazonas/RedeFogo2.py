# -*- coding: utf-8 -*-
''' Neste codigo, sao criadas redes para cada mes '''
import os
import math
import pandas as pd
from igraph import Graph

# diretorio para resultados e dados
rd = os.path.dirname(os.path.dirname(os.getcwd()))
rd = rd + '/Resultados e Dados/Amazonas'

''' leitura dos arquivos '''

# fire_nrt_M6_94041.csv contem dados de 2019-10-01 ate 2019-12-01
df = pd.read_csv(rd + r'/csv/fire_archive_M6_94041.csv')
# eventos1 contem apenas os dados com confiabilidade maior ou igual a 75%
eventos1 = df.loc[df['confidence'] >= 75]
del df

# fire_archive_M6_94041.csv contem dados de 2003-01-01 ate 2019-09-30
df = pd.read_csv(rd + r'/csv/fire_nrt_M6_94041.csv')
# eventos2 contem apenas os dados com confiabilidade maior ou igual a 75%
eventos2 = df.loc[df['confidence'] >= 75]
del df

# eventos comtem a concatenacao de eventos1 e eventos2
eventos = pd.concat([eventos1, eventos2], sort = True, ignore_index = True)
del eventos1
del eventos2

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
# indice da celula correspondente
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
    
# recebe o indice da celula e retorna a coordenada do seu centro
def centroIndice(d, L):
    c = l*(d + 0.5)
    if L == 'x':
        c += long_i
    elif L == 'y':
        c += lat_i
    return c

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
		
# listas para longitude a latitude do centro de cada celula baseado no seu nome
longitudeCentro = []
for i in nomesVertices:
	long = i.split(',')[0]
	c = centroIndice(float(long), 'x')
	longitudeCentro.append(c)

latitudeCentro = []
for i in nomesVertices:
	lat = i.split(',')[1]
	c = centroIndice(float(lat), 'y')
	latitudeCentro.append(c)

# listas com datas e celulas dos eventos
datas = [x for x in eventos['acq_date']]
celulas = [x for x in eventos['celula']]
del eventos

# dicionario com nome de meses
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
g = Graph(n*n)
numGrafo = 1

dataAtual = datas[0].split('-') 
dataGrafo = datas[0].split('-')
g.vs['name'] = nomesVertices
g.vs['longitude'] = longitudeCentro
g.vs['latitude'] = latitudeCentro

for i in range(1, N): # comeca no segundo evento
	dataAtual = datas[i].split('-') # divide em tres strings: ano, mes, dia
	if dataGrafo[1] != dataAtual[1]:
		# guarda algumas infromacoes sobre o grafo
		g.vs['longitude'] = longitudeCentro
		g.vs['latitude'] = latitudeCentro
		g.write_gml(rd + '/grafosMes/grafo' + str(numGrafo) + "_" + mes(dataGrafo[1]) + '-'  + dataGrafo[0] + '.gml')
		numGrafo += 1
		del g
		dataGrafo = dataAtual
		g = Graph(n*n)
		g.vs['name'] = nomesVertices
	if celulas[i] != celulaAnterior and not g.are_connected(celulas[i], celulaAnterior):
		g.add_edge(celulas[i], celulaAnterior) # cria a aresta
	celulaAnterior = celulas[i]
	if i == N-1:
		g.vs['longitude'] = longitudeCentro
		g.vs['latitude'] = latitudeCentro
		g.write_gml(rd + '/grafosMes/grafo' + str(numGrafo) + "_" + mes(dataGrafo[1]) + '-'  + dataGrafo[0] + '.gml')
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
coordenadasVertice.to_csv(rd + "/csv/coordenadasVertice.csv")