import os
import time
import sys
from typing import Optional, Any, List, Union
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional
import sqlite3
import json
import hashlib

@dataclass
class User:
    id: int
    username: str
    email: str
    progress: Dict
    achievements: List[str]
    xp: int
    streak: int
    last_active: datetime

class PythonTutorial:
    def __init__(self):
        self.db = Database()
        self.auth = Authentication()
        self.analytics = Analytics()
        self.achievements = AchievementSystem()
        self.content = ContentManager()
        self.social = SocialFeatures()
    
    def initialize(self):
        self.db.setup()
        self.load_content()
        self.setup_gui()
    
    def run(self):
        self.show_welcome()
        if self.auth.login_or_register():
            self.main_loop()
    
    def main_loop(self):
        while True:
            self.update_progress()
            self.check_achievements()
            self.show_recommendations()
            self.handle_user_input()
            self.save_analytics()

class Database:
    def setup(self):
        # Implementar esquema do banco de dados
        pass

class Authentication:
    def login_or_register(self) -> bool:
        # Implementar sistema de autenticação
        pass

class Analytics:
    def track_progress(self, user_id: int, action: str):
        # Implementar tracking de ações
        pass

class AchievementSystem:
    def check_achievements(self, user: User):
        # Implementar sistema de conquistas
        pass

class ContentManager:
    def load_modules(self):
        # Carregar conteúdo dinâmico
        pass

