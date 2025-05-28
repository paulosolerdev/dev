"""
10. Leonardo o Pescador comprou um microcomputador para controlar o rendimento
diário de seu trabalho.

Sempre que ele traz um peso de peixes maior que o estabelecido pelo
regulamento de pesca do estado de São Paulo (50 quilos) deve pagar uma
multa de R$ 8,00 por quilo excedente.

O programa deve seguir as seguintes regras:

- Solicitar que o usuário insira o peso total de peixes pescados em quilos.
- Se o peso for maior que 50 quilos, calcular o excesso e o valor da multa.
- Armazenar a quantidade de quilos excedentes na variável excesso.
- Armazenar o valor da multa na variável multa (R$ 8,00 por quilo excedente).
- Exibir o peso total, o excesso (se houver) e o valor da multa (se houver).

"""

def calcular_multa(peso):
    limite = 50
    valor_multa_por_quilo = 8
    
    if peso > limite:
        excesso = peso - limite
        multa = excesso * valor_multa_por_quilo
    else:
        excesso = 0
        multa = 0
    
    return excesso, multa

try:

    peso_total = float(input("Digite o peso total de peixes pescados em quilos: "))
    excesso, multa = calcular_multa(peso_total)
    
    print(f"Peso total: {peso_total:.2f} kg")
    
    if excesso > 0:
        print(f"Peso excedente: {excesso:.2f} kg")
        print(f"Valor da multa: R$ {multa:.2f}")
    else:
        print("Peso dentro do limite permitido.")

except ValueError:

    print("Entrada inválida. Por favor, insira um número válido.")