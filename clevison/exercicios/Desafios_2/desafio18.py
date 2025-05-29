"""
18. Exercício: Contagem de Letras Maiúsculas e Minúsculas

Escreva um programa em Python que leia uma palavra ou frase digitada pelo
    usuário e retorne o número total de letras maiúsculas e minúsculas
    presentes na entrada. O programa deve utilizar apenas lógica básica e
    funções embutidas do Python para realizar a contagem. 

Requisitos:

- O programa deve solicitar que o usuário digite uma palavra ou frase.
- O programa deve contar e exibir o número total de letras maiúsculas e
    minúsculas separadamente.
- Deve-se ignorar qualquer caractere que não seja uma letra, como números,
espaços, e pontuações.
- Utilize apenas funções embutidas do Python, como isalpha(), isupper() e 
islower() para realizar a contagem.
"""

def contar_maiusculas_minusculas(frase):
    maiusculas = 0
    minusculas = 0
    
    for letra in frase:
        if letra.isalpha():  # Verifica se é uma letra
            if letra.isupper():  # Verifica se é maiúscula
                maiusculas += 1
            elif letra.islower():  # Verifica se é minúscula
                minusculas += 1
    
    return maiusculas, minusculas

def programa_principal():
    entrada = input("Digite uma palavra ou frase: ")
    maiusculas, minusculas = contar_maiusculas_minusculas(entrada)
    
    print(f"Número de letras maiúsculas: {maiusculas}")
    print(f"Número de letras minúsculas: {minusculas}")

if __name__ == "__main__":
    programa_principal()
