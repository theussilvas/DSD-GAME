import Pyro4

@Pyro4.expose
class ClientCallback:
    def notify(self, item):
        print(f"Novo item adicionado: {item}")

def main():
    # Conectar-se ao Name Server
    ns = Pyro4.locateNS()
    
    # Obter referência do objeto remoto
    uri = ns.lookup("example.sharedobject")
    shared_object = Pyro4.Proxy(uri)
    
    # Configurar o callback
    daemon = Pyro4.Daemon()
    callback = ClientCallback()
    callback_uri = daemon.register(callback)
    shared_object.register_callback(callback_uri)
    
    # Iniciar thread do daemon do cliente para receber notificações
    def client_daemon():
        daemon.requestLoop()
    
    import threading
    threading.Thread(target=client_daemon, daemon=True).start()

    # Interagir com o objeto remoto
    print("Dados atuais:", shared_object.get_data())
    
    while True:
        new_item = input("Adicionar novo item: ")
        updated_data = shared_object.add_item(new_item)
        print("Dados atualizados:", updated_data)

if __name__ == "__main__":
    main()
