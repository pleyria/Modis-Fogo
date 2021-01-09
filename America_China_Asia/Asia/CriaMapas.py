import os
import re
import numpy as np
from igraph import Graph as gr
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# funcao para ordenar nomes de arquivos
def ordenaNomesArquivos(f):
	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
	return sorted(f, key = alphanum_key)

# retorna a substring de s entre os separadores i e f
def substringEntreChars(s, i, f):
	sub = s[s.find(i)+1 : s.find(f)]
	return sub

# diretorio para resultados e dados
rd = os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))
rd = rd + '/Resultados e Dados/America_China_Asia/Asia'

# lista com os nomes dos grafos
f = os.listdir(rd + "/grafosMes")
# ordena os nomes cronologicamente
f = ordenaNomesArquivos(f)

# filtra apenas os grafos do intervalo desejado
s = []
for i in f:
    sub = substringEntreChars(i, '-', '.')
    if int(sub) < 2020:
        s.append(i)
f = s
del s, i

# tamanho da imagem em polegadas
h = 11.69
w = 8.27

# area da imagem
# latitude varia de 46.9 a 59
lat_i = 46.9
lat_f = 59

# longitude varia de 57 a 77
long_i = 57
long_f = 77

# divisoes do grid
a = 25 # numero de divisoes na latitude
b = 40 # numero de divisoes na longitude

# gera as coordenadas das divisoes do grid
y = np.linspace(lat_i, lat_f, num = a)
x = np.linspace(long_i, long_f, num = b)

# transforma as listas de coordenadas em matrizes
xx, yy = np.meshgrid(x, y)

numMapa = 0

# percorre os arquivos
for arquivo in f:
    ano = substringEntreChars(arquivo, '-', '.')
    mes = substringEntreChars(arquivo, '_', '-')
    
    # abre o grafo
    grafo = gr.Read_GML(rd + '/grafosMes/' + arquivo)
    
    # lista com longitudes dos vertices
    longs = grafo.vs['longitude']
    # lista com latitudes dos vertices
    lats = grafo.vs['latitude']
    # lista com dados dos vertices
    dados_degree = grafo.degree()
    dados_betweenness = grafo.betweenness()
    dados_closeness = grafo.closeness()
    
    del grafo
    
    # transforma as listas de dados em matrizes
    dados_degree = np.array(dados_degree)
    dados_degree = dados_degree.reshape(a, b)
    
    dados_betweenness = np.array(dados_betweenness)
    dados_betweenness = dados_betweenness.reshape(a, b)
    
    dados_closeness = np.array(dados_closeness)
    dados_closeness = dados_closeness.reshape(a, b)
    
    # plota degree

    plt.figure(figsize=(w, h))
    # seleciona a area, resolucao e tipo de projecao
    mapa = Basemap(projection = 'cyl', resolution='i',
                llcrnrlat = lat_i, urcrnrlat = lat_f,
                llcrnrlon = long_i, urcrnrlon = long_f)
    # desenha linhas dos continentes
    mapa.drawcoastlines(linewidth = 1.2, zorder = 2)
    # desenha linhas dos paises
    mapa.drawcountries(linewidth = 1.2, zorder = 2)
    # desenha linhas dos estados
    mapa.drawstates(linewidth = 0.5, zorder = 2)
    # cor dos continentes
    mapa.fillcontinents(color = '#c0f772', zorder = 1)
    # cor do oceano
    mapa.drawmapboundary(fill_color = '#49c4d1', zorder = 0)
    
    # plota os dados como cores
    mapa.pcolormesh(xx, yy, dados_degree, cmap = 'OrRd', latlon=True,
                    zorder = 2, alpha = 0.5)
    # escabala de cores
    cbar = plt.colorbar(orientation='horizontal', shrink=0.625, aspect=20, fraction=0.2,pad=0.02)
    cbar.set_label('Degree', size = 12)
    
    # titulo do mapa
    plt.title(mes + r'/' + ano, size = 15)
    
    # salva imagem
    plt.savefig(rd + '/Mapas/degree/' + ano + '/' + 
                'mapa' + str(numMapa % 12 + 1) + '_' + mes, bbox_inches='tight')
    plt.close()
    del dados_degree
    
    # plota betweenness
    
    plt.figure(figsize=(w, h))
    # seleciona a area, resolucao e tipo de projecao
    mapa = Basemap(projection = 'cyl', resolution='i',
                llcrnrlat = lat_i, urcrnrlat = lat_f,
                llcrnrlon = long_i, urcrnrlon = long_f)
    # desenha linhas dos continentes
    mapa.drawcoastlines(linewidth = 1.2, zorder = 2)
    # desenha linhas dos paises
    mapa.drawcountries(linewidth = 1.2, zorder = 2)
    # desenha linhas dos estados
    mapa.drawstates(linewidth = 0.5, zorder = 2)
    # cor dos continentes
    mapa.fillcontinents(color = '#c0f772', zorder = 1)
    # cor do oceano
    mapa.drawmapboundary(fill_color = '#49c4d1', zorder = 0)
    
    # plota os dados como cores
    mapa.pcolormesh(xx, yy, dados_betweenness, cmap = 'RdPu', latlon=True,
                    zorder = 2, alpha = 0.5)
    # escabala de cores
    cbar = plt.colorbar(orientation='horizontal', shrink=0.625, aspect=20, fraction=0.2,pad=0.02)
    cbar.set_label('Betweenness', size = 12)
    
    # titulo do mapa
    plt.title(mes + r'/' + ano, size = 15)
    
    # salva imagem
    plt.savefig(rd + '/Mapas/betweenness/' + ano + '/' + 
                'mapa' + str(numMapa % 12 + 1) + '_' + mes, bbox_inches='tight')
    plt.close()
    del dados_betweenness
    
    # plota betweenness
    
    plt.figure(figsize=(w, h))
    # seleciona a area, resolucao e tipo de projecao
    mapa = Basemap(projection = 'cyl', resolution='i',
                llcrnrlat = lat_i, urcrnrlat = lat_f,
                llcrnrlon = long_i, urcrnrlon = long_f)
    # desenha linhas dos continentes
    mapa.drawcoastlines(linewidth = 1.2, zorder = 2)
    # desenha linhas dos paises
    mapa.drawcountries(linewidth = 1.2, zorder = 2)
    # desenha linhas dos estados
    mapa.drawstates(linewidth = 0.5, zorder = 2)
    # cor dos continentes
    mapa.fillcontinents(color = '#c0f772', zorder = 1)
    # cor do oceano
    mapa.drawmapboundary(fill_color = '#49c4d1', zorder = 0)
    
    # plota os dados como cores
    mapa.pcolormesh(xx, yy, dados_closeness, cmap = 'YlOrBr', latlon=True,
                    zorder = 2, alpha = 0.5)
    # escabala de cores
    cbar = plt.colorbar(orientation='horizontal', shrink=0.625, aspect=20, fraction=0.2,pad=0.02)
    cbar.set_label('Closeness', size = 12)
    
    # titulo do mapa
    plt.title(mes + r'/' + ano, size = 15)
    
    # salva imagem
    plt.savefig(rd + '/Mapas/closeness/' + ano + '/' + 
                'mapa' + str(numMapa % 12 + 1) + '_' + mes, bbox_inches='tight')
    plt.close()
    del dados_closeness
    
    numMapa += 1
    