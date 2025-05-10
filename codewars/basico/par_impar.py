def par_ou_impar(numero):
    if numero % 2 == 0:
        return "Par"
    else:
        return "Ímpar"
    
# Testando a função
if __name__ == "__main__":
    numero = int(input("Digite um número: "))
    resultado = par_ou_impar(numero)
    print(f"O número {numero} é {resultado}.")

print("$==============================================$")

# Testando a função com números pares e ímpares
numeros = [2, 3, 4, 5, 6, 7, 8, 9, 10]
for numero in numeros:
    resultado = par_ou_impar(numero)
    print(f"O número {numero} é {resultado}.")

