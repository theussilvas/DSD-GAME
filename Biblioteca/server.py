import Pyro4
import Pyro4.naming
from datetime import datetime

@Pyro4.expose
#Pyro4.behavior(instance_mode="single")
class Biblioteca:
    def __init__(self):
        self.livros = ['O Senhor dos Anéis', 'Harry Potter', 'As Crônicas de Nárnia', 'O Pequeno Príncipe', 'Dom Quixote', 'As Aventuras de Sherlock Holmes', 'O Hobbit', 'Cem Anos de Solidão', 'O Alquimista']
        self.livrosEmprestados = {}
        self.usuarios = {}
        self.sessoes = {}

    def registrarUsuario(self, usuario, senha):
        usuario = usuario.lower()  # Transforma o nome de usuário em minúsculas
        if usuario in self.usuarios:
            return "Usuário já registrado."
        self.usuarios[usuario] = senha
        return "Usuário registrado com sucesso."

    def autenticarUsuario(self, usuario, senha):
        usuario = usuario.lower()  # Transforma o nome de usuário em minúsculas
        if usuario in self.usuarios and self.usuarios[usuario] == senha:
            self.sessoes[usuario] = True  # Marca o usuário como logado
            return "Autenticação bem-sucedida."
        return "Nome de usuário ou senha inválidos."

    def sair(self, usuario):
        usuario = usuario.lower()  # Transforma o nome de usuário em minúsculas
        if usuario in self.sessoes:
            del self.sessoes[usuario]  # Marca o usuário como deslogado
            return "Você saiu com sucesso."
        return "Você não está logado."

    def adicionarLivro(self, livro):
        self.livros.append(livro)
        return f"Livro '{livro}' adicionado à biblioteca."

    def obterLivros(self):
        return self.livros

    def emprestarLivro(self, usuario, livro_index):
        usuario = usuario.lower()  # Transforma o nome de usuário em minúsculas
        if usuario not in self.sessoes:
            return "Você precisa estar logado para emprestar um livro."
        if isinstance(livro_index, int) and 0 <= livro_index < len(self.livros):
            livro = self.livros[livro_index]
            if livro not in self.livrosEmprestados:
                data_hora = datetime.now().strftime('%d %B %Y %H:%M:%S')
                self.livrosEmprestados[livro] = {'usuario': usuario, 'data_hora': data_hora}
                self.livros.remove(livro)
                return f"{livro} emprestado para {usuario} em {data_hora}!"
            else:
                return f"{livro} já está emprestado."
        else:
            return "Índice de livro inválido."

    def obterLivrosEmprestados(self, usuario=None): #Lista de livros que o leitor pegou emprestado
        if usuario:
            usuario = usuario.lower()  # Transforma o nome de usuário em minúsculas
            return {livro: info for livro, info in self.livrosEmprestados.items() if info['usuario'] == usuario}
        return self.livrosEmprestados

    def devolverLivro(self, usuario, livro_index):
        usuario = usuario.lower()  # Transforma o nome de usuário em minúsculas
        if usuario not in self.sessoes:
            return "Você precisa estar logado para devolver um livro."
        
        livros_emprestados = self.obterLivrosEmprestados(usuario)
        if isinstance(livro_index, int) and 0 <= livro_index < len(livros_emprestados):
            livro = list(livros_emprestados)[livro_index]
            del self.livrosEmprestados[livro]
            self.livros.append(livro)
            return f"{livro} devolvido por {usuario}!"
        else:
            return "Número inválido. Por favor, forneça um número válido de livro."

def main():
    daemon = Pyro4.Daemon(host = '10.112.9.217') # IP DA MÁQUINA ONDE O SERVIDOR DE NOMES RODA
    uri = daemon.register(Biblioteca())
    ns = Pyro4.locateNS()
    ns.register("acesso.biblioteca", uri)

    print("Servidor da biblioteca está em execução.")
    daemon.requestLoop()
   

if __name__ == "__main__":
    main()

