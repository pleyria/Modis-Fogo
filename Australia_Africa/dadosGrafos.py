# -*- coding: utf-8 -*-
''' Neste codigo, sao criados arquivos csv
    com media e variancia de degree, media de betweenness,
    media de closeness, entropia, numero de vertices e arestas
    para as redes mensais da Australia e Africa
'''

import os
import math
import pandas as pd
import re
from igraph import Graph

# conta quantos elementos k tem na lista l
def countLista(l, k):
    count = 0
    for i in l:
        if i == k:
            count += 1
    return count

# probabilidade de escolher aleatoriamente um vertice com grau k no grafo g
def probGrau(g, k):
    return countLista(g.degree(), k)/g.vcount()

# entropia do grafo
def entropia(g):
    N = g.vcount()
    graus = g.degree()
    grauMax = max(graus)
    H = 0
    for i in range (grauMax + 1):
        p = probGrau(g, i)
        if p > 0:
            H += p * math.log10(p)/math.log10(N)
    return -H

# retorna a soma de todos os elementos de uma lista
def somaLista(l):
	s = 0
	for i in l:
		s += i
	return s

# retorna a substring de s entre os separadores i e f
def substringEntreChars(s, i, f):
	sub = s[s.find(i)+1 : s.find(f)]
	return sub

# funcao para ordenar nomes de arquivos
def ordenaNomesArquivos(f):
	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
	return sorted(f, key = alphanum_key)

# dicionario para criar o dataframe
dados = {                      
	'ano' : [],                                                            
	'mes' : [],
	'mean_degree' : [],
    'variance_degree' : [],
	'mean_betweenness' : [],
	'mean_closeness' : [],
	'entropy' : [],
    'n_vertices' : [],                                                                                                                                                                                                                 
    'n_arestas' : [],
    'regiao' : []
}

# diretorio para resultados e dados
rd = os.path.dirname(os.path.dirname(os.getcwd()))
rdAf = rd + '/Resultados e Dados/Australia_Africa/Africa'
rdAu = rd + '/Resultados e Dados/Australia_Africa/Australia'

# leitura dos arquivos gml dos grafos da Africa
fAf = os.listdir(rdAf + "/grafosMes") # lista com os nomes dos grafos
fAf = ordenaNomesArquivos(fAf) # ordena os nomes cronologicamente

# leitura dos arquivos gml dos grafos da Australia
fAu = os.listdir(rdAu + "/grafosMes") # lista com os nomes dos grafos
fAu = ordenaNomesArquivos(fAu) # ordena os nomes cronologicamente

# obtencao dos dados da Africa
for arquivo in fAf: # percorre todos os grafos mensais em ordem
    # guarda o ano do grafo
    A = substringEntreChars(arquivo, '-', '.')
    dados['ano'].append(A)
    
    # guarda o mes do grafo
    M = substringEntreChars(arquivo, '_', '-')
    dados['mes'].append(M) # guarda mes do grafo
    
    # guarda a regiao do grafo
    dados['regiao'].append(0) # 0 -> Africa
    
    # abre o grafo
    g = Graph.Read_GML(rdAf + "/grafosMes/" + arquivo)
    
    # calculo e armazenamento do grau medio
    listaDado = g.degree() # listaDado contem os graus
    dado = somaLista(listaDado)/len(listaDado) # dado contem a media
    dados['mean_degree'].append(dado)

    # calculo e armazenamento da variancia do grau
    var = sum((i - dado) ** 2 for i in listaDado) / len(listaDado)
    dados['variance_degree'].append(var)
    del var

    # calculo e armazenamento da betweenness media
    listaDado = g.betweenness()
    dado = somaLista(listaDado)/len(listaDado)
    dados['mean_betweenness'].append(dado)

    # calculo e armazenamento da closeness media
    listaDado = g.closeness()
    dado = somaLista(listaDado)/len(listaDado)
    dados['mean_closeness'].append(dado)

    # calculo e armazenamento da entropia normalizada
    dado = entropia(g)
    dados['entropy'].append(dado)

    # calculo e armazenamento do numero de vertices
    v = g.degree()
    dado = 0
    for i in v:
        if i > 0:
            dado += 1
    dados['n_vertices'].append(dado)
    
    # calculo e armazenamento do numero de arestas
    dado = g.ecount()
    dados['n_arestas'].append(dado)
    
    del g


# obtencao dos dados da Australia
for arquivo in fAu: # percorre todos os grafos mensais em ordem
    # guarda o ano do grafo
    A = substringEntreChars(arquivo, '-', '.')
    dados['ano'].append(A)
    
    # guarda o mes do grafo
    M = substringEntreChars(arquivo, '_', '-')
    dados['mes'].append(M) # guarda mes do grafo
    
    # guarda a regiao do grafo
    dados['regiao'].append(1) # 1 -> Australia
    
    # abre o grafo
    g = Graph.Read_GML(rdAu + "/grafosMes/" + arquivo)
    
    # calculo e armazenamento do grau medio
    listaDado = g.degree() # listaDado contem os graus
    dado = somaLista(listaDado)/len(listaDado) # dado contem a media
    dados['mean_degree'].append(dado)

    # calculo e armazenamento da variancia do grau
    var = sum((i - dado) ** 2 for i in listaDado) / len(listaDado)
    dados['variance_degree'].append(var)
    del var

    # calculo e armazenamento da betweenness media
    listaDado = g.betweenness()
    dado = somaLista(listaDado)/len(listaDado)
    dados['mean_betweenness'].append(dado)

    # calculo e armazenamento da closeness media
    listaDado = g.closeness()
    dado = somaLista(listaDado)/len(listaDado)
    dados['mean_closeness'].append(dado)

    # calculo e armazenamento da entropia normalizada
    dado = entropia(g)
    dados['entropy'].append(dado)

    # calculo e armazenamento do numero de vertices
    v = g.degree()
    dado = 0
    for i in v:
        if i > 0:
            dado += 1
    dados['n_vertices'].append(dado)
    
    # calculo e armazenamento do numero de arestas
    dado = g.ecount()
    dados['n_arestas'].append(dado)
    
    del g
    
# cria um dataframe com os dados do dicionario
dadosGrafos = pd.DataFrame(dados)
del dados

# salva um arquivo com o dataframe
dadosGrafos.to_csv(rd + "/Resultados e Dados/Australia_Africa/dadosGrafos.csv")