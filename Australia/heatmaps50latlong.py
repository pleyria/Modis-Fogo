# -*- coding: utf-8 -*-
import os
import re
import numpy as np
import math
import scipy
from igraph import Graph
import seaborn as sns
import matplotlib.pyplot as plt

# diretorio para resultados e dados
rd = os.path.dirname(os.path.dirname(os.getcwd()))
rd = rd + '/Resultados e Dados/Australia'

# funcao para ordenar nomes de arquivos
def ordenaNomesArquivos(f):
	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
	return sorted(f, key = alphanum_key)

# transforma uma lista 2d em 1d
def total2d(v):
    # V e uma copia de v
    V = []
    for i in v:
        V.append(i.copy())

    total = []
    for i in v:
        for j in i:
            total.append(j)
    del V
    return total

# normaliza uma lista 2d com o zscore aplicado em cada sublista
def zscore2d(v, total):
    # V e uma copia de v
    V = []
    for i in v:
        V.append(i.copy())
        
    z = scipy.stats.zscore(total)
    
    c = 0
    for i in V:
        for j in range(len(i)):
            i[j] = z[c]
            c += 1
    return V

# normaliza uma lista 2d com a equacao do min max aplicada em cada sublista
def minMax2d(v, total):
    # V e uma copia de v
    V = []
    for i in v:
        V.append(i.copy())
    
    M = max(total)
    m = min(total)
    d = M - m
    
    for i in V:
        for j in range(len(i)):
            i[j] = (i[j] - m)/d
    return V

# normaliza uma lista 2d com raiz quadrada
def sqrt2d(v):
    # V e uma copia de v
    V = []
    for i in v:
        V.append(i.copy())
    
    for i in V:
        for j in range(len(i)):
            i[j] = math.sqrt(i[j])
    return V

# normaliza uma lista 2d com logaritmo
def log2d(v):
    # V e uma copia de v
    V = []
    for i in v:
        V.append(i.copy())
        
    for i in V:
        for j in range(len(i)):
            if i[j] > 0:
                i[j] = math.log10(i[j])
    return V

# lista com os nomes dos grafos
f = os.listdir(rd + "/LatLong05/grafosMes")
# ordena os nomes cronologicamente
f = ordenaNomesArquivos(f)

# listas para os dados dos grafos
deg = []
bet = []
clo = []

# obtencao dos dados dos grafos
for arquivo in f:
    # abre o grafo mensal
    g = Graph.Read_GML(rd + "/LatLong05/grafosMes/" + arquivo)
    # obtem as informacoes de todos os vertices
    deg.append(g.degree())
    bet.append(g.betweenness())
    clo.append(g.closeness())
    del g
del f

# dados normalizados

# totais
t_deg = total2d(deg)
t_bet = total2d(bet)
t_clo = total2d(clo)

# zscores
z_deg = zscore2d(deg, t_deg)
z_bet = zscore2d(bet, t_bet)
z_clo = zscore2d(clo, t_clo)

# minMax
mm_deg = minMax2d(deg, t_deg)
mm_bet = minMax2d(bet, t_bet)
mm_clo = minMax2d(clo, t_clo)
del t_deg
del t_bet
del t_clo

# sqrt
sqrt_deg = sqrt2d(deg)
sqrt_bet = sqrt2d(bet)
sqrt_clo = sqrt2d(clo)

# log
log_deg = log2d(deg)
log_bet = log2d(bet)
log_clo = log2d(clo)

# lista com anos
anos = []
for a in range (2003, 2020):
    anos.append(str(a))
    
# lista com vertices
a = 68
b = 82
vertices = []
for i in range (0, a*b, b):
    vertices.append(i)
del a, b

# dimensoes para a figura (polegadas)
X = 17.535433
Y = 8.26772

''' plot robust '''

# degree heatmap
plt.figure(figsize = (X,Y))
mapa = sns.heatmap(deg, cmap="Greens", robust = True)
plt.yticks(np.arange(0, 204, step = 12), anos)
plt.xticks(vertices, vertices)
plt.title("Degree")
plt.ylabel("Meses")
plt.xlabel("Vértices")
plt.grid()
imagem = mapa.get_figure()
imagem.savefig(rd + "/LatLong05/heatmaps/robust/heatmap_degree_robust.png", dpi = 300, bbox_inches='tight')
plt.close()

# betweenness heatmap
plt.figure(figsize = (X,Y))
mapa = sns.heatmap(bet, cmap="Greens", robust = True)
plt.yticks(np.arange(0, 204, step = 12), anos)
plt.xticks(vertices, vertices)
plt.title("Betweenness")
plt.ylabel("Meses")
plt.xlabel("Vértices")
plt.grid()
imagem = mapa.get_figure()
imagem.savefig(rd + "/LatLong05/heatmaps/robust/heatmap_betweenness_robust.png", dpi = 300, bbox_inches='tight')
plt.close()

