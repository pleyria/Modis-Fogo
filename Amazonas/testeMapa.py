import os
from igraph import Graph as gr
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# tamanho da imagem em polegadas
largura = 11.69
altura = 8.27
plt.figure(figsize=(largura, altura))


# seleciona a area, resolucao e tipo de projecao
mapa = Basemap(projection = 'cyl', resolution='i',
            llcrnrlat = -44, urcrnrlat = -10,
            llcrnrlon = 113, urcrnrlon = 154)
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

# divisoes do grid
a = 68 # numero de divisoes na latitude
b = 82 # numero de divisoes na longitude

# abre o grafo
rd = os.path.dirname(os.path.dirname(os.getcwd()))
rd = rd + '/Resultados e Dados/Australia'
grafo = gr.Read_GML(rd + '/LatLong05/grafosMes/grafo47_Nov-2006.gml')

# lista com longitudes dos vertices
longs = grafo.vs['longitude']

# lista com latitudes dos vertices
lats = grafo.vs['latitude']

# lista com dados dos vertices
dados = grafo.degree()

del grafo

# transforma lista de dadps em uma matriz
dados = np.array(dados)
dados = dados.reshape(a, b)

# gera as coordenadas das divisoes do grid
y = np.linspace(mapa.llcrnrlat, mapa.urcrnrlat, num = a)
x = np.linspace(mapa.llcrnrlon, mapa.urcrnrlon, num = b)

# transforma as listas de coordenadas em matrizes
xx, yy = np.meshgrid(x, y)

# plota os dados como cores
mapa.pcolormesh(xx, yy, dados, cmap = 'OrRd', latlon=True,
                zorder = 2, alpha = 0.5)

# titulo do mapa
plt.title('Graus dos vértices - Novembro 2006')
plt.show()

