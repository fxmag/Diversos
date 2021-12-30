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

#if not mt5.initialize(login=1002947504, server="ClearInvestimentos-CLEAR", password="Joh0516"):
#if not mt5.initialize(login=1092947504, server="ClearInvestimentos-DEMO", password="Joh0516"):
if not mt5.initialize(login=4999473749, server="MetaQuotes-Demo", password="elf4lnbx"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()

     
symbol = "EURUSD"
#symbol = "WDOF22"
item = symbol
ativo = symbol 

print(symbol)

# CRIAÇÃO DOS CÁLCULOS (MÉDIAS)
#timezone = pytz.timezone("Etc/UTC")
#utc_from = datetime(2021, 12, 24, tzinfo=timezone)
#rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M5, utc_from, 289)
#rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 123) # PARA 9 HORAS DE MERCADO, 108 BARRAS
rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 210) # PARA 9 HORAS DE MERCADO, 108 BARRAS
rates_frame = pd.DataFrame(rates)
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
resumo = rates_frame[['time','open','high','low','close','tick_volume']]
#resumo.tail()  


# CALCULO DO ESTOCASTICO e MME 3
n = 8
highMax = resumo['high'].rolling(n).max() 
lowMin = resumo['low'].rolling(n).min()

#estocastico
resumo['estoc %K'] = ((resumo['close'] - lowMin) / (highMax - lowMin)) * 100
resumo['estoc %D'] = resumo['estoc %K'].rolling(3).mean()

# estocastico lento
resumo["EstocS %K"] = resumo["estoc %D"]
resumo["EstocS %D"] = resumo["EstocS %K"].rolling(3).mean()
#resumo2.dropna(inplace=True) #remover espaços em branco

    
resumo['flag'] = ''
resumo['sinal'] = ''

for i in range (1, len(resumo)): # TRADE

    if resumo['EstocS %K'][i] > resumo['EstocS %D'][i]:
        resumo['flag'][i] = 'COMPRA'
    else:
        resumo['flag'][i] = 'VENDA'
    
for x in range(1,len(resumo)):
    if resumo['flag'][x] == resumo['flag'][x-1]:
        resumo['sinal'][x] = ''
    else:
        resumo['sinal'][x] = 'sinal'


# RESUMINDO A TABELA
resumo = resumo[['time','open','high','low','close','EstocS %K','EstocS %D','flag','sinal']]

# LÓGICA DE EXECUCAO
# MENSAGEM NA MUDANÇA DE CONDICAO

# FORCE PARA TESTES
#resumo['sinal'].iloc[-1] = 'sinal'

if resumo['sinal'].iloc[-1] == 'sinal':
    flag = resumo['flag'].iloc[-1]
    bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
    bot.sendMessage(-351556985, f' >> Estratégia ESTOC: {item} ({flag}) <<')
    print('Dados encontrados e enviados via Telegram'.upper())


# RELATÓRIO DAS POSIÇÕES
info_posicoes = mt5.positions_get(symbol = symbol)
if info_posicoes:
    #print(info_posicoes)
    df = pd.DataFrame(list(info_posicoes), columns=info_posicoes[0]._asdict().keys())
    #display(df)
    ticket = df['ticket'].iloc[0]
    natureza = df['type'].iloc[0]

# EXECUÇÃO EM CADA VARREDURA
#if (resumo['flag'].iloc[-2] == 'COMPRA') & (resumo['sinal'].iloc[-2] == 'sinal') & (resumo['EstocS %K'].iloc[-2] >= resumo['EstocS %D'].iloc[-2]) & (resumo['EstocS %K'].iloc[-2] >= 0.00) & (resumo['EstocS %K'].iloc[-2] <= 30.00):

    
def compra():
    # COMPRA: CALCULOS
    highBuy = resumo['high'].iloc[-2]
    lowBuy = resumo['low'].iloc[-2]
    amplitudeCandle = highBuy - lowBuy

    #precoCompra = closeBuy + 1
    precoCompra = highBuy + 0.00001
    precoLoss = lowBuy - 0.00001
    precoGain = precoCompra + amplitudeCandle

    print(f'Amplitude Candle: {amplitudeCandle}')
    print(f'Máxima: {highBuy}')
    print(f'Mínima: {lowBuy}')
    print(f'Preço Compra: {precoCompra}')
    print(f'Stop: {precoLoss}')
    print(f'Gain: {precoGain} ')

    symbol = "EURUSD"
    lot = 1.0
    #point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask
    desviation = 1
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
    



#elif (resumo['flag'].iloc[-2] == 'VENDA') & (resumo['sinal'].iloc[-2] == 'sinal') & (resumo['EstocS %K'].iloc[-2] <= resumo['EstocS %D'].iloc[-2]) & (resumo['EstocS %K'].iloc[-2] <= 100.00) & (resumo['EstocS %K'].iloc[-2] >= 70.00):
        
def venda():
    # VENDA: CALCULOS
    highSell = resumo['high'].iloc[-2]
    lowSell = resumo['low'].iloc[-2]
    amplitudeCandle = highSell - lowSell

    #precoVenda = closeSell - 1
    precoVenda = lowSell - 0.00001
    precoLoss = highSell + 0.00001
    precoGain = precoVenda - amplitudeCandle

    print(f'Amplitude Candle: {amplitudeCandle}')
    print(f'Máxima: {highSell}')
    print(f'Mínima: {lowSell}')
    print(f'Preço Venda: {precoVenda}')
    print(f'Stop: {precoLoss}')
    print(f'Gain: {precoGain}')

    symbol = "EURUSD"
    lot = 1.0
    point = mt5.symbol_info(symbol).point
    price=mt5.symbol_info_tick(symbol).bid
    desviation = 1
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



print(resumo.tail())

venda()     
 