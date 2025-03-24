def limpar_tela():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def aguardar_enter():
    input("\nPressione ENTER para continuar...")
    limpar_tela()

def executar_codigo(codigo, globals_dict=None):
    if globals_dict is None:
        globals_dict = {}
    
    try:
        exec(codigo, globals_dict)
        return True, None
    except Exception as e:
        return False, str(e)

def verificar_resposta(resposta_usuario, resposta_esperada):
    return resposta_usuario.strip().lower() == resposta_esperada.strip().lower()

def tutorial_variaveis():
    print("=== 1. Variáveis e Tipos de Dados ===")
    print("\nEm Python, você não precisa declarar o tipo da variável.")
    print("O tipo é determinado automaticamente pelo valor atribuído.")
    
    print("\nExemplo 1: Criando uma variável do tipo string")
    print('Digite: nome = "Python"')
    
    while True:
        resposta = input(">>> ")
        if verificar_resposta(resposta, 'nome = "Python"'):
            print("Correto! Agora vamos imprimir a variável.")
            print('Digite: print(nome)')
            
            while True:
                resposta = input(">>> ")
                if verificar_resposta(resposta, 'print(nome)'):
                    sucesso, erro = executar_codigo('nome = "Python"\n' + resposta)
                    if sucesso:
                        break
                print("Tente novamente!")
            break
        print("Tente novamente!")
    
    aguardar_enter()

def tutorial_operacoes():
    print("=== 2. Operações Básicas ===")
    print("\nVamos praticar operações matemáticas básicas.")
    
    print("\nExemplo 1: Soma")
    print("Digite: 5 + 3")
    
    while True:
        resposta = input(">>> ")
        if verificar_resposta(resposta, '5 + 3'):
            print("Resultado:", eval(resposta))
            break
        print("Tente novamente!")
    
    print("\nExemplo 2: Multiplicação")
    print("Digite: 4 * 6")
    
    while True:
        resposta = input(">>> ")
        if verificar_resposta(resposta, '4 * 6'):
            print("Resultado:", eval(resposta))
            break
        print("Tente novamente!")
    
    aguardar_enter()

def tutorial_condicionais():
    print("=== 3. Estruturas Condicionais ===")
    print("\nVamos criar uma estrutura if-else simples.")
    
    print("\nDigite o seguinte código:")
    print("idade = 18")
    print("if idade >= 18:")
    print("    print('Maior de idade')")
    print("else:")
    print("    print('Menor de idade')")
    
    codigo_correto = """idade = 18
if idade >= 18:
    print('Maior de idade')
else:
    print('Menor de idade')"""
    
    codigo_usuario = ""
    print("\nDigite o código (pressione Enter duas vezes para finalizar):")
    
    while True:
        linha = input()
        if linha == "":
            break
        codigo_usuario += linha + "\n"
    
    if codigo_usuario.strip() == codigo_correto.strip():
        print("\nCorreto! Executando o código:")
        executar_codigo(codigo_usuario)
    else:
        print("\nO código não está exatamente como esperado. Veja o exemplo novamente.")
    
    aguardar_enter()

def tutorial_loops():
    print("=== 4. Loops ===")
    print("\nVamos criar um loop for simples.")
    
    print("\nDigite o seguinte código:")
    print("for i in range(3):")
    print("    print(i)")
    
    codigo_correto = """for i in range(3):
    print(i)"""
    
    codigo_usuario = ""
    print("\nDigite o código (pressione Enter duas vezes para finalizar):")
    
    while True:
        linha = input()
        if linha == "":
            break
        codigo_usuario += linha + "\n"
    
    if codigo_usuario.strip() == codigo_correto.strip():
        print("\nCorreto! Executando o código:")
        executar_codigo(codigo_usuario)
    else:
        print("\nO código não está exatamente como esperado. Veja o exemplo novamente.")
    
    aguardar_enter()

def tutorial_listas():
    print("=== 5. Listas ===")
    print("\nVamos criar e manipular uma lista.")
    
    print("\nExemplo 1: Criando uma lista")
    print('Digite: frutas = ["maçã", "banana", "laranja"]')
    
    while True:
        resposta = input(">>> ")
        if verificar_resposta(resposta, 'frutas = ["maçã", "banana", "laranja"]'):
            print("\nAgora vamos acessar o primeiro elemento.")
            print("Digite: print(frutas[0])")
            
            while True:
                resposta = input(">>> ")
                if verificar_resposta(resposta, 'print(frutas[0])'):
                    sucesso, erro = executar_codigo('frutas = ["maçã", "banana", "laranja"]\n' + resposta)
                    if sucesso:
                        break
                print("Tente novamente!")
            break
        print("Tente novamente!")
    
    aguardar_enter()

def tutorial_funcoes():
    print("=== 6. Funções ===")
    print("\nVamos criar uma função simples.")
    
    print("\nDigite o seguinte código:")
    print("def saudacao(nome):")
    print("    return f'Olá, {nome}!'")
    print("\nE depois:")
    print("print(saudacao('Maria'))")
    
    codigo_correto = """def saudacao(nome):
    return f'Olá, {nome}!'

print(saudacao('Maria'))"""
    
    codigo_usuario = ""
    print("\nDigite o código (pressione Enter duas vezes para finalizar):")
    
    while True:
        linha = input()
        if linha == "":
            break
        codigo_usuario += linha + "\n"
    
    if codigo_usuario.strip() == codigo_correto.strip():
        print("\nCorreto! Executando o código:")
        executar_codigo(codigo_usuario)
    else:
        print("\nO código não está exatamente como esperado. Veja o exemplo novamente.")
    
    aguardar_enter()

def menu_principal():
    while True:
        limpar_tela()
        print("=== Tutorial Interativo de Python ===")
        print("\nEscolha um tópico para estudar:")
        print("1. Variáveis e Tipos de Dados")
        print("2. Operações Básicas")
        print("3. Estruturas Condicionais")
        print("4. Loops")
        print("5. Listas")
        print("6. Funções")
        print("0. Sair")
        
        opcao = input("\nDigite o número da opção desejada: ")
        
        if opcao == "1":
            tutorial_variaveis()
        elif opcao == "2":
            tutorial_operacoes()
        elif opcao == "3":
            tutorial_condicionais()
        elif opcao == "4":
            tutorial_loops()
        elif opcao == "5":
            tutorial_listas()
        elif opcao == "6":
            tutorial_funcoes()
        elif opcao == "0":
            print("\nObrigado por usar o Tutorial Interativo de Python!")
            break
        else:
            print("\nOpção inválida!")
            aguardar_enter()

if __name__ == "__main__":
    menu_principal()
