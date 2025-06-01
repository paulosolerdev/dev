"""
23. Diferentes formas de somas os elementos de ums lista

Dada a lista x = [5, 10, 15, 20, 25], apresente pelo menos cinco formas 
    diferentes de retornar a soma dos elementos dessa lista. Utilize
    diferentes abordagens e estruturas de controle ou funções nativas do Python.

Requisitos:
- Apresente cinco maneiras distintas de calcular e exibir a soma dos elementos 
    da lista.
- As abordagens devem variar entre o uso de funções embutidas, laços de
    repetição, compreensões de lista e outras ferramentas da linguagem Python.
- O resultado final para cada método deve ser o mesmo: a soma dos elementos da
    lista.
"""

x = [5, 10, 15, 20, 25]

# 1. Usando a função sum()
soma1 = sum(x)
print(f'Soma usando a função sum(): {soma1}')

# 2. Usando um loop for
soma2 = 0
for numero in x:
    soma2 += numero
print(f"Soma usando loop for: {soma2}")

# 3. Usando uma compreensão de lista
soma3 = sum([numero for numero in x])
print(f'Soma usando compreensão de lista: {soma3}')

# 4. Usando a função reduce do módulo functools
from functools import reduce
soma4 = reduce(lambda a, b: a + b, x)
print(f'Soma usando reduce: {soma4}')

# 5. Usando um loop while
soma5 = 0
i = 0
while i < len(x):
    soma5 += x[i]
    i += 1
print(f'Soma usando loop while: {soma5}')

# 6. Usando a função map
soma6 = sum(map(int, x))
print(f'Soma usando map: {soma6}')

# 7. Usando a função zip com uma lista de zeros
soma7 = sum(a + b for a, b in zip(x, [0]*len(x)))
print(f'Soma usando zip: {soma7}')

# 8. Usando a função enumerate
soma8 = sum(numero for index, numero in enumerate(x))
print(f'Soma usando enumerate: {soma8}')

# 9. Usando a função filter para filtrar números positivos
soma9 = sum(filter(lambda n: n > 0, x))
print(f'Soma usando filter: {soma9}')

# 10. Usando a função len para calcular a média e multiplicar pelo tamanho da lista
soma10 = sum(x) * len(x) / len(x)
print(f'Soma usando len para calcular a média: {soma10}')
