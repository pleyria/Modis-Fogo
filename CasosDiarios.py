# -*- coding: utf-8 -*-

'''
listar os numeros de casos diarios para:
    -Africa
    -Australia
    -Amazonia
    -America do norte
    -China
    -Asia
'''

import os
import pandas as pd
from datetime import timedelta, date

# funcao que retorna um gerador de datas
def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

rd = os.path.dirname(os.getcwd())
rd = rd + r'/Resultados e Dados/'

# diretorios com o csv de ocorrencia de fogo de cada regiao
rdAf = rd + r'Australia_Africa/Africa/csv/fire_archive_M6_135342.csv'
rdAu = rd + r'Australia_Africa/Australia/csv/fire_archive_M6_135341.csv'
rdAm = rd + r'Amazonas/csv/fire_unico.csv'
rdAn = rd + r'America_China_Asia/America/csv/fire_archive_M6_146856.csv'
rdCh = rd + r'America_China_Asia/China/csv/fire_archive_M6_146857.csv'
rdAs = rd + r'America_China_Asia/Asia/csv/fire_archive_M6_146858.csv'
caminhos = [rdAf, rdAu, rdAm, rdAn, rdCh, rdAs]
regioes = ['Africa', 'Australia', 'Amazonia', 'AmericaNorte', 'China', 'Asia']

# gera uma lista com os nomes das datas estudadas
datas = []
start_dt = date(2003, 1, 1)
end_dt = date(2019, 12, 1)
for dt in daterange(start_dt, end_dt):
    datas.append(dt.strftime("%Y-%m-%d"))

# conta os eventos e gera os vetores
k = 0
for i in caminhos:
    df = pd.read_csv(i)
    ev = df.loc[df['confidence'] >= 75]
    del df
    eventos = pd.concat([ev], sort = True, ignore_index = True)
    del ev
    ev = [i for i in eventos['acq_date']]
    del eventos
    casosDiarios = []
    c = 0
    for j in datas:
        casosDiarios.append(ev.count(j))
    Casos = pd.DataFrame(casosDiarios)
    del casosDiarios
    Casos.to_csv(rd + r'casos diarios/Casos' + regioes[k], index=False)
    del Casos
    k = k + 1

