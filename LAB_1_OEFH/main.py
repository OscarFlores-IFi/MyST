# -- ------------------------------------------------------------- Importar con funciones -- #

import download as fn                              # Para procesamiento de datos
import pandas as pd                                 # Procesamiento de datos
import numpy as np
import plotly.express as px

# -- --------------------------------------------------------- Descargar precios de OANDA -- #

# token de OANDA
OA_Ak = '107596e9d65c' + '1bbc9175953d917140' + '12-f975c6201dddad03ac1592232c0ea0ea'
Id = ["EUR_USD", "AUD_USD", "GBP_USD", "USD_JPY", "EUR_JPY"]                  # Instrumento
OA_Gn = "H1"                        # Granularidad de velas
fini = pd.to_datetime("2019-07-06 00:00:00").tz_localize('GMT')  # Fecha inicial
ffin = pd.to_datetime("2019-12-06 00:00:00").tz_localize('GMT')  # Fecha final

# Descargar precios masivos

data = {}
for i in Id:
    data[i] = fn.f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=OA_Gn,
                             p3_inst=i, p4_oatk=OA_Ak, p5_ginc=4900)

# Tomamos unicamente los precios de cierre
closes = pd.DataFrame({Id[i]:data[Id[i]].Close for i in range(len(Id))}).dropna()
(closes/closes.iloc[0,:]).plot()

# Creamos la matriz de Promedios móviles para cada activo

vent = [3, 5, 8, 13, 21, 34]
MeanAvg = {j:pd.DataFrame({i:closes[j].rolling(i).mean() for i in vent}).dropna() for j in Id}













