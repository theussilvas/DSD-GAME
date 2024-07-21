import Pyro4
import threading

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class JogoJokenpo:
    def __init__(self):
        self.jogadas = [None, None]
        self.clientes = {}
        self.apelidos = {}
        self.lock = threading.Lock()
        self.turno = 0
        self.next_id = 0
        self.pontos = [0, 0]

    def jogar(self, jogada, cliente_id):
        with self.lock:
            if cliente_id != self.turno:
                raise Exception(f"Não é sua vez de jogar. É a vez de {self.apelidos[self.turno]}.")

            if jogada not in [0, 1, 2]:
                raise ValueError("Jogada inválida. Use 0 para pedra, 1 para papel e 2 para tesoura.")

            self.jogadas[cliente_id] = jogada
            self.turno = 1 - self.turno

            if None not in self.jogadas:
                resultado = self.determinar_vencedor()
                self.notificar_clientes(resultado)
                self.jogadas = [None, None]

                if max(self.pontos) >= 2:
                    vencedor = self.apelidos[self.pontos.index(max(self.pontos))]
                    self.notificar_clientes(f"{vencedor} venceu a partida!")
                    self.reiniciar_jogo()
            else:
                self.notificar_clientes(f"{self.apelidos[cliente_id]} fez sua jogada. Aguardando jogada de {self.apelidos[self.turno]}.")

    def determinar_vencedor(self):
        jogada1, jogada2 = self.jogadas

        if jogada1 == jogada2:
            return "Empate!"
        elif (jogada1 - jogada2) % 3 == 1:
            self.pontos[0] += 1
            return f"{self.apelidos[0]} vence a rodada com {self.jogada_para_texto(jogada1)} contra {self.jogada_para_texto(jogada2)} de {self.apelidos[1]}"
        else:
            self.pontos[1] += 1
            return f"{self.apelidos[1]} vence a rodada com {self.jogada_para_texto(jogada2)} contra {self.jogada_para_texto(jogada1)} de {self.apelidos[0]}"

    def jogada_para_texto(self, jogada):
        jogadas = ['pedra', 'papel', 'tesoura']
        return jogadas[jogada]

    def registrar_callback(self, uri_cliente, apelido):
        proxy_cliente = Pyro4.Proxy(uri_cliente)
        cliente_id = self.next_id
        self.next_id += 1
        self.clientes[cliente_id] = proxy_cliente
        self.apelidos[cliente_id] = apelido
        return cliente_id

    def notificar_clientes(self, mensagem):
        for cliente in self.clientes.values():
            try:
                cliente.notificar(mensagem)
            except Pyro4.errors.CommunicationError:
                pass

    def reiniciar_jogo(self):
        self.pontos = [0, 0]
        self.notificar_clientes("Iniciando uma nova partida. Boa sorte!")

def main():
    Pyro4.Daemon.serveSimple(
        {
            JogoJokenpo: "exemplo.jogo_jokenpo"
        },
        ns=True
    )

if __name__ == "__main__":
    main()
