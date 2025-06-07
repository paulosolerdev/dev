"""
Vou escrever um código com 10 linhas para testar o recuo de trecho selecionado com shift+tab.
"""

def main():
    # Solicita ao usuário que insira um número inteiro
    numero = int(input("Digite um número inteiro: "))
    
    # Verifica se o número é positivo, negativo ou zero
    if numero > 0:
        print("O número é positivo.")
    elif numero < 0:
        print("O número é negativo.")
    else:
        print("O número é zero.")

if __name__ == "__main__":
    main()
