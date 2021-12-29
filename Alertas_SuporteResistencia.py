import telepot

bot = telepot.Bot("5026686955:AAHvm0rJOf-_nSCi8sOHYVMhY8zPCBEd73k")

def recebeMsg(msg):
    texto = msg['text']
    #print(texto)
    if texto == '8579.5':
        print(f'SUPORTE CADASTRADO: {texto}')
    else:
        print('Texto diferente')


bot.message_loop(recebeMsg)

while True:
    pass