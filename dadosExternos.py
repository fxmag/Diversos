dados = open('C:\\Users\\johnny\\Documents\\Python Scripts\\VSCode\\dados.txt', 'r', encoding='utf-8')
leitura = dados.readlines()

usuario = leitura[0]
senha = leitura[1]

print(f'Usuário: {usuario}'.strip())
print(f'Senha: {senha}')



dados.close()