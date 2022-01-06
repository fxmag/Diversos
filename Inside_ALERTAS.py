#!/usr/bin/env python
# coding: utf-8

# In[6]:


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
#print(f'Buscando dados...{agora}')

#if not mt5.initialize(login=54679378, server="MetaQuotes-Demo", password="hz7ulfri"):
if not mt5.initialize(login=1092947504, server="ClearInvestimentos-DEMO", password="Joh0516"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()

diaHoje = 5
diaAmanha = 6
diaHoje = str(diaHoje)

symbol = 'WDOG22'

# CRIAÇÃO DOS CÁLCULOS (MÉDIAS)
#timezone = pytz.timezone("Etc/UTC")
#utc_from = datetime(2022, 1, diaAmanha, tzinfo=timezone)
ratesM1 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 210)
rates_frameM1 = pd.DataFrame(ratesM1)
rates_frameM1['time']=pd.to_datetime(rates_frameM1['time'], unit='s')
dfM1 = rates_frameM1[['time','open','high','low','close']]
dfM1 = dfM1.tail(5)


#dfM1 = dfM1.loc[dfM1["time"].between('2022-1-4 10:01:00', '2022-1-4 18:00:00')]

dfM1


# In[9]:


candleRefHigh = dfM1['high'].iloc[-3]
candleRefLow = dfM1['low'].iloc[-3]

candleINSHigh = dfM1['high'].iloc[-2]
candleINSLow = dfM1['low'].iloc[-2]

print(f'Ref High: {candleRefHigh}')
print(f'Ref Low: {candleRefLow}')
print(f'Inside High: {candleINSHigh}')
print(f'Inside Low: {candleINSLow}')


# In[10]:


dfM1['RefHigh'] = candleRefHigh
dfM1['RefLow'] = candleRefLow
dfM1['INSHigh'] = candleINSHigh
dfM1['INSLow'] = candleINSLow

dfM1 = dfM1[['time','RefHigh','RefLow','INSHigh','INSLow']]
dfM1


# In[ ]:


dfM1['INSIDE'] = ''

for i in range (1, len(dfM1)):
    if (dfM1['RefHigh'][i] > dfM1['INSHigh'][i]) & (dfM1['RefLow'][i] < dfM1['INSLow'][i]):
    #if dfM1['RefHigh'][i] > dfM1['INSHigh'][i]:
        dfM1['INSIDE'][i] = 'INSIDE'
    else:
        dfM1['INSIDE'][i] = ''

display(dfM1.head(60))


# In[ ]:





# In[ ]:




