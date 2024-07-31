from datetime import datetime
#Importação de data e hora

import Pyro4
#Importação Python Remote Objects, 
#É uma classe que permite construir aplicativos nos quais os objetos podem se comunicar entre si pela rede.
#-------------------------------------------------------------------------------------------------------------#

#Decorador do Pyro4 para marcar um método ou classe a ser exposta para chamadas remotas.
#Você pode aplicá-lo a um método ou a uma classe como um todo.
@Pyro4.expose  
class Chat(object):
    def send_message(self, nome, texto):
        agora = datetime.now()
        print(f'{nome} diz: {texto} - Recebido às {agora:%H:%M:%S} \n')

def start_server():
    daemon = Pyro4.Daemon() #Contém lógica do lado do servidor e despacha chamadas de método remoto de entrada para os objetos apropriados.
    ns = Pyro4.locateNS() #Obter um proxy para o servidor de nomes é feito usando a seguinte função Pyro4.locateNS.
    uri = daemon.register(Chat) #Tem a ver com chamadas de metodos remotos.
    ns.register('mess.server', str(uri)) #Registra um objeto (uri) com um nome lógico no servidor de nomes.
    print(f'Server conectado com sucesso, escutando novas mensagens') #Mensagem para sinalizar que a conexão foi establecida com sucesso.
    daemon.requestLoop()

#Caso de erro
if __name__ == '__main__':
    try:
        start_server()
    except (KeyboardInterrupt, EOFError):
        print('Tchauzinho! :D')
exit