# closeness heatmap
plt.figure(figsize = (X,Y))
mapa = sns.heatmap(clo, cmap="Greens", robust = True)
plt.yticks(np.arange(0, 204, step = 12), anos)
plt.xticks(vertices, vertices)
plt.title("Closeness")
plt.ylabel("Meses")
plt.xlabel("Vértices")
plt.grid()
imagem = mapa.get_figure()
imagem.savefig(rd + "/LatLong05/heatmaps/robust/heatmap_closeness_robust.png", dpi = 300, bbox_inches='tight')
plt.close()

print('robust')

''' plots sem normalizacao '''

# degree heatmap
plt.figure(figsize = (X,Y))
mapa = sns.heatmap(deg, cmap="Greens")
plt.yticks(np.arange(0, 204, step = 12), anos)
plt.xticks(vertices, vertices)
plt.title("Degree")
plt.ylabel("Meses")
plt.xlabel("Vértices")
plt.grid()
imagem = mapa.get_figure()
imagem.savefig(rd + "/LatLong05/heatmaps/semNormalizacao/heatmap_degree.png", dpi = 300, bbox_inches='tight')
plt.close()
del deg

# betweenness heatmap
plt.figure(figsize = (X,Y))
mapa = sns.heatmap(bet, cmap="Greens")
plt.yticks(np.arange(0, 204, step = 12), anos)
plt.xticks(vertices, vertices)
plt.title("Betweenness")
plt.ylabel("Meses")
plt.xlabel("Vértices")
plt.grid()
imagem = mapa.get_figure()
imagem.savefig(rd + "/LatLong05/heatmaps/semNormalizacao/heatmap_betweenness.png", dpi = 300, bbox_inches='tight')
plt.close()
del bet

# closeness heatmap
plt.figure(figsize = (X,Y))
mapa = sns.heatmap(clo, cmap="Greens")
plt.yticks(np.arange(0, 204, step = 12), anos)
plt.xticks(vertices, vertices)
plt.title("Closeness")
plt.ylabel("Meses")
plt.xlabel("Vértices")
plt.grid()
imagem = mapa.get_figure()
imagem.savefig(rd + "/LatLong05/heatmaps/semNormalizacao/heatmap_closeness.png", dpi = 300, bbox_inches='tight')
plt.close()
del clo

print('sem')

''' plots zscore '''

# degree heatmap
plt.figure(figsize = (X,Y))
mapa = sns.heatmap(z_deg, cmap="Greens")
plt.yticks(np.arange(0, 204, step = 12), anos)
plt.xticks(vertices, vertices)
plt.title("Degree")
plt.ylabel("Meses")
plt.xlabel("Vértices")
plt.grid()
imagem = mapa.get_figure()
imagem.savefig(rd + "/LatLong05/heatmaps/zscore/heatmap_degree_zscore.png", dpi = 300, bbox_inches='tight')
plt.close()
del z_deg

# betweenness heatmap
plt.figure(figsize = (X,Y))
mapa = sns.heatmap(z_bet, cmap="Greens")
plt.yticks(np.arange(0, 204, step = 12), anos)
plt.xticks(vertices, vertices)
plt.title("Betweenness")
plt.ylabel("Meses")
plt.xlabel("Vértices")
plt.grid()
imagem = mapa.get_figure()
imagem.savefig(rd + "/LatLong05/heatmaps/zscore/heatmap_betweenness_zscore.png", dpi = 300, bbox_inches='tight')
plt.close()
del z_bet

# closeness heatmap
plt.figure(figsize = (X,Y))
mapa = sns.heatmap(z_clo, cmap="Greens")
plt.yticks(np.arange(0, 204, step = 12), anos)
plt.xticks(vertices, vertices)
plt.title("Closeness")
plt.ylabel("Meses")
plt.xlabel("Vértices")
plt.grid()
imagem = mapa.get_figure()
imagem.savefig(rd + "/LatLong05/heatmaps/zscore/heatmap_closeness_zscore.png", dpi = 300, bbox_inches='tight')
plt.close()
del z_clo

print('z')

''' plot minmax '''

# degree heatmap
plt.figure(figsize = (X,Y))
mapa = sns.heatmap(mm_deg, cmap="Greens")
plt.yticks(np.arange(0, 204, step = 12), anos)
plt.xticks(vertices, vertices)
plt.title("Degree")
plt.ylabel("Meses")
plt.xlabel("Vértices")
plt.grid()
imagem = mapa.get_figure()
imagem.savefig(rd + "/LatLong05/heatmaps/minmax/heatmap_degree_minmax.png", dpi = 300, bbox_inches='tight')
plt.close()
del mm_deg

