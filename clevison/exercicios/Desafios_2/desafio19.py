"""
19. Exercício: Validação de Endereço de Site

Escreva um programa em Python que solicite ao usuário a entrada de um 
    endereço de site e valide se o endereço digitado está correto, 
    atendento aos seguintes critérios:

- O endereço deve começar com o prefixo 'www.'.
- O endereço deve terminar com '.com.br'.
- O programa deve continuar pedindo ao usuário que insira o endereço até
    que ele seja validado como correto. Ao digitar um endereço válido,
    o programa deve exibir uma mensagem de confirmação e encerrar a execução.

Requisitos:
- Verifique se o endereço começa com 'www.' e termina com '.com.br'.
- Se o endereço não for válido, informe ao usuário e solicite uma nova entrada.
- O programa deve continuar até que um endereço válido seja fornecido.
"""

def validar_endereco(endereco):
    if endereco.startswith("www.") and endereco.endswith(".com.br"):
        return True
    return False

def solicitar_endereco():
    while True:
        endereco = input("Digite o endereço do site (deve começar com 'www.' e terminar com '.com.br'): ")
        if validar_endereco(endereco):
            print("Endereço válido!")
            break
        else:
            print("Endereço inválido. Por favor, tente novamente.")

def programa_principal():
    solicitar_endereco()

if __name__ == "__main__":
    programa_principal()
