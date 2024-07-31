from datetime import datetime 
#Importação de data e hora

import Pyro4
#Importação Python Remote Objects, 
#É uma classe que permite construir aplicativos nos quais os objetos podem se comunicar entre si pela rede.
#-------------------------------------------------------------------------------------------------------------#

server = Pyro4.Proxy(f"PYRONAME:mess.server") #Conexão com o server

def start_chatting(nick): #Função para inicicar o chat, Nick é apenas um parâmetro para nome, pode ser substítuido por qualquer outro nome.
    text = '' #Se for digitado 'sair' o chat acaba para o usuário
    while (text != 'sair'):
        text = input("Digite algo: ")
        now = datetime.now()
        server.send_message(nick, text) #Mensagem enviada para o servidor
        print(f'Enviado às {now:%H:%M:%S} \n')
    print('Tchau! ;) ')

nome = input("Qual o seu nome? ")

#Caso de erro
if __name__ == '__main__':
    try:
        start_chatting(nome)
    except (KeyboardInterrupt, EOFError):
        print('Tchau! ;) ')
exit


#Instruções de execução:
#Digite no terminal: pyro4-ns
#Em um novo terminal, execute o "server.py"
#Em um novo terminal, execute o "cliente.py"