print("=== Bem-vindo ao Tutorial Python Básico ===")

# 1. Variáveis e Tipos de Dados
print("\n1. Variáveis e Tipos de Dados:")
nome = "Maria"
idade = 25
altura = 1.65
is_estudante = True

print(f"String (texto): {nome}")
print(f"Integer (número inteiro): {idade}")
print(f"Float (número decimal): {altura}")
print(f"Boolean (verdadeiro/falso): {is_estudante}")

# 2. Operações Básicas
print("\n2. Operações Básicas:")
a = 10
b = 3
print(f"Soma: {a + b}")
print(f"Subtração: {a - b}")
print(f"Multiplicação: {a * b}")
print(f"Divisão: {a / b}")
print(f"Divisão inteira: {a // b}")
print(f"Resto: {a % b}")
print(f"Potência: {a ** b}")

# 3. Estruturas Condicionais
print("\n3. Estruturas Condicionais:")
idade = 18
if idade >= 18:
    print("Maior de idade")
else:
    print("Menor de idade")

# 4. Loops
print("\n4. Loops:")
print("While loop:")
contador = 0
while contador < 3:
    print(f"Contador: {contador}")
    contador += 1

print("\nFor loop:")
for i in range(3):
    print(f"Número: {i}")

# 5. Listas
print("\n5. Listas:")
frutas = ["maçã", "banana", "laranja"]
print(f"Lista completa: {frutas}")
print(f"Primeiro item: {frutas[0]}")
frutas.append("uva")
print(f"Lista após adicionar uva: {frutas}")

# 6. Funções
print("\n6. Funções:")
def saudacao(nome):
    return f"Olá, {nome}!"

print(saudacao("João"))

# 7. Dicionários
print("\n7. Dicionários:")
pessoa = {
    "nome": "Carlos",
    "idade": 30,
    "cidade": "São Paulo"
}
print(f"Dicionário: {pessoa}")
print(f"Nome: {pessoa['nome']}")

print("\n=== Fim do Tutorial ===")
print("Continue praticando e explorando mais conceitos!")
