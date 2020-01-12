# -*- coding: utf-8 -*-
import os
import re
import pandas as pd
from igraph import Graph
import matplotlib.pyplot as plt

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
	'mean_entropy' : []
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
	# pega o maior componente conexo
	largest = g.clusters().giant()
	del g
	
	# calculo e armazenamento do grau medio
	listaDado = largest.degree()
	dado = somaLista(listaDado)/len(listaDado)
	dados['mean_degree'].append(dado)
	
	# calculo e armazenamento da betweenness media
	listaDado = largest.betweenness()
	dado = somaLista(listaDado)/len(listaDado)
	dados['mean_betweenness'].append(dado)
	
	# calculo e armazenamento da closeness media
	listaDado = largest.closeness()
	dado = somaLista(listaDado)/len(listaDado)
	dados['mean_closeness'].append(dado)
	
	# calculo e armazenamento da entropia normalizada media
	listaDado = largest.diversity()
	dado = somaLista(listaDado)/len(listaDado)
	dados['mean_entropy'].append(dado)
	
	del largest
	
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
	mean_entropy = [a for a in dadosAno['mean_entropy']]
	
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
	plt.plot(m, mean_entropy)
	plt.title("mean entropy " + ano)
	plt.savefig("GraficosAno/" + ano + "/mean_entropy", dpi = 600)
	plt.close()

''' criacao do dataframe com coordenadas de cada vertice '''

