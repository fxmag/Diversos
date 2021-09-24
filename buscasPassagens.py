import requests
import pandas as pd
from bs4 import BeautifulSoup

origem = 'SAO'
destino = 'NYC'
#IDA
anoIda = '2021'
mesIda = '10'
dataIda = list(range(25,28))

for x in dataIda:
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
    url = f'https://www.kayak.com.br/flights/{origem}-{destino}/{anoIda}-{mesIda}-{x}?sort=bestflight_a'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    preco = soup.find('span',{'class':'js-label js-price _itL _ibU _ibV _idj _kKW'}).text.strip()
    tempo = soup.find('span',{'class':'js-subLabel js-duration _ibU _ibV _idj _kLa _kLb _kLc _kLe _kKW'}).text.strip()
    empresa = soup.find('span',{'class':'codeshares-airline-names'}).text.strip()
    
    print(f'DIA: {x}/{mesIda}/{anoIda}')
    print('>>> MELHOR OPÇÃO <<<')
    print(f'Preço: {preco}')
    print(f'Duração: {tempo}')
    print(f'Empresa: {empresa}')
    print('-'*25)
    
print('*** FIM DA BUSCA ***')