
# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Repaso de python 3 y analisis de precios OHLC                              -- #
# -- Codigo: principal.py - script principal de proyecto                                  -- #
# -- Rep: https://github.com/ITESOIF/MyST/tree/master/Notas_Python/Notas_RepasoPython     -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

# -- ------------------------------------------------------------- Importar con funciones -- #

import download as fn                              # Para procesamiento de datos
import pandas as pd                                 # Procesamiento de datos
import numpy as np
import plotly.express as px

# -- --------------------------------------------------------- Descargar precios de OANDA -- #

# token de OANDA
OA_Ak = '107596e9d65c' + '1bbc9175953d917140' + '12-f975c6201dddad03ac1592232c0ea0ea'
OA_In = ["EUR_USD", "AUD_USD", "GBP_USD", "USD_JPY", "EUR_JPY"]                  # Instrumento
OA_Gn = "H1"                        # Granularidad de velas
fini = pd.to_datetime("2019-07-06 00:00:00").tz_localize('GMT')  # Fecha inicial
ffin = pd.to_datetime("2019-12-06 00:00:00").tz_localize('GMT')  # Fecha final

# Descargar precios masivos

data = {}
for i in OA_In:
    data[i] = fn.f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=OA_Gn,
                             p3_inst=i, p4_oatk=OA_Ak, p5_ginc=4900)

# Tomamos unicamente los precios de cierre
closes = pd.DataFrame({OA_In[i]:data[OA_In[i]].Close for i in range(len(OA_In))}).dropna()
(closes/closes.iloc[0,:]).plot()

#

