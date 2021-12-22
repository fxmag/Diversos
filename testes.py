from datetime import datetime
import MetaTrader5 as mt5
import time
import telepot
import pytz

# importamos o módulo pandas para exibir os dados recebidos na forma de uma tabela
import pandas as pd
pd.set_option('display.max_columns', 500) # número de colunas
pd.set_option('display.width', 1500)      # largura máxima da tabela
pd.options.mode.chained_assignment = None  # default='warn'

#if not mt5.initialize(login=1092947504, server="ClearInvestimentos-DEMO", password="Joh0516"):
#if not mt5.initialize(login=1002947504, server="ClearInvestimentos-CLEAR", password="Joh0516"):
if not mt5.initialize(login=4999473749, server="MetaQuotes-Demo", password="elf4lnbx"):
#if not mt5.initialize(login=54679378, server="MetaQuotes-Demo", password="hz7ulfri"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()
    

# CRIAÇÃO DAS ORDENS ABERTURA E FECHAMENTO
# DOLAR ()
#symbol = "EURUSD"
#symbol = "WDOF22"
symbol = "GBPUSD"
#symbol = "USDJPY"
item = symbol
ativo = symbol

print(symbol)

# CRIAÇÃO DOS CÁLCULOS (MÉDIAS)
timezone = pytz.timezone("Etc/UTC")
utc_from = datetime(2021, 12, 22, tzinfo=timezone)
rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 40)
rates_frame = pd.DataFrame(rates)
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
resumo = rates_frame[['time','open','close','spread']]
#resumo

# SETUP 30.3
TrintaMME = resumo['close'].ewm(span=30).mean() 
TresMME = resumo['open'].ewm(span=3).mean()

resumo.insert(loc=4,column='MME 30',value=TrintaMME)
resumo.insert(loc=5,column='MME 3',value=TresMME)

# MACD
resumo['EMA12'] = resumo.close.ewm(span=12).mean()
resumo['EMA26'] = resumo.close.ewm(span=26).mean()
resumo['MACD'] = resumo.EMA12 - resumo.EMA26
resumo['signal'] = resumo.MACD.ewm(span=9).mean()
resumo['histog'] = resumo['MACD'] - resumo['signal']
#display(resumo.tail(60))

#teste = resumo[['MACD','signal','histog']]
#display(teste.tail(60))

# MONITORAMENTO
resumo['flag'] = ''
resumo['sinal'] = ''

for i in range (1, len(resumo)):
    if resumo['MME 30'][i] < resumo['MME 3'][i]:
        resumo['flag'][i] = 'COMPRA'
    else:
        resumo['flag'][i] = 'VENDA'

for x in range(1,len(resumo)):
    if resumo['flag'][x] == resumo['flag'][x-1]:
        resumo['sinal'][x] = ''
    else:
        resumo['sinal'][x] = 'sinal'

print(resumo.tail(40))