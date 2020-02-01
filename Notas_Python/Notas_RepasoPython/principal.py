
# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Repaso de python 3 y analisis de precios OHLC                              -- #
# -- Codigo: principal.py - script principal de proyecto                                  -- #
# -- Rep: https://github.com/ITESOIF/MyST/tree/master/Notas_Python/Notas_RepasoPython     -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

# -- ------------------------------------------------------------- Importar con funciones -- #

import funciones as fn                              # Para procesamiento de datos
import visualizaciones as vs                        # Para visualizacion de datos
import pandas as pd                                 # Procesamiento de datos
import numpy as np
import plotly.express as px
from datos import OA_Ak                             # Importar token para API de OANDA

# -- --------------------------------------------------------- Descargar precios de OANDA -- #

# token de OANDA
OA_In = "EUR_USD"                  # Instrumento
OA_Gn = "D"                        # Granularidad de velas
fini = pd.to_datetime("2019-07-06 00:00:00").tz_localize('GMT')  # Fecha inicial
ffin = pd.to_datetime("2019-12-06 00:00:00").tz_localize('GMT')  # Fecha final

# Descargar precios masivos
df_pe = fn.f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=OA_Gn,
                             p3_inst=OA_In, p4_oatk=OA_Ak, p5_ginc=4900)

# -- --------------------------------------------------------------- Graficar OHLC plotly -- #

vs_grafica1 = vs.g_velas(p0_de=df_pe.iloc[0:120, :])
vs_grafica1.show()

# -- ------------------------------------------------------------------- Conteno de velas -- #

# multiplicador de precios
pip_mult = 10000

# -- 0A.1: Hora
df_pe['hora'] = [df_pe['TimeStamp'][i].hour for i in range(0, len(df_pe['TimeStamp']))]

# -- 0A.2: Dia de la semana.
df_pe['dia'] = [df_pe['TimeStamp'][i].weekday() for i in range(0, len(df_pe['TimeStamp']))]

# -- 0B: Boxplot de amplitud de velas (close - open).
df_pe['co'] = (df_pe['Close'] - df_pe['Open'])*pip_mult

# -- ------------------------------------------------------------ Graficar Boxplot plotly -- #
vs_grafica2 = vs.g_boxplot_varios(p0_data=df_pe[['co']], p1_norm=False)
vs_grafica2.show()

# -- 01: Mes de la vela.
df_pe['mes'] = [df_pe['TimeStamp'][i].month for i in range(0,len(df_pe['TimeStamp']))]

# -- 02: Sesion de la vela.
sesion = []
for i  in range(len(df_pe.mes)):
    if i in [22, 23, 0, 1, 2, 3, 4, 5, 6, 7]:
        s = 'asia'
    elif i in [8]:
        s = 'asia_europa'
    elif i in [9, 10, 11, 12]:
        s = 'europa'
    elif i in [13, 14, 15, 16]:
        s = 'europa_america'
    elif i in [17, 18, 19, 20, 21]:
        s = 'america'
    sesion.append(s)
df_pe['sesion'] = sesion

# -- 03: Amplitud OC esperada de vela para cualquier dia de la semana (Dist de Freq).
df_pe['OC'] = (df_pe.Open - df_pe.Close)*pip_mult

# -- 04: Amplitud HL esperada de vela para cualquier dia de la semana (Dist de Freq).
df_pe['hl'] = (df_pe.High - df_pe.Low)*pip_mult

# -- 05: Evolucion de velas consecutivas (1: Alcistas, 0: Bajistas).
df_pe['sentido'] = ['alcista'if i>=0 else 'bajista' for i in df_pe.co]
df_pe['sentido_c'] = fn.secuencial(df_pe.sentido)

# -- 06: Maxima evolucion esperada de velas consecutivas (Dist Acum de Freq).
periodos = [5, 25, 50]
tmp = [[df_pe['hl'][i:i+5].max() for i in range(len(df_pe.hl)-j)] for j in periodos]
volatilidad_5 = tmp[0]
volatilidad_25 = tmp[1]
volatilidad_50 = tmp[2]

# -- 07: Calculo + Grafica autopropuesta.
px.line(df_pe, x = "TimeStamp", y = "OC", title = 'Open-Close pips').show()