class SocialFeatures:
    def handle_social(self):
        # Implementar recursos sociais
        pass

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

    def get_user_input(self, prompt: str, valid_options: Optional[List[str]] = None) -> str:
        while True:
            if '\n' in prompt:
                print(prompt)
                user_input = input(">>> ")
            else:
                user_input = input(f"\n{prompt}: ")
            
            if valid_options and user_input.lower() not in valid_options:
                print(f"\nOpção inválida. Escolha entre: {', '.join(valid_options)}")
                continue
            return user_input

    def get_multiline_input(self, prompt: str) -> str:
        print(f"\n{prompt}")
        print("(Digite seu código e pressione Ctrl+D ou Ctrl+Z (Windows) para finalizar)")
        lines = []
        try:
            while True:
                line = input("... ")
                lines.append(line)
        except EOFError:
            pass
        return '\n'.join(lines)

    def show_lesson(self, topic: str, content: str) -> None:
        self.print_header(topic)
        print(content)
        input("\nPressione ENTER para continuar...")

    def run_practice(self, titulo, pergunta, respostas_validas, example="", dica="", is_multiline=False):
        # Adiciona verificação de espaços em branco e normalização
        def normalizar_codigo(codigo):
            # Remove espaços em branco extras e linhas vazias
            return "\n".join(line.strip() for line in codigo.split("\n") if line.strip())
        
        # Modifica a validação para usar a função normalizar_codigo
        def validar_resposta(resposta, respostas_validas):
            resposta_norm = normalizar_codigo(resposta)
            return any(normalizar_codigo(valid) == resposta_norm for valid in respostas_validas)

        # Resto do código permanece o mesmo
        self.print_header(f"Prática: {titulo}")
        print(f"\n{pergunta}\n")
        if example:
            print(f"Exemplo:\n{example}\n")
        
        tentativas = 3
        while tentativas > 0:
            if dica:
                ver_dica = input("\nDeseja ver uma dica? (s/n)\n>>> ").lower()
                if ver_dica == 's':
                    print(f"\nDica:\n{dica}\n")
            
            print("\nSua resposta:")
            print("(Digite seu código e pressione Ctrl+D ou Ctrl+Z (Windows) para finalizar)")
            
            linhas = []
            try:
                while True:
                    linha = input("... ")
                    linhas.append(linha)
            except (EOFError, KeyboardInterrupt):
                resposta = "\n".join(linhas)
                
            if validar_resposta(resposta, respostas_validas):
                print("\n✅ Correto! Muito bem!")
                self.pontuacao += 1
                return True
            
            tentativas -= 1
            if tentativas > 0:
                print(f"\n❌ Tente novamente! Você ainda tem {tentativas} tentativa(s).")
            else:
                print("\n❌ Não foi dessa vez. A resposta correta seria:")
                print(example)
                return False

    def check_answer(self, user_answer: str, correct_answers: Union[Any, List[Any]], is_multiline: bool = False) -> bool:
        if isinstance(correct_answers, list):
            if is_multiline:
                # Remove espaços em branco extras e normaliza quebras de linha
                user_answer = '\n'.join(line.rstrip() for line in user_answer.splitlines())
                return any(user_answer == '\n'.join(ans.rstrip() for ans in correct.splitlines()) 
                          for correct in correct_answers)
            return user_answer in correct_answers
        return user_answer == correct_answers

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
            "Escreva um bloco try-except básico (use \\n para quebras de linha)",
            ["try:\\n    pass\\nexcept:", 
             "try:\\n    pass\\nexcept Exception:", 
             "try:\\n    pass\\nexcept Exception as e:"],
            example="try:\\n    pass\\nexcept:",
            dica="Digite 'try:\\n    pass\\nexcept:' como uma única linha")

        self.modulos_completos.add("intermediario_completo")

    def executar_licoes_avancado(self):
        # Lição 1: Programação Orientada a Objetos
        self.show_lesson("Lição 1: Programação Orientada a Objetos",
            """Classes são a base da Programação Orientada a Objetos (POO).

            class NomeClasse:
                def __init__(self, parametros):
                    self.atributos = parametros
                
                def metodo(self):
                    return resultado
            
            Conceitos importantes:
            - Encapsulamento: _privado, __muito_privado
            - Herança: class Filha(Pai)
            - Polimorfismo: mesma interface, diferentes implementações
            - Composição: ter vs ser""")

        self.run_practice("Classes",
            "Crie uma classe Pessoa com __init__ recebendo nome e idade",
            ["class Pessoa:\n    def __init__(self, nome, idade):\n        self.nome = nome\n        self.idade = idade",
             "class Pessoa:\n    def __init__(self, nome, idade):\n        self.nome, self.idade = nome, idade"],
            example="class Pessoa:\n    def __init__(self, nome, idade):\n        self.nome = nome\n        self.idade = idade",
            dica="Use class, __init__ com self e defina os atributos",
            is_multiline=True)

        # Lição 2: Decoradores
        self.show_lesson("Lição 2: Decoradores",
            """Decoradores são funções que modificam outras funções.
            
            def meu_decorador(func):
                def wrapper(*args, **kwargs):
                    # código antes
                    resultado = func(*args, **kwargs)
                    # código depois
                    return resultado
                return wrapper
            
            @meu_decorador
            def funcao():
                pass
            
            Decoradores comuns:
            - @property
            - @classmethod
            - @staticmethod
            - @functools.lru_cache""")

        self.run_practice("Decoradores",
            "Crie um decorador que mede o tempo de execução de uma função",
            ["""def medir_tempo(func):
                def wrapper(*args, **kwargs):
                    import time
                    inicio = time.time()
                    resultado = func(*args, **kwargs)
                    fim = time.time()
                    print(f'Tempo: {fim - inicio:.2f}s')
                    return resultado
                return wrapper"""],
            example="def medir_tempo(func):\n    def wrapper(*args, **kwargs):\n        import time\n        inicio = time.time()\n        resultado = func(*args, **kwargs)\n        print(f'Tempo: {time.time() - inicio:.2f}s')\n        return resultado\n    return wrapper",
            dica="Use um decorador com wrapper que mede tempo inicial e final",
            is_multiline=True)

        # Lição 3: Geradores e Iteradores
        self.show_lesson("Lição 3: Geradores e Iteradores",
            """Geradores são funções que geram valores sob demanda.
            
            def gerador():
                yield valor1
                yield valor2
            
            Iteradores implementam __iter__ e __next__
            
            Exemplos:
            - range() é um gerador
            - map() retorna um iterador
            - (x for x in lista) é uma expressão geradora""")

        self.run_practice("Geradores",
            "Crie um gerador de números pares até n",
            ["def pares(n):\n    for i in range(0, n+1, 2):\n        yield i",
             "def pares(n):\n    i = 0\n    while i <= n:\n        yield i\n        i += 2"],
            example="def pares(n):\n    for i in range(0, n+1, 2):\n        yield i",
            dica="Use yield para gerar números pares de 0 até n",
            is_multiline=True)

        # Lição 4: Concorrência e Paralelismo
        self.show_lesson("Lição 4: Concorrência e Paralelismo",
            """Python oferece várias formas de concorrência:
            
            1. threading - para I/O bound
            2. multiprocessing - para CPU bound
            3. asyncio - para I/O bound assíncrono
            
            async def funcao():
                await operacao_async()
            
            with ThreadPoolExecutor() as executor:
                futures = executor.submit(funcao)""")

        self.run_practice("Async",
            "Crie uma função assíncrona que espera n segundos",
            ["async def esperar(n):\n    await asyncio.sleep(n)",
             "async def esperar(n):\n    import asyncio\n    await asyncio.sleep(n)"],
            example="async def esperar(n):\n    await asyncio.sleep(n)",
            dica="Use async def e await asyncio.sleep()",
            is_multiline=True)

        # Lição 5: Testes e Debugging
        self.show_lesson("Lição 5: Testes e Debugging",
            """Testes são essenciais para código confiável.
            
            import unittest
            
            class TesteMeuCodigo(unittest.TestCase):
                def setUp(self):
                    # preparação
                
                def test_funcionalidade(self):
                    self.assertEqual(esperado, resultado)
            
            Tipos de testes:
            - Unitários: unittest, pytest
            - Integração: entre componentes
            - End-to-end: sistema completo""")

        self.run_practice("Testes",
            "Crie um teste unitário para uma função soma(a, b)",
            ["""class TesteSoma(unittest.TestCase):
                def test_soma(self):
                    self.assertEqual(soma(2, 3), 5)
                    self.assertEqual(soma(-1, 1), 0)"""],
            example="class TesteSoma(unittest.TestCase):\n    def test_soma(self):\n        self.assertEqual(soma(2, 3), 5)",
            dica="Crie uma classe de teste que herda de unittest.TestCase",
            is_multiline=True)

        # Lição 6: Design Patterns
        self.show_lesson("Lição 6: Design Patterns",
            """Padrões de projeto são soluções reutilizáveis.
            
            Tipos principais:
            1. Criacionais (Factory, Singleton)
            2. Estruturais (Adapter, Decorator)
            3. Comportamentais (Observer, Strategy)
            
            Exemplo de Singleton:
            class Singleton:
                _instance = None
                def __new__(cls):
                    if cls._instance is None:
                        cls._instance = super().__new__(cls)
                    return cls._instance""")

        self.run_practice("Design Patterns",
            "Implemente o padrão Factory para criar formas geométricas",
            ["""class FormaFactory:
                @staticmethod
                def criar_forma(tipo):
                    if tipo == "circulo":
                        return Circulo()
                    elif tipo == "quadrado":
                        return Quadrado()
                    raise ValueError("Forma inválida")"""],
            example="class FormaFactory:\n    @staticmethod\n    def criar_forma(tipo):\n        if tipo == \"circulo\":\n            return Circulo()",
            dica="Use um método estático que retorna diferentes classes baseado no tipo",
            is_multiline=True)

        self.modulos_completos.add("avancado_completo")

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
