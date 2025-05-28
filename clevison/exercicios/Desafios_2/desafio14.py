"""
14. Escreva um programa que:

- Receba do usuário uma série de nomes em uma única linha, separados por espaços.
- Organize esses nomes em ordem alfabética.
- Exiba os nomes ordenados em uma única linha, separados por espaço.
"""

print(*sorted(input().split()))
