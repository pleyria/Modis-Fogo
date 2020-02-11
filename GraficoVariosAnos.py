# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# leitura do datraframe com dados dos grafos mensais
df = pd.read_csv(r'csv/dadosGrafosMensais.csv', index_col = 0)

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

# plot mean degree, mean betweenness, mean closeness, entropy
fig = plt.figure(figsize=(10,3))
plt.xticks(np.arange(0, 204, step = 12), anos)
plt.plot(mean_degree, label = 'Mean Degree')
plt.plot(mean_betweenness, label = 'Mean Betweenness')
plt.plot(mean_closeness, label = 'Mean Closeness')
plt.plot(entropy, label = 'Entropy')
plt.legend()
plt.tick_params(
    axis = 'x',
    which = 'both',
    top = False,
    bottom = False
)
plt.rc('xtick', labelsize = 10)
plt.title("Mean Degree")
plt.grid()
plt.savefig(r'Graficos2003-2019/4Medidas', dpi = 600, bbox_inches='tight')
plt.close()

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
plt.savefig(r'Graficos2003-2019/mean_degree', dpi = 600, bbox_inches='tight')
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
plt.savefig(r'Graficos2003-2019/mean_betweenness', dpi = 600, bbox_inches='tight')
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
plt.savefig(r'Graficos2003-2019/mean_closeness', dpi = 600, bbox_inches='tight')
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
plt.savefig(r'Graficos2003-2019/entropy', dpi = 600, bbox_inches='tight')
plt.close()
del entropy
