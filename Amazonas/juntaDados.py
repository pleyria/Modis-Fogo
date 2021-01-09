# -*- coding: utf-8 -*-
"""
Arquivo para juntar os dois csv com os dados da amazonia
"""

import os
import pandas as pd

# diretorio para resultados e dados
rd = os.path.dirname(os.path.dirname(os.getcwd()))
rd = rd + '/Resultados e Dados/Amazonas'

''' leituraa dos arquivos '''

# fire_nrt_M6_94041.csv contem dados de 2019-10-01 ate 2019-12-01
df = pd.read_csv(rd + r'/csv/fire_archive_M6_94041.csv')
# eventos1 contem apenas os dados com confiabilidade maior ou igual a 75%
eventos1 = df.loc[df['confidence'] >= 75]
del df

# fire_archive_M6_94041.csv contem dados de 2003-01-01 ate 2019-09-30
df = pd.read_csv(rd + r'/csv/fire_nrt_M6_94041.csv')
# eventos2 contem apenas os dados com confiabilidade maior ou igual a 75%
eventos2 = df.loc[df['confidence'] >= 75]
del df

# eventos comtem a concatenacao de eventos1 e eventos2
eventos = pd.concat([eventos1, eventos2], sort = True, ignore_index = True)
del eventos1
del eventos2

eventos.to_csv(rd + r'/csv/fire_unico.csv', index=False)

