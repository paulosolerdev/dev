""""
3.4 – Lista de convidados: Se pudesse convidar alguém, vivo ou morto, para o
jantar, quem você convidaria? Crie uma lista que inclua pelo menos três pessoas
que você gostaria de convidar para jantar. Em seguida, utilize sua lista para
exibir uma mensagem para cada pessoa, convidando-a para jantar.
"""

# Definindo a lista de convidados
convidados = ['Albert Einstein', 'Jesus Cristo', 'Abraham Lincoln']

# Exibindo mensagens de convite
for convidado in convidados:
    print(f"Olá {convidado}, você está convidado para um jantar especial!")

# Adicionando um novo convidado à lista
convidados.append('Marie Curie')
print(f"\n{convidados[-1]} também está convidada para o jantar!")

# Exibindo a lista atualizada de convidados
print("\nLista atualizada de convidados:")
for convidado in convidados:
    print(convidado)

# Adicionando mais convidados à lista
convidados.insert(0, 'Leonardo da Vinci')
convidados.insert(2, 'Mahatma Gandhi')
convidados.append('Simão Pedro')
print("\nNovos convidados foram adicionados à lista!")

# Exibindo a lista atualizada de convidados
print("\nLista atualizada de convidados:")
for convidado in convidados:
    print(convidado)

# Removendo convidados da lista
print("\nInfelizmente, não podemos convidar todos os convidados.")
removidos = [convidados.pop(0), convidados.pop(2), convidados.pop(3)]
print(f"\nOs seguintes convidados foram removidos da lista: {', '.join(removidos)}")
# Exibindo a lista final de convidados
print("\nLista final de convidados:")
for convidado in convidados:
    print(convidado)
# Limpando a lista de convidados
convidados.clear()
print("\nTodos os convidados foram removidos da lista.")
# Exibindo a lista final de convidados
print("\nLista final de convidados:")
print(convidados)
