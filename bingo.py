from random import randint
from time import sleep
from pip._vendor.rich.console import Console
from pip._vendor.rich.table import Table
from pip._vendor.rich.panel import Panel

class Bingo:
    def __init__(self):
        self.console = Console()
        self.numeros_sorteados = []
        self.cartelas = []
        
    def criar_cartela(self):
        cartela = []
        while len(cartela) < 24:
            num = randint(1, 75)
            if num not in cartela:
                cartela.append(num)
        cartela.sort()
        # Adiciona espaço vazio no centro
        cartela.insert(12, "  ")
        return cartela
    
    def mostrar_cartela(self, cartela, numero_cartela):
        table = Table(title=f"Cartela {numero_cartela}")
        
        # Adiciona 5 colunas
        for letra in "BINGO":
            table.add_column(letra, justify="center")
            
        # Adiciona as linhas
        for i in range(0, 25, 5):
            linha = cartela[i:i+5]
            # Marca números sorteados com *
            linha_formatada = [
                f"*{n}*" if n in self.numeros_sorteados else f" {n} "
                for n in linha
            ]
            table.add_row(*linha_formatada)
            
        self.console.print(table)
        
    def sortear_numero(self):
        while True:
            num = randint(1, 75)
            if num not in self.numeros_sorteados:
                self.numeros_sorteados.append(num)
                return num
                
    def verificar_vitoria(self, cartela):
        # Verifica linhas
        for i in range(0, 25, 5):
            if all(n in self.numeros_sorteados for n in cartela[i:i+5] if n != "  "):
                return True
                
        # Verifica colunas
        for i in range(5):
            if all(n in self.numeros_sorteados for n in cartela[i::5] if n != "  "):
                return True
                
        # Verifica diagonais
        diagonal1 = [cartela[0], cartela[6], cartela[18], cartela[24]]
        diagonal2 = [cartela[4], cartela[8], cartela[16], cartela[20]]
        
        if all(n in self.numeros_sorteados for n in diagonal1):
            return True
        if all(n in self.numeros_sorteados for n in diagonal2):
            return True
            
        return False
        
    def jogar(self):
        self.console.clear()
        self.console.print(Panel.fit("Bem-vindo ao Bingo!", style="bold green"))
        
        # Solicita número de jogadores
        num_jogadores = int(input("\nQuantos jogadores? "))
        
        # Cria cartelas para cada jogador
        self.cartelas = [self.criar_cartela() for _ in range(num_jogadores)]
        
        while True:
            self.console.clear()
            
            # Mostra cartelas
            for i, cartela in enumerate(self.cartelas, 1):
                self.mostrar_cartela(cartela, i)
                
            # Mostra números já sorteados
            self.console.print("\nNúmeros sorteados:", style="blue")
            self.console.print(sorted(self.numeros_sorteados))
            
            # Aguarda comando
            comando = input("\nPressione ENTER para sortear ou 'S' para sair: ").upper()
            if comando == 'S':
                break
                
            # Sorteia novo número
            numero = self.sortear_numero()
            self.console.print(f"\nNúmero sorteado: {numero}", style="bold yellow")
            sleep(2)
            
            # Verifica se alguém ganhou
            for i, cartela in enumerate(self.cartelas, 1):
                if self.verificar_vitoria(cartela):
                    self.console.clear()
                    self.mostrar_cartela(cartela, i)
                    self.console.print(f"\nBINGO! Jogador {i} venceu!", style="bold green")
                    return

if __name__ == "__main__":
    bingo = Bingo()
    bingo.jogar()
