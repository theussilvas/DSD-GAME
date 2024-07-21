import Pyro4

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class SharedObject:
    def __init__(self):
        self.data = []
        self.clients = []

    def add_item(self, item):
        self.data.append(item)
        self.notify_clients(item)
        return self.data

    def get_data(self):
        return self.data

    def register_callback(self, client_uri):
        client_proxy = Pyro4.Proxy(client_uri)
        self.clients.append(client_proxy)

    def notify_clients(self, item):
        for client in self.clients:
            try:
                client.notify(item)
            except Pyro4.errors.CommunicationError:
                self.clients.remove(client)

# Inicializar o servidor Pyro
def main():
    Pyro4.Daemon.serveSimple(
        {
            SharedObject: "example.sharedobject"
        },
        ns=True
    )

if __name__ == "__main__":
    main()
