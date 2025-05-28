"""
13. Crie um programa que:

- Solicite ao usuário que insira o tamanho desejado para a senha.
- Gere uma senha aleatória de acordo com o tamanho informado.
- A senha pode conter letras maiúsculas, minúsculas, números e 
caracteres especiais.
"""

import random
import string

def gerar_senha(tamanho):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    senha = ''.join(random.choice(caracteres) for _ in range(tamanho))
    return senha

try:
    tamanho = int(input("Digite o tamanho desejado para a senha: "))
    if tamanho <= 0:
        print("O tamanho da senha deve ser maior que zero.")
    else:
        senha_gerada = gerar_senha(tamanho)
        print("Senha gerada:", senha_gerada)

except ValueError:
    print("Entrada inválida. Por favor, insira um número inteiro válido.")
