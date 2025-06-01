"""
22. Reorganização de carros por ano de fabricação

Escreva um programa em python que receba uma lista de dicionários,
    onde cada dicionário descreve um carro e contém as seguintes
    informações:

- Modelo do carro (chave: "modelo").
- Ano de fabricação (chave: "ano_fabricacao").
- O objetivo é reorganizar a lista de carros de acordo com o ano de
    fabricação em ordem crescente, sem modificar a lista original,
    e exibir a lista reorganizada.

Requisitos:
- A lista de carros deve ser composta por dicionários, onde cada
    dicionário tem as chaves "modelo" e "ano_fabricacao".
- O programa deve reorganizar a lista com base no valor do campo
    "ano_fabricacao", do mais antigo ao mais recente.
- A lista original deve permanecer inalterada, e o resultado deve ser
    uma nova lista com os carros ordenados.
"""

def organizar_por_ano(carros):

    return sorted(carros, key=lambda carro: carro['ano_fabricacao'])


carros = [
    {"modelo": "Civic", "ano_fabricacao": 2010},
    {"modelo": "Continental GT", "ano_fabricacao": 2022},
    {"modelo": "SW4", "ano_fabricacao": 2023},
    {"modelo": "Corolla", "ano_fabricacao": 2024},
    {"modelo": "Fusca", "ano_fabricacao": 1980}
]

print("Lista original de carros: ")

for carro in carros:

    print(carro)

carros_organizados = organizar_por_ano(carros)

print("\nLista de carros organizada por ano de fabricação: ")

for carro in carros_organizados:

    print(carro)
