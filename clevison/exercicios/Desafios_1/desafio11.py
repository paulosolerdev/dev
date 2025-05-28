"""
11. Faça um programa para uma loja de tintas.

O programa deve seguir as seguintes regras:

- Solicitar ao usuário o tamanho da área a ser pintada em metros quadrados.
- Considerar que a cobertura da tinta é de 1 litro para cada 5 metros quadrados.
- A tinta é vendida em latas de 18 litros, e cada lata custa R$ 100,00.

O programa deve calcular:
- A quantidade de latas de tinta necessárias para cobrir a área.
- O preço total das latas de tinta.
- Informe ao usuário a quantidade de latas de tinta a serem compradas e o preço total.
"""

import math

def calcular_tinta(area):
    cobertura_por_litro = 5
    litros_por_lata = 18
    preco_por_lata = 100.00

    litros_necessarios = area / cobertura_por_litro
    latas_necessarias = math.ceil(litros_necessarios / litros_por_lata)
    preco_total = latas_necessarias * preco_por_lata

    return latas_necessarias, preco_total

try:

    area = float(input("Digite o tamanho da área a ser pintada em metros quadrados: "))

    if area <= 0:
        raise ValueError("A área deve ser um valor positivo.")
    
    latas_necessarias, preco_total = calcular_tinta(area)

    print(f"Quantidade de latas de tinta necessárias: {latas_necessarias}")
    print(f"Preço total das latas de tinta: R$ {preco_total:.2f}")

except ValueError as e:
    print(f"Erro: {e}")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")
finally:
    print("Programa encerrado.")
