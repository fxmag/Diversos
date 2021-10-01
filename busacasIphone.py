import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

urldolar = 'https://www.google.com/search?q=cota%C3%A7%C3%A3o+dolar&sxsrf=AOaemvL1XSAfg9Jh0kxrWyQcjrSyGO9nDQ%3A1633109871240&source=hp&ei=b0dXYcTWC4vJ5OUP39Cf-Ag&iflsig=ALs-wAMAAAAAYVdVfyGPXoe3GKL6__Pc_utTyRFKSfkS&oq=cota%C3%A7%C3%A3o+dolar&gs_lcp=Cgdnd3Mtd2l6EAMYATIECCMQJzILCAAQgAQQsQMQgwEyCwgAEIAEELEDEIMBMgsIABCABBCxAxCDATILCAAQgAQQsQMQgwEyCAgAEIAEELEDMgUIABCABDIICAAQgAQQsQMyCwgAEIAEELEDEIMBMgUIABCABDoOCC4QgAQQsQMQxwEQowI6CwguEIAEEMcBEKMCOhEILhCABBCxAxCDARDHARCjAjoECAAQQzoICAAQsQMQgwFQ0gxYwRFg4yNoAHAAeACAAcQBiAHfBZIBAzAuNJgBAKABAQ&sclient=gws-wiz'

option = Options()
option.headless = True
driverd = webdriver.Chrome(options=option)     # NAVEGADOR OFF
#driver = webdriver.Chrome()                  # NAVEGADOR ON
driverd.get(urldolar)
html = driverd.page_source
soupdolar = BeautifulSoup(html, 'html.parser')
cotacao = soupdolar.find('span',{'class':'DFlfde SwHCTb'}).text
#print(cotacao)
#print('Dados Obtidos')

z = cotacao.replace(',','.')
cotacao = float(z)
print(f'Cotação de HOJE do Dólar: {cotacao}')

driverd.close()


url = 'https://www.apple.com/shop/refurbished/iphone'

option = Options()
option.headless = True
#driver = webdriver.Chrome(options=option)   # NAVEGADOR OFF
driverc = webdriver.Chrome()                  # NAVEGADOR ON
driverc.get(url)
html = driverc.page_source
soup = BeautifulSoup(html, 'html.parser')

matriz = soup.find_all('ul',{'class':'as-gridpage-producttiles as-producttiles pinwheel'})

for item in soup.find_all('li',{'class':'as-producttile as-util-relatedlink'}):
    phone = item.find('a',{'class':'as-producttile-tilelink'}).text
    preco = item.find('div',{'class':'as-price-currentprice as-producttile-currentprice'}).text
    economia = item.find('span',{'class':'as-producttile-savingsprice'}).text.strip()
    
    #preco = str(preco)
    preco = preco.strip('$')
    preco = float(preco)
    
    economia = economia.strip('Save $')
    economia = float(economia)
                
    conversaoMain = (round(preco * cotacao))
    conversaoEcon = (round(economia * cotacao))
    
    print(phone)
    print(f'Dólar: ${preco}(R$ {conversaoMain})')
    print(F'Economia: ${economia} (R$ {conversaoEcon})')
    print('-'*30)

driverc.close()