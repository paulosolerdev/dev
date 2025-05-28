"""
12. Crie uma função que:

- Receba dois parâmetros: o nome e o sobrenome do usuário.
- Retorne o nome no formato americano: sobrenome, nome.
"""

def nome_americano(nome, sobrenome):
    return f'{sobrenome}, {nome}'

nome = input('Digite seu nome: ')
sobrenome = input('Digite seu sobrenome: ')

print(nome_americano(nome, sobrenome))
