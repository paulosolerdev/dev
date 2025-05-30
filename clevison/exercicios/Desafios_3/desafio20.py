"""
20. Exercício: Troca de posições na lista

Escreva um programa em python que receba uma lista de elementos mistos e
    troque as posições do primeiro e do último elemento da lista. O programa
    deve funcionar independentemente do tipo de elementos na lista
    (números, strings, etc.). Imprima a lista original e a lista modificada.

Requisitos:
- O programa deve receber uma lista de elementos mistos.
- A troca deve ser feita apenas entre o primeiro e o último elemento.
- O programa deve exibir a lista original e a lista após a troca.
- Se a lista contiver apenas um elemento ou estiver vazia, nenhuma
    troca deve ser realizada.
"""

def troca_posicoes(lista):
    if len(lista) > 1:
        # Armazenar o primeiro e o último elemento
        primeiro = lista[0]
        ultimo = lista[-1]
        
        # Trocar as posições
        lista[0] = ultimo
        lista[-1] = primeiro
        
    return lista

def main():
    # Receber a lista do usuário
    entrada = input("Digite os elementos da lista separados por vírgula: ")
    lista = [item.strip() for item in entrada.split(",") if item.strip()]
    
    # Exibir a lista original
    print("Lista original:", lista)
    
    # Trocar as posições e exibir a lista modificada
    lista_modificada = troca_posicoes(lista)
    print("Lista após a troca:", lista_modificada)

if __name__ == "__main__":
    main()
