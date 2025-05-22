"""
8 - Construa uma função que receba uma data no formato dd/mm/aaaa e retorne
uma string no formato D de mês por extenso de aaaa.

Se a data for inválida, a função deve retornar NULL.

A função deve considerar os meses por extenso como: "Janeiro", "Fevereiro", 
"Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro",
"Outubro", "Novembro", "Dezembro".
"""

from datetime import datetime

meses_por_extenso = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho",
    7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

def data_por_extenso(data_str):
    try:
        data = datetime.strptime(data_str, "%d/%m/%Y")

        dia = data.day
        mes = data.month
        ano = data.year
        
        mes_extenso = meses_por_extenso.get(mes)
        if not mes_extenso:
            return None
        return f"{dia} de {mes_extenso} de {ano}"
    
    except (ValueError, TypeError):
        return "NULL"

print(data_por_extenso("21/05/2025"))
print(data_por_extenso("21/13/2025"))
print(data_por_extenso("31/02/2025"))
print(data_por_extenso("15/05/2025"))
