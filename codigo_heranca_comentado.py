"""
3. Pilares da POO

    Tipos de herança

    1. Herança simples: Uma classe herda de uma única superclasse.
    2. Herança múltipla: Uma classe herda de várias superclasses.

1. Herança simples: Uma classe herda de uma única classe base ou superclasse.

A herança simples é um conceito de programação orientada a objetos onde
uma classe herda atributos e métodos de uma única classe pai.

Vamos criar um exemplo simples de herança que representa diferentes
papéis em uma escola: Pessoa, Estudante e Professor.

A classe Pessoa é a classe pai e contém atributos e métodos comuns a 
todas as pessoas em uma escola, como nome e idade.

As classes Estudante e Professor herdam da classe Pessoa e adicionam
atributos e métodos específicos para cada estudante e professor, respectivamente.

Aqui está o código:
"""

# Classe base (superclasse) que define características comuns a todas as pessoas
class Pessoa:
    # Construtor da classe base que inicializa atributos comuns
    def __init__(self, nome, idade):
        self.nome = nome    # Atributo comum a todas as pessoas
        self.idade = idade  # Atributo comum a todas as pessoas

    # Método comum que será herdado por todas as subclasses
    def exibir_info(self):
        print(f"Nome: {self.nome}")
        print(f"Idade: {self.idade}")


# Subclasse que herda de Pessoa - exemplo de herança simples
# A sintaxe Estudante(Pessoa) indica que Estudante herda de Pessoa
class Estudante(Pessoa):
    # Construtor da subclasse
    def __init__(self, nome, idade, matricula):
        # Chamada ao construtor da classe pai para inicializar os atributos herdados
        Pessoa.__init__(self, nome, idade)
        # Atributo específico da classe Estudante
        self.matricula = matricula

    # Método específico da classe Estudante - especialização
    def estudar(self):
        print(f"{self.nome} está estudando.")


# Outra subclasse que herda de Pessoa - outro exemplo de herança simples
class Professor(Pessoa):
    # Construtor da subclasse
    def __init__(self, nome, idade, disciplina):
        # Chamada ao construtor da classe pai para inicializar os atributos herdados
        Pessoa.__init__(self, nome, idade)
        # Atributo específico da classe Professor
        self.disciplina = disciplina

    # Método específico da classe Professor - especialização
    def ensinar(self):
        print(f"{self.nome} está ensinando {self.disciplina}.")
    
# Criação de objetos - instanciando as classes

# Instância da classe base
pessoa = Pessoa("João", 30)
# Instância da subclasse Estudante
estudante = Estudante("Maria", 20, "12345")
# Instância da subclasse Professor
professor = Professor("Carlos", 40, "Matemática")

# Demonstração do uso dos objetos
print("\nInformações da Pessoa:")
pessoa.exibir_info()  # Chamada de método da classe base
print()

print("\nInformações do Estudante:")
estudante.exibir_info()  # Método herdado da classe base
estudante.estudar()      # Método específico da subclasse
print()

print("\nInformações do Professor:")
professor.exibir_info()  # Método herdado da classe base
professor.ensinar()      # Método específico da subclasse
print()
