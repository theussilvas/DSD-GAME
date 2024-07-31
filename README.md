# Projeto Biblioteca

Este projeto implementa uma biblioteca digital utilizando Pyro4 para comunicação remota entre cliente e servidor. Ele permite registrar usuários, autenticar usuários, adicionar livros, listar livros, emprestar livros e devolver livros.

## Pré-requisitos

- Python 3.6 ou superior
- Pyro4

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/theussilvas/DSD-GAME
   cd DSD-GAME/Biblioteca

2. **Crie um ambiente virtual e ative-o::**
   
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    
3. **Instale as dependências necessárias:**
   ```bash
      pip install Pyro4

## Configuração e Execução

### Passo 1: Executar o servidor de nomes do Pyro4

1. **Abra um terminal.**
2. **Execute o comando:**

   ```bash
   python3 -m Pyro4.naming -n 10.112.9.217

### Passo 2: Atualizar o IP no código do servidor
Abra o arquivo server.py no seu editor de texto.

### Passo 3: Atualize o IP na linha onde o daemon é criado:
  ```bash
      daemon = Pyro4.Daemon(host='10.112.9.217') 
      Salve o arquivo.
      Rode o server.py e o client.py
