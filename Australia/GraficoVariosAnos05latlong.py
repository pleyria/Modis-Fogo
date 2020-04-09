# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# diretorio para resultados e dados
rd = os.path.dirname(os.path.dirname(os.getcwd()))
rd = rd + '/Resultados e Dados/Australia'

# leitura do datraframe com dados dos grafos mensais
df = pd.read_csv(rd + r'/LatLong05/csv/dadosGrafosMensais.csv', index_col = 0)

# plot dos graficos

# lista com anos
anos = []
for a in range (2003, 2020):
    anos.append(str(a))

# listas com dados
mean_degree = [a for a in df['mean_degree']]
mean_betweenness = [a for a in df['mean_betweenness']]
mean_closeness = [a for a in df['mean_closeness']]
entropy = [a for a in df['entropy']]
vertices = [a for a in df['n_vertices']]
arestas = [a for a in df['n_arestas']]

# plot mean degree
fig = plt.figure(figsize=(10,3))
plt.xticks(np.arange(0, 204, step = 12), anos)
plt.plot(mean_degree)
plt.tick_params(
    axis = 'x',
    which = 'both',
    top = False,
    bottom = False
)
plt.rc('xtick', labelsize = 10)
plt.title("Mean Degree")
plt.grid()
plt.savefig(rd + r'/LatLong05/Graficos2003-2019/mean_degree', dpi = 300, bbox_inches='tight')
plt.close()
del mean_degree

# plot mean betweenness
fig = plt.figure(figsize=(10,3))
plt.xticks(np.arange(0, 204, step = 12), anos)
plt.plot(mean_betweenness)
plt.tick_params(
    axis = 'x',
    which = 'both',
    top = False,
    bottom = False
)
plt.rc('xtick', labelsize = 10)
plt.title("Mean Betweenness")
plt.grid()
plt.savefig(rd + r'/LatLong05/Graficos2003-2019/mean_betweenness', dpi = 300, bbox_inches='tight')
plt.close()
del mean_betweenness

# plot mean closeness
fig = plt.figure(figsize=(10,3))
plt.xticks(np.arange(0, 204, step = 12), anos)
plt.plot(mean_closeness)
plt.tick_params(
    axis = 'x',
    which = 'both',
    top = False,
    bottom = False
)
plt.rc('xtick', labelsize = 10)
plt.title("Mean Closeness")
plt.grid()
plt.savefig(rd + r'/LatLong05/Graficos2003-2019/mean_closeness', dpi = 300, bbox_inches='tight')
plt.close()
del mean_closeness

# plot entropy
fig = plt.figure(figsize=(10,3))
plt.xticks(np.arange(0, 204, step = 12), anos)
plt.plot(entropy)
plt.tick_params(
    axis = 'x',
    which = 'both',
    top = False,
    bottom = False
)
plt.rc('xtick', labelsize = 10)
plt.title("Entropy")
plt.grid()
plt.savefig(rd + r'/LatLong05/Graficos2003-2019/entropy', dpi = 300, bbox_inches='tight')
plt.close()
del entropy

# plot vertices
fig = plt.figure(figsize=(10,3))
plt.xticks(np.arange(0, 204, step = 12), anos)
plt.plot(vertices)
plt.tick_params(
    axis = 'x',
    which = 'both',
    top = False,
    bottom = False
)
plt.rc('xtick', labelsize = 10)
plt.title("Vertices")
plt.grid()
plt.savefig(rd + r'/LatLong05/Graficos2003-2019/vertices', dpi = 300, bbox_inches='tight')
plt.close()
del vertices

# plot arestas
fig = plt.figure(figsize=(10,3))
plt.xticks(np.arange(0, 204, step = 12), anos)
plt.plot(arestas)
plt.tick_params(
    axis = 'x',
    which = 'both',
    top = False,
    bottom = False
)
plt.rc('xtick', labelsize = 10)
plt.title("Arestas")
plt.grid()
plt.savefig(rd + r'/LatLong05/Graficos2003-2019/arestas', dpi = 300, bbox_inches='tight')
plt.close()
del arestas
