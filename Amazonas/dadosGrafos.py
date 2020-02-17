# -*- coding: utf-8 -*-
import os
import re
import math
import pandas as pd
from igraph import Graph
import matplotlib.pyplot as plt

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
	'mean_betweenness' : [],
	'mean_closeness' : [],
	'entropy' : [],
     'n_vertices' : [],
     'n_arestas' : []
}

''' leitura dos arquivos e criacao do dataframe '''

f = os.listdir("grafosMes") # lista com os nomes dos grafos
f = ordenaNomesArquivos(f) # ordena os nomes cronologicamente

for arquivo in f: # percorre todos os grafos mensais em ordem
    # guarda o ano do grafo
    A = substringEntreChars(arquivo, '-', '.')
    dados['ano'].append(A)
    
    # guarda o mes do grafo
    M = substringEntreChars(arquivo, '_', '-')
    dados['mes'].append(M) # guarda mes do grafo
    
    # abre o grafo
    g = Graph.Read_GML("grafosMes/" + arquivo)
    
    # calculo e armazenamento do grau medio
    listaDado = g.degree()
    dado = somaLista(listaDado)/len(listaDado)
    dados['mean_degree'].append(dado)

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
dadosGrafos.to_csv("csv/dadosGrafosMensais.csv")

''' plots dos graficos '''

# plots de cada ano
for a in range (2003, 2020):
	ano = str(a) # ano para plotar
	dadosAno = dadosGrafos.loc[dadosGrafos['ano'] == ano] # dataframe do ano
	
	# listas com os dados do ano
	m = [a for a in dadosAno['mes']]
	mean_degree = [a for a in dadosAno['mean_degree']]
	mean_betweenness = [a for a in dadosAno['mean_betweenness']]
	mean_closeness = [a for a in dadosAno['mean_closeness']]
	entropy = [a for a in dadosAno['entropy']]
	
	# plot degree
	plt.plot(m, mean_degree)
	plt.title("mean degree " + ano)
	plt.savefig("GraficosAno/" + ano + "/mean_degree", dpi = 600)
	plt.close()
	
	# plot betweenness
	plt.plot(m, mean_betweenness)
	plt.title("mean betweenness " + ano)
	plt.savefig("GraficosAno/" + ano + "/mean_betweenness", dpi = 600)
	plt.close()
	
	# plot closeness
	plt.plot(m, mean_closeness)
	plt.title("mean closeness " + ano)
	plt.savefig("GraficosAno/" + ano + "/mean_closenness", dpi = 600)
	plt.close()
	
	# plot entropy
	plt.plot(m, entropy)
	plt.title("entropy " + ano)
	plt.savefig("GraficosAno/" + ano + "/entropy", dpi = 600)
	plt.close()


