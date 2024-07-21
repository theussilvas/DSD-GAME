import Pyro4

@Pyro4.expose
class CallbackCliente:
    def notificar(self, mensagem):
        print(mensagem)

def main():
    ns = Pyro4.locateNS()
    uri = ns.lookup("exemplo.jogo_jokenpo")
    jogo_jokenpo = Pyro4.Proxy(uri)
    
    apelido = input("Digite seu apelido: ")

    daemon = Pyro4.Daemon()
    callback = CallbackCliente()
    uri_callback = daemon.register(callback)
    cliente_id = jogo_jokenpo.registrar_callback(uri_callback, apelido)
    print(f"Cliente registrado com ID: {cliente_id} e apelido: {apelido}")
    
    def daemon_cliente():
        daemon.requestLoop()
    
    import threading
    threading.Thread(target=daemon_cliente, daemon=True).start()
    
    while True:
        try:
            jogada = int(input("Digite sua jogada (0: pedra, 1: papel, 2: tesoura): "))
            jogo_jokenpo.jogar(jogada, cliente_id)
        except ValueError:
            print("Entrada inválida. Por favor, digite 0, 1 ou 2.")
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
