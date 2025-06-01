"""
25. Dada uma lista contendo os dias da semana na seguinte ordem:

['Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo', 'Segunda']

Implemente um código em Python que reordene os elementos dessa lista de
    modo que o primeiro elemento seja "Segunda", seguido pela sequência 
    correta dos dias da semana. O objetivo é reorganizar a lista para obter
    o seguinte resultado:

['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
"""

# dias_da_semana = ['Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo', 'Segunda']
# print(dias_da_semana)

# #=================================================================#

# dias_da_semana_reordenados = ['Segunda'] + dias_da_semana[:-1]
# print(dias_da_semana_reordenados)

#=================================================================#

dias_da_semana = ['Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo', 'Segunda']
print("Lista original: ", dias_da_semana)

indice_segunda = dias_da_semana.index('Segunda')

dias_reordenados = dias_da_semana[indice_segunda:] + dias_da_semana[:indice_segunda]
print("Lista reordenada: ", dias_reordenados)
