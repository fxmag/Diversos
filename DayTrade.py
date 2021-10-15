import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
pd.options.mode.chained_assignment = None

#ticker = input(f'Qual o ticker? ')
ticker = 'asai3f'
dia = yf.Ticker(ticker+'.SA')
base = dia.history(period='1d', interval='5m')

# Criar coluna 'Dif' e efetuar a subtração
base['Dif'] = base['Close'] - base['Open']
# Criar coluna 'G/P' e efetuar calculo
base['G/P %'] = base['Dif'] / base['Open']
# Redefinir a tabela 'base' com as colunas desejadas
base = base[['Open','Close','Dif','G/P %','Volume']]
# Criar coluna 'Sinal' com o indicativo de C ou V
base['Sinal'] = ''
for i in range (1, len(base)):
    if base['Open'][i] < base['Close'][i]:
        base['Sinal'][i] = 'C'
    else:
        base['Sinal'][i] = 'V'
# Contar os 'V' e 'C' na tabela Sinal
cv = base['Sinal'].value_counts(dropna=False) 
# Transformar dados C ou V em lista
cv.to_list()
compra = cv[1]
venda = cv[0]
print(f'Compra: {compra}')
print(f'Venda: {venda}')
# Organizar por maiores ganhos
mediaGeral = base.sort_values(by=['G/P %'], ascending=False).head(50)
#medias
# Média dos ganhos
medias = mediaGeral[['G/P %']]
mediaGanho = float(medias.mean())
mediaGanho = round(mediaGanho,5)
print(mediaGanho)

venda = base[['Open','G/P %']]
venda[['Gatilho']] = base[['Open']] * mediaGanho + base[['Open']]
venda = round(venda,2)
venda.tail(5)