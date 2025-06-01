# """
# 24. Implemente um sistema de carrinho de compras simples em Python.

# O sistema deverá permitir que o usuário adicione e remova itens do carrinho,
# bem como visualize o conteúdo do carrinho. A interação com o sistema será 
# feira via comandos de texto e ele deve permanecer ativo até que o usuário
# escolha encerrar.

# O sistema deve seguir estas instruções:

# Comandos:

# - adicionar: Solicita o nome de um item e o adiciona ao carrinho.
# - remover: Solicita o nome de um item e o remove do carrinho, se estiver presente.
# - ver: Exibe o conteúdo atual do carrinho.
# - sair: Encerra o programa.

# Regras:

# - Se o usuário tentar remover um item que não está no carrinho, uma mensagem
#     apropriada deve ser exibida.
# - Se o usuário tentar remover itens de um carrinho vazio, uma mensagem
#     informativa também deve ser exibida.
# - O sistema deve seguir funcionando até que o comando sair seja digitado.

# Restrições:

# - Não utilize compreensão de listas ou funções que retornem listas vazias.
# - Apenas estruturas condicionais simples (if, elif, else) devem ser usadas.
# """

# def carrinho_de_compras():
#     carrinho = []

#     while True:
#         comando = input("Digite um comando (adicionar, remover, ver, sair): ").strip().lower()

#         if comando == "adicionar":
#             item = input("Digite o nome do item a ser adicionado: ").strip()
#             carrinho.append(item)
#             print(f'Item "{item}" adicionado ao carrinho.')

#         elif comando == "remover":
#             if not carrinho:
#                 print("O carrinho está vazio. Não há itens para remover.")
#                 continue
                
#             item = input("Digite o nome do item a ser removido: ").strip()
#             if item in carrinho:
#                 carrinho.remove(item)
#                 print(f'Item "{item}" removido do carrinho.')
#             else:
#                 print(f'Item "{item}" não encontrado no carrinho.')

#         elif comando == "ver":
#             if not carrinho:
#                 print("O carrinho está vazio.")
#             else:
#                 print("Itens no carrinho:")
#                 for item in carrinho:
#                     print(f"- {item}")

#         elif comando == "sair":
#             print("Encerrando o sistema de carrinho de compras.")
#             break

#         else:
#             print("Comando inválido. Por favor, use 'adicionar', 'remover', 'ver' ou 'sair'.")

# if __name__ == "__main__":
#     carrinho_de_compras()

carrinho = []

while True:

    comando = input("Digite  'adicionar' para incluir um item, 'remover' para excluir, 'ver' para exibir o carrinho ou 'sair' para encerrar: ").lower()

    if comando == "adicionar":
        item = input("Digite o nome do item que deseja adicionar: ")
        carrinho.append(item)
        print(f'Item "{item}" adicionado ao carrinho.')
    
    elif comando == "remover":
        if carrinho:
            item = input("Digite o nome do item que deseja remover:")
            if item in carrinho:
                carrinho.remove(item)
                print(f'Item "{item}" removido do carrinho.')
            else:
                print(f'Item "{item}" não encontrado no carrinho.')
        else:
            print("O carrinho está vazio. Não há itens para remover.")

    elif comando == "ver":
        if carrinho:
            print("Itens no carrinho:")
            for item in carrinho:
                print(f"- {item}")
        else:
            print("O carrinho está vazio.")
    
    elif comando == "sair":
        print("Encerrando o sistema de carrinho de compras.")
        break

    else:
        print("Comando inválido. Por favor, use 'adicionar', 'remover', 'ver' ou 'sair'.")
