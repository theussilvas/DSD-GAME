import Pyro4

def menu_principal():
    print("\nMenu da Biblioteca:")
    print("1. Ver livros")
    print("2. Adicionar um livro")
    print("3. Emprestar um livro")
    print("4. Ver livros emprestados")
    print("5. Devolver um livro")
    print("6. Sair")

def menu_login():
    print("\nMenu de Login:")
    print("1. Registrar")
    print("2. Login")
    print("3. Sair")

def main():
    ns = Pyro4.locateNS()
    uri = ns.lookup("acesso.biblioteca")
    biblioteca = Pyro4.Proxy(uri)

    usuario_logado = None

    while True:
        if usuario_logado:
            menu_principal()
            escolha = input("Digite sua escolha: ")

            if escolha == "1":
                livros = biblioteca.obterLivros()
                print()  # Pular uma linha
                if livros:
                    print("Livros disponíveis na biblioteca:")
                    for i, livro in enumerate(livros):
                        print(f"{i + 1}. {livro}")
                else:
                    print("Nenhum livro disponível na biblioteca.")
                print()  # Pular uma linha
            
            elif escolha == "2":
                livro = input("Digite o nome do livro para adicionar: ").lower()
                resultado = biblioteca.adicionarLivro(livro)
                print(resultado)
            
            elif escolha == "3":
                livros = biblioteca.obterLivros()
                print()  # Pular uma linha
                if livros:
                    print("Livros disponíveis para empréstimo:")
                    for i, livro in enumerate(livros):
                        print(f"{i + 1}. {livro}")
                    livro_index_str = input("Digite o número do livro para emprestar: ")
                    if livro_index_str.isdigit():
                        livro_index = int(livro_index_str) - 1
                        resultado = biblioteca.emprestarLivro(usuario_logado, livro_index)
                        print(resultado)
                    else:
                        print("Entrada inválida. Por favor, digite um número.")
                else:
                    print("Nenhum livro disponível para empréstimo.")
            
            elif escolha == "4":
                livrosEmprestados = biblioteca.obterLivrosEmprestados(usuario_logado)
                print()  # Pular uma linha
                if livrosEmprestados:
                    print("Seus livros emprestados:")
                    for i, (livro, info) in enumerate(livrosEmprestados.items()):
                        print(f"{i + 1}. {livro} emprestado em {info['data_hora']}")
                else:
                    print("Você não tem livros emprestados.")
            
            elif escolha == "5":
                livrosEmprestados = biblioteca.obterLivrosEmprestados(usuario_logado)
                print()  # Pular uma linha
                if livrosEmprestados:
                    print("Seus livros emprestados:")
                    for i, (livro, info) in enumerate(livrosEmprestados.items()):
                        print(f"{i + 1}. {livro} emprestado em {info['data_hora']}")
                    livro_index_str = input("Digite o número do livro para devolver: ")
                    if livro_index_str.isdigit():
                        livro_index = int(livro_index_str) - 1
                        livro = list(livrosEmprestados.keys())[livro_index]
                        resultado = biblioteca.devolverLivro(usuario_logado, livro)
                        print(resultado)
                    else:
                        print("Entrada inválida. Por favor, digite um número.")
                else:
                    print("Nenhum livro emprestado para devolver.")
            
            elif escolha == "6":
                resultado = biblioteca.sair(usuario_logado)
                print(resultado)
                usuario_logado = None
            
            else:
                print("Escolha inválida. Por favor, tente novamente.")
        else:
            menu_login()
            escolha = input("Digite sua escolha: ")

            if escolha == "1":
                usuario = input("Digite seu nome de usuário: ").lower()
                senha = input("Digite sua senha: ")
                resultado = biblioteca.registrarUsuario(usuario, senha)
                print(resultado)
            
            elif escolha == "2":
                usuario = input("Digite seu nome de usuário: ").lower()
                senha = input("Digite sua senha: ")
                resultado = biblioteca.autenticarUsuario(usuario, senha)
                print(resultado)
                if resultado == "Autenticação bem-sucedida.":
                    usuario_logado = usuario
            
            elif escolha == "3":
                break
            
            else:
                print("Escolha inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    main()
