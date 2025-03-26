import os
import time
import sys
from typing import Optional, Any
from datetime import datetime

class Tutorial:
    def __init__(self):
        self.nome_aluno = ""
        self.pontuacao = 0
        self.total_exercicios = 0
        self.historico = []
        self.data_inicio = None
        self.nivel_atual = "iniciante"
        self.modulos_completos = set()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self, title: str) -> None:
        self.clear_screen()
        print("\n" + "=" * 60)
        print(f"{title:^60}")
        print("=" * 60 + "\n")

    def print_loading(self, message: str) -> None:
        print(f"\n{message}", end="")
        for _ in range(3):
            time.sleep(0.3)
            print(".", end="", flush=True)
        print("\n")

    def salvar_progresso(self):
        # Simulação de salvamento de progresso
        self.print_loading("Salvando seu progresso")
        
    def carregar_progresso(self):
        # Simulação de carregamento de progresso
        self.print_loading("Carregando seu progresso")

    def get_user_input(self, prompt: str, valid_options: Optional[list] = None) -> str:
        while True:
            response = input(f"{prompt}: ").strip()
            if valid_options is None or response.lower() in valid_options:
                return response
            print(f"Por favor, escolha uma das opções válidas: {', '.join(valid_options)}")

    def show_lesson(self, topic: str, content: str) -> None:
        self.print_header(topic)
        print(content)
        input("\nPressione ENTER para continuar...")

    def run_practice(self, topic: str, instruction: str, correct_answer: Any, 
                    example: Optional[str] = None, dica: Optional[str] = None) -> bool:
        self.total_exercicios += 1
        self.print_header(f"Prática: {topic}")
        print(instruction)
        
        if example:
            print(f"\nExemplo: {example}")
        
        if dica:
            ver_dica = self.get_user_input("\nDeseja ver uma dica? (s/n)", ['s', 'n'])
            if ver_dica.lower() == 's':
                print(f"\nDica: {dica}")

        tentativas = 0
        max_tentativas = 3
        while tentativas < max_tentativas:
            resposta = self.get_user_input("\nSua resposta")
            is_correct = self.check_answer(resposta, correct_answer)
            
            if is_correct:
                self.pontuacao += 1
                print("\n✅ Parabéns! Resposta correta!")
                break
            else:
                tentativas += 1
                if tentativas < max_tentativas:
                    print(f"\n❌ Tente novamente! Você ainda tem {max_tentativas - tentativas} tentativa(s).")
                else:
                    print(f"\n❌ A resposta correta era: {correct_answer}")
                    print("Continue praticando!")
        
        self.historico.append({
            'topico': topic,
            'correto': is_correct,
            'resposta_user': resposta,
            'resposta_correta': correct_answer,
            'tentativas': tentativas,
            'data': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        input("\nPressione ENTER para continuar...")
        return is_correct

    def check_answer(self, user_answer: str, correct_answer: Any) -> bool:
        if isinstance(correct_answer, list):
            return user_answer.lower() in [str(ans).lower() for ans in correct_answer]
        return user_answer.lower() == str(correct_answer).lower()

    def show_progress(self) -> None:
        self.print_header("Seu Progresso")
        
        # Estatísticas gerais
        percentual = (self.pontuacao / self.total_exercicios) * 100 if self.total_exercicios > 0 else 0
        tempo_estudo = "Iniciado hoje" if not self.data_inicio else f"Estudando há {(datetime.now() - self.data_inicio).days} dias"
        
        print(f"Nome: {self.nome_aluno}")
        print(f"Nível atual: {self.nivel_atual.capitalize()}")
        print(f"Tempo de estudo: {tempo_estudo}")
        print(f"Módulos completos: {len(self.modulos_completos)}")
        print(f"Pontuação atual: {self.pontuacao}/{self.total_exercicios}")
        print(f"Percentual de acertos: {percentual:.1f}%")
        
        # Histórico detalhado
        print("\nHistórico de respostas:")
        for item in self.historico:
            status = "✅" if item['correto'] else "❌"
            print(f"\n{status} {item['topico']} ({item['data']})")
            print(f"   Tentativas: {item['tentativas']}/3")
            print(f"   Sua resposta: {item['resposta_user']}")
            print(f"   Resposta correta: {item['resposta_correta']}")

        input("\nPressione ENTER para continuar...")

    def menu_principal(self) -> str:
        self.print_header("Menu Principal")
        print(f"Bem-vindo(a), {self.nome_aluno}!")
        print("\nEscolha uma opção:")
        print("1. Começar/Continuar tutorial")
        print("2. Ver progresso")
        print("3. Escolher nível")
        print("4. Salvar progresso")
        print("5. Carregar progresso")
        print("6. Sair")
        return self.get_user_input("\nEscolha uma opção", ['1', '2', '3', '4', '5', '6'])

    def escolher_nivel(self) -> None:
        self.print_header("Escolha seu Nível")
        print("1. Iniciante")
        print("2. Intermediário")
        print("3. Avançado")
        nivel = self.get_user_input("\nEscolha seu nível", ['1', '2', '3'])
        niveis = {
            '1': 'iniciante',
            '2': 'intermediário',
            '3': 'avançado'
        }
        self.nivel_atual = niveis[nivel]
        print(f"\nNível alterado para {self.nivel_atual}!")
        input("\nPressione ENTER para continuar...")

    def executar_tutorial(self):
        self.data_inicio = datetime.now()
        self.print_header("Bem-vindo ao Tutorial Python Interativo!")
        self.nome_aluno = self.get_user_input("Primeiro, me diga seu nome")
        
        while True:
            opcao = self.menu_principal()
            
            if opcao == '1':
                self.executar_licoes()
            elif opcao == '2':
                self.show_progress()
            elif opcao == '3':
                self.escolher_nivel()
            elif opcao == '4':
                self.salvar_progresso()
            elif opcao == '5':
                self.carregar_progresso()
            else:
                self.finalizar_tutorial()
                break

    def executar_licoes(self):
        if self.nivel_atual == 'iniciante':
            self.executar_licoes_iniciante()
        elif self.nivel_atual == 'intermediário':
            self.executar_licoes_intermediario()
        else:
            self.executar_licoes_avancado()

    def executar_licoes_iniciante(self):
        # Lição 1: Variáveis
        self.show_lesson("Lição 1: Variáveis", 
            """Em Python, variáveis são como caixas onde guardamos informações.
            
            Tipos básicos de variáveis:
            - Strings (texto): nome = "Maria"
            - Números inteiros: idade = 25
            - Números decimais: altura = 1.75
            - Booleanos: esta_chovendo = True
            
            Para criar uma variável, use o operador de atribuição (=):
            exemplo = "valor" """)

        self.run_practice("Variáveis",
            "Crie uma variável 'numero' e atribua o valor 42",
            ["numero = 42", "numero=42"],
            example="idade = 25",
            dica="Use o operador = para atribuição")

        # Lição 2: Operações Matemáticas
        self.show_lesson("Lição 2: Operações Matemáticas",
            """Python é uma calculadora poderosa! Operações básicas:
            
            + : Adição (5 + 3 = 8)
            - : Subtração (10 - 4 = 6)
            * : Multiplicação (6 * 2 = 12)
            / : Divisão (15 / 3 = 5)
            ** : Potência (2 ** 3 = 8)
            % : Resto da divisão (17 % 5 = 2)
            
            Você pode combinar operações: (10 + 5) * 2""")

        self.run_practice("Matemática Básica",
            "Quanto é (4 + 6) * 2?",
            "20",
            dica="Primeiro resolva o que está dentro dos parênteses")

        # Lição 3: Strings
        self.show_lesson("Lição 3: Strings",
            """Strings são textos em Python.
            
            Formas de criar strings:
            - Com aspas simples: 'Olá'
            - Com aspas duplas: "Mundo"
            
            Operações com strings:
            - Concatenação: "Olá" + " Mundo"
            - Repetição: "Ha" * 3 = "HaHaHa"
            - Maiúsculas: "texto".upper()
            - Minúsculas: "TEXTO".lower()""")

        self.run_practice("Strings",
            'Concatene "Olá" com "Mundo"',
            ["Olá Mundo", "OláMundo", '"Olá" + "Mundo"', "'Olá' + 'Mundo'"],
            example='"Olá" + "Mundo" ou "Olá Mundo"',
            dica="Você pode usar + para juntar strings ou escrever diretamente")

        # Lição 4: Listas
        self.show_lesson("Lição 4: Listas",
            """Listas são coleções ordenadas de itens.
            
            Criando listas:
            numeros = [1, 2, 3, 4, 5]
            frutas = ["maçã", "banana", "laranja"]
            
            Operações com listas:
            - Acessar elemento: lista[0]
            - Adicionar: lista.append(item)
            - Remover: lista.remove(item)
            - Tamanho: len(lista)""")

        self.run_practice("Listas",
            "Crie uma lista com os números 1, 2 e 3",
            ["[1,2,3]", "[1, 2, 3]", "1,2,3", "1, 2, 3"],
            example="[1, 2, 3]",
            dica="Use colchetes [] para criar uma lista")

        self.modulos_completos.add("iniciante_basico")

    def executar_licoes_intermediario(self):
        # Lição 1: Estruturas de Controle
        self.show_lesson("Lição 1: Estruturas de Controle",
            """As estruturas de controle permitem que seu código tome decisões.
            
            if condição:
                # código se verdadeiro
            elif outra_condição:
                # código se a primeira for falsa e esta verdadeira
            else:
                # código se todas forem falsas
            
            Operadores de comparação:
            == : igual
            != : diferente
            >  : maior que
            <  : menor que
            >= : maior ou igual
            <= : menor ou igual""")

        self.run_practice("Estruturas de Controle",
            "Escreva um if que verifica se idade é maior que 18",
            ["if idade > 18:", "if idade > 18", "if(idade > 18):", "if(idade > 18)"],
            example="if idade > 18:",
            dica="Use if seguido da condição e dois pontos")

        # Lição 2: Loops
        self.show_lesson("Lição 2: Loops",
            """Loops permitem repetir código várias vezes.
            
            For loop:
            for item in sequencia:
                # código a repetir
            
            While loop:
            while condição:
                # código a repetir
            
            Exemplos:
            for i in range(5):  # conta de 0 a 4
            for fruta in frutas:  # itera sobre uma lista
            while contador > 0:  # repete até condição ser falsa""")

        self.run_practice("Loops",
            "Crie um for que itera sobre range(3)",
            ["for i in range(3):", "for x in range(3):", "for n in range(3):"],
            example="for i in range(3):",
            dica="Use 'for' seguido de uma variável, 'in range(3)' e dois pontos")

        # Lição 3: Funções
        self.show_lesson("Lição 3: Funções",
            """Funções são blocos de código reutilizáveis.
            
            def nome_funcao(parametro1, parametro2):
                # código da função
                return resultado
            
            Exemplos:
            def somar(a, b):
                return a + b
            
            def saudacao(nome="Mundo"):  # parâmetro com valor padrão
                return f"Olá, {nome}!"
            
            def calcular(*args, **kwargs):  # múltiplos argumentos""")

        self.run_practice("Funções",
            "Crie uma função chamada dobro que recebe x como parâmetro",
            ["def dobro(x):", "def dobro(x): return x * 2", "def dobro(x): return x*2"],
            example="def dobro(x):",
            dica="Use 'def', nome da função, parênteses com parâmetro e dois pontos")

        # Lição 4: Dicionários
        self.show_lesson("Lição 4: Dicionários",
            """Dicionários são estruturas de chave-valor.
            
            pessoa = {
                "nome": "João",
                "idade": 30,
                "cidade": "São Paulo"
            }
            
            Operações comuns:
            - Acessar: dicionario["chave"]
            - Adicionar: dicionario["nova_chave"] = valor
            - Remover: del dicionario["chave"]
            - Verificar: "chave" in dicionario""")

        self.run_practice("Dicionários",
            'Crie um dicionário com a chave "nome" e valor "Ana"',
            ['{"nome": "Ana"}', "{'nome': 'Ana'}", 'dict(nome="Ana")'],
            example='{"nome": "Ana"}',
            dica="Use chaves {} com a chave e valor separados por dois pontos")

        # Lição 5: Tratamento de Exceções
        self.show_lesson("Lição 5: Tratamento de Exceções",
            """Exceções permitem lidar com erros graciosamente.
            
            try:
                # código que pode gerar erro
            except TipoErro:
                # código se der erro
            else:
                # código se não der erro
            finally:
                # código executado sempre
            
            Tipos comuns de exceções:
            - ValueError
            - TypeError
            - IndexError
            - KeyError
            - ZeroDivisionError""")

        self.run_practice("Exceções",
            "Escreva um bloco try-except básico",
            ["try:\n    pass\nexcept:", "try:\n    pass\nexcept Exception:", 
             "try:\n    pass\nexcept Exception as e:"],
            example="try:\n    pass\nexcept:",
            dica="Use 'try:' seguido de 'except:'")

        self.modulos_completos.add("intermediario_completo")

    def executar_licoes_avancado(self):
        # Lição 1: Programação Orientada a Objetos
        self.show_lesson("Módulo Avançado - Em Desenvolvimento",
            """Este módulo está em desenvolvimento e incluirá:
            
            - Programação Orientada a Objetos
            - Decoradores
            - Geradores e Iteradores
            - Concorrência e Paralelismo
            - Testes Unitários
            
            Volte em breve para mais conteúdo!""")
        
        self.modulos_completos.add("avancado_preview")

    def finalizar_tutorial(self):
        self.print_header("Parabéns!")
        print(f"""
        {self.nome_aluno}, você completou o tutorial de Python!
        
        Sua pontuação final: {self.pontuacao}/{self.total_exercicios}
        Percentual de acertos: {(self.pontuacao/self.total_exercicios)*100:.1f}%
        
        Módulos completos: {len(self.modulos_completos)}
        Nível alcançado: {self.nivel_atual.capitalize()}
        
        Tópicos cobertos:
        - Variáveis
        - Operações Matemáticas
        - Strings
        - Listas
        
        Continue praticando e nunca pare de aprender!
        """)
        self.print_loading("Finalizando tutorial")

def main():
    tutorial = Tutorial()
    tutorial.executar_tutorial()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTutorial interrompido pelo usuário. Até a próxima! 👋")
    except Exception as e:
        print(f"\n\nOcorreu um erro inesperado: {e}")
        print("Por favor, reinicie o tutorial.")
