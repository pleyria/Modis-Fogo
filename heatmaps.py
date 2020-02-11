# -*- coding: utf-8 -*-
import os
import re
import numpy as np
from igraph import Graph
import seaborn as sns
import matplotlib.pyplot as plt

# funcao para ordenar nomes de arquivos
def ordenaNomesArquivos(f):
	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
	return sorted(f, key = alphanum_key)

# lista com os nomes dos grafos
f = os.listdir("grafosMes")
# ordena os nomes cronologicamente
f = ordenaNomesArquivos(f)

# listas para os dados dos grafos
deg = []
bet = []
clo = []

# obtencao dos dados dos grafos
for arquivo in f:
    # abre o grafo mensal
    g = Graph.Read_GML("grafosMes/" + arquivo)
    # obtem as informacoes de todos os vertices
    deg.append(g.degree())
    bet.append(g.betweenness())
    clo.append(g.closeness())
    del g

# lista com anos
anos = []
for a in range (2003, 2020):
    anos.append(str(a))

# degree heatmap
mapa = sns.heatmap(deg, cmap="Greens", xticklabels = False)
plt.yticks(np.arange(0, 204, step = 12), anos)
plt.title("Degree")
plt.ylabel("Meses")
plt.xlabel("Vértices (total = 900)")
plt.grid()
imagem = mapa.get_figure()
imagem.savefig("heatmaps/heatmap_degree.png", dpi = 600, bbox_inches='tight')
plt.close()
del deg

# betweenness heatmap
mapa = sns.heatmap(bet, cmap="Greens", xticklabels = False)
plt.yticks(np.arange(0, 204, step = 12), anos)
plt.title("Betweenness")
plt.ylabel("Meses")
plt.xlabel("Vértices (total = 900)")
plt.grid()
imagem = mapa.get_figure()
imagem.savefig("heatmaps/heatmap_betweenness.png", dpi = 600, bbox_inches='tight')
plt.close()
del bet

# closeness heatmap
mapa = sns.heatmap(clo, cmap="Greens", xticklabels = False)
plt.yticks(np.arange(0, 204, step = 12), anos)
plt.title("Closeness")
plt.ylabel("Meses")
plt.xlabel("Vértices (total = 900)")
plt.grid()
imagem = mapa.get_figure()
imagem.savefig("heatmaps/heatmap_closeness.png", dpi = 600, bbox_inches='tight')
plt.close()
del clo
