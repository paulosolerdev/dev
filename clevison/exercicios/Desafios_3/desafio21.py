"""
21. Contagem de Segundas-Feiras no Dia 1º em um intervalo de datas

Escreva um programa em python que solicita ao usuário um intervalo de datas,
    com uma data de início e uma data de fim, e conta quantas segundas-feiras
    caem no dia 1º de cada mês dentro desse intervalo. 

O programa deve validar as entradas e garantir que a data de início seja
    anterior ou igual à data de fim.

Requisitos:
- O programa deve solicitar ao usuário que insira uma data de início e uma
    data de fim no formato "DD/MM/AAAA".
- O programa deve verificar se o dia 1º de cada mês dentro do intervalo
    especificado é uma segunda-feira e contar quantas vezes isso ocorre.
- Se a data de início for posterior à data de fim, o programa deve exibir
    uma mensagem de erro e solicitar que o usuário insira as datas novamente.
- Caso o formato da data seja inválido, o programa deve solicitar a correção
    até que o formato correto seja fornecido.
"""

from datetime import datetime, timedelta

def contar_segundas_feiras(data_inicio, data_fim):
    contador = 0
    data_atual = data_inicio

    while data_atual <= data_fim:
        if data_atual.day == 1 and data_atual.weekday() == 0:  # 0 é segunda-feira
            contador += 1
        data_atual += timedelta(days=1)

    return contador

def obter_data(mensagem):
    while True:
        try:
            data_str = input(mensagem)
            data = datetime.strptime(data_str, "%d/%m/%Y")
            return data
        except ValueError:
            print("Formato de data inválido. Por favor, use o formato DD/MM/AAAA.")

def main():
    while True:
        data_inicio = obter_data("Digite a data de início (DD/MM/AAAA): ")
        data_fim = obter_data("Digite a data de fim (DD/MM/AAAA): ")

        if data_inicio > data_fim:
            print("A data de início deve ser anterior ou igual à data de fim. Tente novamente.")
        else:
            break

    total_segundas_feiras = contar_segundas_feiras(data_inicio, data_fim)
    print(f"Total de segundas-feiras no dia 1º entre {data_inicio.strftime('%d/%m/%Y')} e {data_fim.strftime('%d/%m/%Y')}: {total_segundas_feiras}")

if __name__ == "__main__":
    main()
