import pyautogui as py
from time import sleep

tempo1 = 2
tempo2 = 7

grupo1 = ['osvaldo','alirio','jose','roberto']
mensagem1 = 'Bom dia meu amigo. Como vai você? Tudo bem por aí?'

grupo2 = ['arquivos']
mensagem2 = 'Olá minha querida irmã. Como está? Tudo bem por aí?'

#Abrir navegador 
py.click(152,746) 
sleep(tempo1)

#digitar WhatsappWeb 
py.click(319,64) 
sleep(tempo1) 
py.typewrite('https://web.whatsapp.com\n',interval=0.20) 
sleep(35)

#Escolher Contatos 
for item in grupo2: 
    py.click(80,274) 
    py.typewrite(item,interval=0.3) 
    py.press('enter') 
    sleep(tempo1) 
    py.typewrite(mensagem1,interval=0.3)
    py.press('enter') 
py.click(1340,8)
py.press('enter')

#posicao = py.position()
#print(posicao)
