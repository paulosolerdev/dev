# Exercício: Verificar se uma palavra é um palíndromo
#📝 Descrição:
#Crie uma função chamada eh_palindromo que receba uma palavra ou frase
#  e diga se ela é um palíndromo (ou seja, se ela é igual quando lida
#  de trás pra frente, ignorando espaços e letras maiúsculas/minúsculas).

"""
📥 Entrada:
Uma string com uma palavra ou frase.

📤 Saída:
Uma string dizendo se é ou não um palíndromo.


"""

def eh_palindromo(palavra):
    # Remove espaços e converte para minúsculas
    palavra = palavra.replace(" ", "").lower()
    
    # Verifica se a palavra é igual à sua reversa
    if palavra == palavra[::-1]:
        return "É um palíndromo"
    else:
        return "Não é um palíndromo"

# Testando a função
if __name__ == "__main__":
    palavra = input("Digite uma palavra ou frase: ")
    resultado = eh_palindromo(palavra)
    print(resultado)

# Testando a função com exemplos
palavras = [
    "arara",
    "radar",
    "reviver",
    "python",
    "socorram me subi no onibus em marrocos",
    "a base do teto desaba",
    "anotaram a data da maratona",
    "a mala nada na lama",
    "a grama é amarga",
    "a lata é tália",
    "a torre da derrota",
    "a vida é a arte do encontro",
    "a cara rajada da jararaca",
    "a dama admirou o rim da amada",
    "a mãe te ama"
]

for palavra in palavras:
    resultado = eh_palindromo(palavra)
    print(f"{palavra}: {resultado}")
