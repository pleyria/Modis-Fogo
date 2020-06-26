import os
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

'''
    Programa para plotar uma area da Australia 
    para fazer testes com 1600 celulas
    
'''

# area da imagem
# latitude varia de -27 a -11
lat_i = -27
lat_f = -11

# longitude varia de 120 a 145
long_i = -120
long_f = -145

# diretorio para resultado
rd = os.path.dirname(os.getcwd())
rd = rd + '/Resultados e Dados'

# tamanho da imagem em polegadas
h = 11.69
w = 8.27

plt.figure(figsize=(w, h))
mapa = Basemap(projection='cyl',llcrnrlat=-27,urcrnrlat=-11,\
            llcrnrlon=120,urcrnrlon=145,resolution='i')
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

mapa.drawcoastlines()

plt.savefig(rd + '/mapa', bbox_inches='tight')

plt.show()

plt.close()