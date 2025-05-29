"""
16. Cadastro de veículos com Orientação a Objetos em Python

Implemente uma estrutura orientada a objetos para o cadastro de veículos.
Cada veículo deve ser descrito por suas características principais,
incluindo: marca, modelo, ano, cor e valor.

A estrutura deve permitir o cadastro de múltiplos veículos, e o sistema deve
exibir as informações completas de cada veículo, além do identificador de
memória do objeto correspondente.

Requisitos:
- Crie uma classe chamada veículo que represente o modelo de dados para
o cadastro de veículos, contendo os seguintes atributos:

    - marca (string): marca do veículo
    - modelo (string): modelo do veículo
    - ano (inteiro): ano de fabricação do veículo
    - cor (string): cor do veículo
    - valor (float): valor monetário do veículo

- Método de exibição: Implemente um método dentro da classe
    que permita exibir todas as informações de um veículo de forma
    organizada e amigável. Além disso, este método deve exibir o 
    identificador únido do objeto em memória.

- Cadastro de veículos: Cadastre pelo menos três veículos utilizando a
    classe criada. Para cada veículo cadastrado, exiba suas informações
    completas, incluindo o identificador de memória.
"""

class Veiculo:    
    
    def __init__(self, marca, modelo, ano, cor, valor):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        self.cor = cor
        self.valor = valor

    def exibir_informacoes(self):
        print("--- Informações do Veículo ---")
        print(f"Marca: {self.marca}")
        print(f"Modelo: {self.modelo}")
        print(f"Ano: {self.ano}")
        print(f"Cor: {self.cor}")
        print(f"Valor: R${self.valor:.2f}")
        print(f"Identificador de memória: {id(self)}")
        print("-" * 40)

# Cadastro de veículos
veiculo1 = Veiculo("Ford", "Mustang", 2022, "Vermelho", 350000.00)
veiculo2 = Veiculo("Chevrolet", "Camaro", 2021, "Preto", 320000.00)
veiculo3 = Veiculo("Dodge", "Challenger", 2023, "Azul", 380000.00)
veiculo4 = Veiculo("Bentley", "Continental GT", 2025, "Azul", 2000000.00)
veiculo5 = Veiculo("Toyota", "Corolla", 2025, "Preto", 150000.00)

# Exibição das informações dos veículos
veiculo1.exibir_informacoes()
veiculo2.exibir_informacoes()
veiculo3.exibir_informacoes()
veiculo4.exibir_informacoes()
veiculo5.exibir_informacoes()
