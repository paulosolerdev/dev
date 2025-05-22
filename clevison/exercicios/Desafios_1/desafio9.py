"""
9 - Faça um programa que leia 2 strings e informe:

- O conteúdo de cada string seguido do seu comprimento.
- Se as duas strings possuem o mesmo comprimento.
- Se as duas strings possuem conteúdo igual.
- O programa deve seguir as seguintes regras:

1. Solicitar ao usuário que insira duas strings.
2. Para cada string, exibir o conteúdo e o comprimento.
3. Verificar se as strings têm o mesmo comprimento e se possuem o mesmo
conteúdo.
4. Exibir se elas têm o mesmo comprimento e se são iguais ou diferentes
no conteúdo.
"""
# print("Digite duas strings")

# string1 = input("Digite a primeira string: ")
# string2 = input("Digite a segunda string: ")

# print(f"{string1} tem {len(string1)} caracteres")
# print(f"{string2} tem {len(string2)} caracteres")

# if len(string1) == len(string2):
#     print("As duas strings possuem o mesmo comprimento")
# else:
#     print("As duas strings possuem comprimento diferente")

# if string1 == string2:
#     print("As duas strings possuem o mesmo conteúdo")
# else:
#     print("As duas strings possuem conteúdo diferente")

def comparar_strings():
    string1 = input("Digite a primeira string: ")
    string2 = input("Digite a segunda string: ")

    print(f"{string1} tem {len(string1)} caracteres")
    print(f"{string2} tem {len(string2)} caracteres")

    if len(string1) == len(string2):
        print("As duas strings possuem o mesmo comprimento")
    else:
        print("As duas strings possuem comprimento diferente")
    
    if string1 == string2:
        print("As duas strings possuem o mesmo conteúdo")
    else:
        print("As duas strings possuem conteúdo diferente")

comparar_strings()
