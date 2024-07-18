def obter_jogada(jogador):
    print(f"{jogador}, escolha sua jogada (0: Pedra, 1: Papel, 2: Tesoura)")
    jogada = input().strip()
    while jogada not in ["0","1","2"]:
        print("Jogada inválida")
        jogada = input(f"{jogador}, escolha sua jogada (0: Pedra, 1: Papel, 2: Tesoura)").strip()

    return int(jogada)

def obter_vencedor(jogada1,jogada2):
    
    if jogada1 == jogada2:
        return None

    elif (jogada1 == 0 and jogada2 == 2) or \
         (jogada1 == 1 and jogada2 == 0) or \
         (jogada1 == 2 and jogada2 == 1):
        return 1
    else:
        return 2

def placar(pla1,pla2,jog1,jog2):
    print(f"Placar: {jog1} {pla1} x {pla2} {jog2}")      

def main():
    jog1 = input("Jog1, escolha seu apelido:").strip()
    jog2 = input("Jog2, escolha seu apelido:").strip()

    pla1 = 0
    pla2 = 0

    while True:
        jogada1 = obter_jogada(jog1)
        jogada2 = obter_jogada(jog2)
        print(f"{jogada1} e {jogada2}")       

        winner = obter_vencedor(jogada1,jogada2)

        if winner is None:
            print("Empate")
        elif (winner == 1):
            print(f"{jog1} Venceu esta rodada!")
            pla1 += 1
        else:
            print(f"{jog2} Venceu esta rodada!")
            pla2 += 1   

        placar(pla1,pla2,jog1,jog2)

        continuar = input("Mais uma rodada? (s/n)").strip()
        if continuar != "s":
            break

if __name__ == "__main__":
    main()