# betweenness heatmap
plt.figure(figsize = (X,Y))
mapa = sns.heatmap(mm_bet, cmap="Greens")
plt.yticks(np.arange(0, 204, step = 12), anos)
plt.xticks(vertices, vertices)
plt.title("Betweenness")
plt.ylabel("Meses")
plt.xlabel("Vértices")
plt.grid()
imagem = mapa.get_figure()
imagem.savefig(rd + "/LatLong05/heatmaps/minmax/heatmap_betweenness_minmax.png", dpi = 300, bbox_inches='tight')
plt.close()
del mm_bet

# closeness heatmap
plt.figure(figsize = (X,Y))
mapa = sns.heatmap(mm_clo, cmap="Greens")
plt.yticks(np.arange(0, 204, step = 12), anos)
plt.xticks(vertices, vertices)
plt.title("Closeness")
plt.ylabel("Meses")
plt.xlabel("Vértices")
plt.grid()
imagem = mapa.get_figure()
imagem.savefig(rd + "/LatLong05/heatmaps/minmax/heatmap_closeness_minmax.png", dpi = 300, bbox_inches='tight')
plt.close()
del mm_clo

print('mm')

''' plot sqrt '''

# degree heatmap
plt.figure(figsize = (X,Y))
mapa = sns.heatmap(sqrt_deg, cmap="Greens")
plt.yticks(np.arange(0, 204, step = 12), anos)
plt.xticks(vertices, vertices)
plt.title("Degree")
plt.ylabel("Meses")
plt.xlabel("Vértices")
plt.grid()
imagem = mapa.get_figure()
imagem.savefig(rd + "/LatLong05/heatmaps/sqrt/heatmap_degree_sqrt.png", dpi = 300, bbox_inches='tight')
plt.close()
del sqrt_deg

# betweenness heatmap
plt.figure(figsize = (X,Y))
mapa = sns.heatmap(sqrt_bet, cmap="Greens")
plt.yticks(np.arange(0, 204, step = 12), anos)
plt.xticks(vertices, vertices)
plt.title("Betweenness")
plt.ylabel("Meses")
plt.xlabel("Vértices")
plt.grid()
imagem = mapa.get_figure()
imagem.savefig(rd + "/LatLong05/heatmaps/sqrt/heatmap_betweenness_sqrt.png", dpi = 300, bbox_inches='tight')
plt.close()
del sqrt_bet

# closeness heatmap
plt.figure(figsize = (X,Y))
mapa = sns.heatmap(sqrt_clo, cmap="Greens")
plt.yticks(np.arange(0, 204, step = 12), anos)
plt.xticks(vertices, vertices)
plt.title("Closeness")
plt.ylabel("Meses")
plt.xlabel("Vértices")
imagem = mapa.get_figure()
plt.grid()
imagem.savefig(rd + "/LatLong05/heatmaps/sqrt/heatmap_closeness_sqrt.png", dpi = 300, bbox_inches='tight')
plt.close()
del sqrt_clo

print('sqrt')

''' plot log '''

# degree heatmap
plt.figure(figsize = (X,Y))
mapa = sns.heatmap(log_deg, cmap="Greens")
plt.yticks(np.arange(0, 204, step = 12), anos)
plt.xticks(vertices, vertices)
plt.title("Degree")
plt.ylabel("Meses")
plt.xlabel("Vértices")
plt.grid()
imagem = mapa.get_figure()
imagem.savefig(rd + "/LatLong05/heatmaps/log/heatmap_degree_log.png", dpi = 300, bbox_inches='tight')
plt.close()
del log_deg

# betweenness heatmap
plt.figure(figsize = (X,Y))
mapa = sns.heatmap(log_bet, cmap="Greens")
plt.yticks(np.arange(0, 204, step = 12), anos)
plt.xticks(vertices, vertices)
plt.title("Betweenness")
plt.ylabel("Meses")
plt.xlabel("Vértices")
plt.grid()
imagem = mapa.get_figure()
imagem.savefig(rd + "/LatLong05/heatmaps/log/heatmap_betweenness_log.png", dpi = 300, bbox_inches='tight')
plt.close()
del log_bet

# closeness heatmap
plt.figure(figsize = (X,Y))
mapa = sns.heatmap(log_clo, cmap="Greens")
plt.yticks(np.arange(0, 204, step = 12), anos)
plt.xticks(vertices, vertices)
plt.title("Closeness")
plt.ylabel("Meses")
plt.xlabel("Vértices")
plt.grid()
imagem = mapa.get_figure()
imagem.savefig(rd + "/LatLong05/heatmaps/log/heatmap_closeness_log.png", dpi = 300, bbox_inches='tight')
plt.close()
del log_clo

print('log')
