''' programa para criar mapas de casos de fogo do mundo '''
import numpy as np
import math
import os
import pandas as pd
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.colors as clr
from mpl_toolkits.basemap import Basemap

# estacao do ano plotada
# (so mudar aqui que ja muda o mapa)
estacao = 'JanFevMar'
# ano plotado
ano = '2019'

'''
periodos considerados:
JanFevMar
AbrMaiJun
JulAgoSet
OutNovDez
'''

# divisoes do grid
a = 360 # numero de divisoes na latitude (vertical)
b = 720 # numero de divisoes na longitude (horizontal)

# recebe a latitude (-90 a 90) de uma coordenada geografica e
# retorna o indice correpondente na matriz (0 a 359)
def lat2indice(coordenada):
    t = math.floor(coordenada*2 + 180)
    if t >= a:
        return t - 1
    return t

# recebe a longitude (-180 a 180) de uma coordenada geografica e 
# retorna o indice correspondente na matriz (0 a 719)
def long2indice(coordenada):
    t = math.floor(coordenada*2 + 360)
    if t  >= b:
        return t - 1
    return t


# matriz com casos de fogo de cada celula de dimensao a x b
matriz = np.zeros((a,b), dtype=int)

# diretorio do arquivo csv
rd = os.path.dirname(os.getcwd())
rd = rd + r'/Resultados e Dados/mundo'
# arquivo de 20 Marco a 21 Junho
df = pd.read_csv(rd + r'/csv/' + ano + r'/' + estacao + ano + r'.csv')

# apaga colunas inuteis
del df['instrument']
del df['brightness']
del df['scan']
del df['track']
del df['acq_time']
del df['satellite']
del df['version']
del df['bright_t31']
del df['frp']
del df['daynight']
del df['type']
del df['acq_date']

#eventos contem apenas os dados com confiabilidade maior ou igual a 75%
ev = df.loc[df['confidence'] >= 75]
del df
eventos = pd.concat([ev], sort = True, ignore_index = True)
del ev, eventos['confidence']

# listas com coordenadas geograficas
latitude = [i for i in eventos['latitude']]
longitude = [i for i in eventos['longitude']]
del eventos

# conta os casos de fogo e acumula na matriz de acordo 
# com as coordenadas
for i in range(len(latitude)):
    x = long2indice(longitude[i])
    y = lat2indice(latitude[i])
    matriz[y][x] = matriz[y][x] + 1

del latitude, longitude, x, y, i
matriz = matriz+1

# agora eh feito o uso da matriz para plotar o mapa

# tamanho da imagem (em polegadas)
h = 11.69
w = 8.27

# area da imagem
# latitude varia de -90 a 90
lat_i = -90
lat_f = 90

# longitude varia de -180 a 180
long_i = -180
long_f = 180

# gera as coordenadas das divisoes do grid
y = np.linspace(lat_i, lat_f, num = a)
x = np.linspace(long_i, long_f, num = b)

# transforma as listas de coordenadas em matrizes
xx, yy = np.meshgrid(x, y)

# plota o mapa
plt.figure(figsize=(w, h))
# seleciona a area, resolucao e tipo de projecao
mapa = Basemap(projection = 'mill', resolution='l',
            llcrnrlat = lat_i, urcrnrlat = lat_f,
            llcrnrlon = long_i, urcrnrlon = long_f)
# desenha linhas dos continentes
mapa.drawcoastlines(linewidth = 0.5, zorder = 1)
# desenha linhas dos paises
mapa.drawcountries(linewidth = 0.5, zorder = 1)
# desenha paralelos
# labels = [left,right,top,bottom]
paralelos = np.arange(-90.,91, 30.)
mapa.drawparallels(paralelos, labels=[True,False,False,False], linewidth=0.75)
# desenha meridianos
meridianos = np.arange(-180., 181, 60.)
mapa.drawmeridians(meridianos, labels=[False,False,False,True], linewidth=0.75)

# pontos para os retangulos das regioes
# pontos para a Africa
x_Africa = [14, 34, 34, 14, 14]
y_Africa = [-12, -12, 8.07, 8.07, -12]
# Pontos para a Australia
x_Australia = [125, 145.1, 145.1, 125, 125]
y_Australia = [-31.9, -31.9, -13.4, -13.4, -31.4]
# Pontos para a Amazonia
x_Amazonia = [-70, -50, -50, -70, -70]
y_Amazonia = [-15, -15, 5, 5, -15]
# Pontos para a America do norte
x_America = [-123.8, -103.8, -103.8, -123.8, -123.8]
y_America = [36.84, 36.84, 51.25, 51.25, 36.84]
# Pontos para o norte da China
x_China = [110.38, 130.38, 130.38, 110.38, 110.38]
y_China = [40.76, 40.76, 54.29, 54.29, 40.76]
# Pontos para o norte da Asia
x_Asia = [57, 77, 77, 57, 57]
y_Asia = [46.9, 46.9, 59, 59, 46.9]

# plot dos retangulos das regioes
# retangulo da Africa
mapa.plot(x_Africa, y_Africa, latlon=True, marker=None, 
          color='b', linewidth=0.85, linestyle='dashed')
# retangulo da Australia
mapa.plot(x_Australia, y_Australia, latlon=True, marker=None, 
          color='b', linewidth=0.85, linestyle='dashed')
# retangulo da Amazonia
mapa.plot(x_Amazonia, y_Amazonia, latlon=True, marker=None, 
          color='b', linewidth=0.85, linestyle='dashed')
# retangulo da America do norte
mapa.plot(x_America, y_America, latlon=True, marker=None, 
          color='b', linewidth=0.85, linestyle='dashed')
# retangulo do norte da china
mapa.plot(x_China, y_China, latlon=True, marker=None, 
          color='b', linewidth=0.85, linestyle='dashed')
# retangulo do norte da asia
mapa.plot(x_Asia, y_Asia, latlon=True, marker=None, 
          color='b', linewidth=0.85, linestyle='dashed')

del x_Africa, y_Africa, x_Australia, y_Australia, x_Amazonia, y_Amazonia
del x_America, y_America, x_China, y_China, x_Asia, y_Asia

'''
ESSA PARADA DE DIVIDIR EM INTERVALOS NAO DEU CERTO, MAS VOU DEIXAR 
AQUI DE RECORDACAO

# divide os dados em intervalos
# numero de intervalos pela formula de Sturges
C = 1 + 1.33*math.log10(a*b)
C = int(round(C))

# divisao dos intervalos
bounds = np.linspace(matriz.min(), matriz.max(), C+1)

# normalizacao por intervalos para o plot
intervalos = clr.BoundaryNorm(boundaries=bounds, ncolors=256)
'''

# normalizacao por logaritmo
normalizacao = clr.LogNorm(vmin=matriz.min(), vmax=matriz.max())

# criacao do colormap com menor valor branco
Reds = cm.get_cmap('Reds', 256)
newcolors = Reds(np.linspace(0, 1, 256))
white = np.array([1, 1, 1, 1])
newcolors[0] = white
newcmp = clr.ListedColormap(newcolors)

# plota os dados como cores
mapa.pcolormesh(xx, yy, matriz, cmap = newcmp, latlon=True, zorder=0,
                norm=normalizacao)

# escala de cores
cbar = plt.colorbar(orientation='horizontal', shrink=0.9, aspect=20, fraction=0.2,pad=0.02)
cbar.set_label('Fire counts', size = 14)

# salva imagem
plt.savefig(rd + r'/mapas/' + ano + r'/' + estacao + ano, bbox_inches='tight',
            dpi=300)

plt.show()
plt.close()
