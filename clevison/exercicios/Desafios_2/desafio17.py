"""
17. Desenvolva um programa em Python que receba do usuário uma
    lista de números diferentes e retorne o maior deles.

O programa deve incluir as seguintes funcionalidades adicionais:

- Funções Aninhadas: O programa deve utilizar funções aninhadas para
realizar as comparações entre os valores e determinar qual o maior
número.

- Trabalho com Quantidade Variável de Números; O programa deve
permitir que o usuário insira qualquer quantidade de números
(não limitado a três) separados por espaço.

- Verificação de Duplicidade: Caso o usuário insira números duplicados,
    o programa deve notificar o usuário e solicitar a entrada de números
    diferentes.

- Ordenação Decrescente: Após identificar o maior número, o programa deve
exibir todos os números inseridos pelo usuário em ordem decrescente.

- Reinicialização Automática: O programa deve permitir ao usuário escolher
    se deseja rodá-lo novamente ao final da execução, sem precisar
    reiniciar o programa manualmente.
"""

def comparar_dois_numeros(a, b):
    if a > b:
        return a
    else:
        return b
    
def maior_valor(lista_numeros):
    maior = lista_numeros[0]
    
    for num in lista_numeros[1:]:
        maior = comparar_dois_numeros(maior, num)
    return maior

def verificar_duplicidade(lista_numeros):
    if len(lista_numeros) != len(set(lista_numeros)):
        return True
    return False

def solicitar_numeros():
    while True:
        try:
            entrada = input("Digite uma lista de números diferentes separados por espaço: ")
            numeros = list(map(float, entrada.split()))
        
            if verificar_duplicidade(numeros):
                print("Você digitou números duplicados. Por favor, insira números diferentes.")
                continue
            return numeros
        
        except ValueError:
            print("Entrada inválida. Por favor, insira apenas números inteiros separados por espaço.")

def exibir_numeros_ordenados(numeros):
    lista_ordenada = sorted(numeros, reverse=True)
    print("Números em ordem decrescente:", lista_ordenada)

def programa_principal():
    while True:
        numeros = solicitar_numeros()
        maior = maior_valor(numeros)
        
        print(f"O maior número é: {maior}")
        exibir_numeros_ordenados(numeros)
        
        continuar = input("Deseja rodar o programa novamente? (s/n): ").strip().lower()
        if continuar != 's':
            break

if __name__ == "__main__":
    programa_principal()
