from datetime import datetime
import MetaTrader5 as mt5
import time
import telepot
import pytz

import pandas as pd
pd.set_option('display.max_columns', 500) # número de colunas
pd.set_option('display.width', 1500)      # largura máxima da tabela
pd.options.mode.chained_assignment = None  # default='warn'

agora = datetime.now()
print(f'Buscando dados...{agora}')

if not mt5.initialize(login=54679378, server="MetaQuotes-Demo", password="hz7ulfri"):
#if not mt5.initialize(login=1092947504, server="ClearInvestimentos-DEMO", password="Joh0516"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()
    

symbol = "GBPUSD"

# CRIAÇÃO DOS CÁLCULOS (MÉDIAS)
timezone = pytz.timezone("Etc/UTC")
utc_from = datetime(2021, 12, 21, tzinfo=timezone)
rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M10, utc_from, 73)
rates_frame = pd.DataFrame(rates)
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
df = rates_frame[['time','open','high','low','close']]
#df.head()

#vela = df.head(2)
vela = df
print(vela.tail())

#PRIMEIRA VELA
print('>> VELA 1 <<')
closeVela1 = vela['close'].iloc[-2]
openVela1 = vela['open'].iloc[-2]
highVela1 = vela['high'].iloc[-2]
lowVela1 = vela['low'].iloc[-2]
pontos1 = highVela1 - lowVela1

print(f'Open: {openVela1}')
print(f'Close: {closeVela1}')
print(f'Máxima: {highVela1}')
print(f'Mínima: {lowVela1}')
print(f'Pontos Vela 1: {pontos1}')
print('')

#SEGUNDA VELA
print('>> VELA 2 <<')
closeVela2 = vela['close'].iloc[-1]
openVela2 = vela['open'].iloc[-1]
highVela2 = vela['high'].iloc[-1]
lowVela2 = vela['low'].iloc[-1]
pontos2 = highVela2 - lowVela2

print(f'Open: {openVela2}')
print(f'Close: {closeVela2}')
print(f'Máxima: {highVela2}')
print(f'Mínima: {lowVela2}')
print(f'Pontos Vela 2: {pontos2}')


#COMPRA

if closeVela2 >= closeVela1:
    precoGain = closeVela1 + 10
    precoLoss = closeVela1 - 10
    
    # ENVIANDO ORDEM COMPRA 
    symbol = symbol
    lot = 1.0
    point = mt5.symbol_info(symbol).point
    #price = mt5.symbol_info_tick(symbol).ask
    price = closeVela1 + 0.00001
    desviation = 0.00001
    
    requestCOMPRA = {    
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": precoLoss,
        "tp": precoGain,
        "magic": 234000,
        "desviation": desviation,
        "comment": "prython script open",
        "type_time":mt5.ORDER_TIME_GTC,
        'type_filling':mt5.ORDER_FILLING_IOC,
        }
    resultCOMPRA = mt5.order_send(requestCOMPRA)
    resultCOMPRA
    print('\nORDEM DE COMPRA ENVIADA COM SUCESSO')
    print(f'Gain: {precoGain}')
    print(f'Loss: {precoLoss}')
    
    
#VENDA
elif closeVela2 <= closeVela1:
    precoGain = closeVela1 - 0.10000
    precoLoss = closeVela1 + 0.10000
    
    # ENVIANDO ORDEM VENDA    
    symbol = symbol
    lot = 1.0
    point = mt5.symbol_info(symbol).point
    #price=mt5.symbol_info_tick(symbol).bid
    price=closeVela1 - 0.00001
    desviation = 0.00001
    
    requestVENDA={
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": precoLoss,
        "tp": precoGain,
        "deviation": desviation,
        "magic": 234000,
        "comment": "python script close",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
        }    
    resultVENDA = mt5.order_send(requestVENDA)
    resultVENDA
    print('\nORDEM DE VENDA ENVIADA COM SUCESSO')
    print(f'Gain: {precoGain}')
    print(f'Loss: {precoLoss}')

else:
    print('AGUARDANDO PRÓXIMO SINAL')