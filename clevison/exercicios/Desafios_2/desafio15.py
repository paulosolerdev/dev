"""
15. Desenvolva uma estrutura orientada a objetos que:

- Receba do usuário uma string qualquer.
- Converta essa string para letras maiúsculas.
- Cada funcionalidade deve ser implementada como métodos independentes
    dentro da classe, mas que operam sobre o mesmo dado compartilhado
    (a string fornecida).
- A estrutura deve permitir a separação clara entre os métodos de entrada de
    dados, processamento (conversão para maiúsculas) e exibição dos resultados,
    garantindo que cada método execute uma tarefa específica.

Requisitos:

    - Um método para receber a string do usuário.
    - Um método para realizar a conversão da string para letras maiúsculas.
    - Um método para exibir a string convertida.
    - Os métodos devem ser independentes, mas trabalhar sobre o mesmo atributo
        da classe.
"""

class ManipuladorDeString:
    def __init__(self):
        self.texto = ""

    def receber_string(self):
        self.texto = input("Digite uma string: ")

    def converter_para_maiusculas(self):
        return self.texto.upper()

    def exibir_string(self):
        print(self.converter_para_maiusculas())

# Exemplo de uso:
manipulador = ManipuladorDeString()
manipulador.receber_string()
manipulador.converter_para_maiusculas()
manipulador.exibir_string()
