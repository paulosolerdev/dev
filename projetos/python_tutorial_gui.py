import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
import json
import sqlite3
from datetime import datetime
import hashlib
from typing import Dict, List, Optional
from dataclasses import dataclass
import syntax_highlighter
import markdown2
import os

@dataclass
class Exercicio:
    titulo: str
    descricao: str
    codigo_inicial: str
    codigo_resposta: str
    dicas: List[str]
    testes: List[Dict[str, str]]
    pontos: int

@dataclass
class Licao:
    titulo: str
    descricao: str
    conteudo: str
    exemplos: List[str]
    exercicios: List[Exercicio]
    pontos: int
    pre_requisitos: List[int]
    tags: List[str]

class BancoDados:
    def __init__(self):
        self.conn = sqlite3.connect('tutorial_python.db')
        self.criar_tabelas()

    def criar_tabelas(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password_hash TEXT,
                    pontos INTEGER DEFAULT 0,
                    nivel INTEGER DEFAULT 1,
                    data_cadastro TEXT,
                    ultimo_acesso TEXT
                )
            ''')
            
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS progresso (
                    usuario_id INTEGER,
                    licao_id INTEGER,
                    exercicio_id INTEGER,
                    completado INTEGER,
                    codigo_salvo TEXT,
                    pontos INTEGER,
                    data_conclusao TEXT,
                    tempo_gasto INTEGER,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
                )
            ''')

    def salvar_progresso(self, usuario_id: int, dados: dict):
        with self.conn:
            self.conn.execute(
                '''INSERT OR REPLACE INTO progresso 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (usuario_id, dados['licao_id'], dados['exercicio_id'],
                 dados['completado'], dados['codigo_salvo'],
                 dados['pontos'], dados['data_conclusao'],
                 dados['tempo_gasto'])
            )

class TutorialGUI:
    def __init__(self):
        # Criar a janela principal
        self.root = tk.Tk()
        self.root.title("Tutorial Python")
        self.root.geometry("1024x768")
        
        # IMPORTANTE: Inicializar o ThemedStyle antes de qualquer outra configuração de estilo
        self.style = ThemedStyle(self.root)
        
        # Inicializar o dicionário de usuário
        self.usuario = {
            "nome": "",
            "nivel": 1,
            "pontos": 0,
            "exercicios_completos": set(),
            "licoes_completas": set(),
            "ultima_sessao": None
        }
        
        # Inicializar o estado atual
        self.estado_atual = {
            "licao_atual": None,
            "exercicio_atual": None
        }
        
        # Configurar estilos
        self.setup_estilos()
        
        # Carregar configurações
        self.carregar_configuracoes()
        
        # Carregar conteúdo das lições
        self.carregar_conteudo()
        
        # Inicializar banco de dados
        try:
            self.conn = sqlite3.connect('tutorial.db')
            self.cursor = self.conn.cursor()
            
            # Criar tabelas necessárias
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    nivel INTEGER DEFAULT 1,
                    pontos INTEGER DEFAULT 0,
                    ultima_sessao TEXT
                )
            ''')
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS progresso (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER,
                    licao_id INTEGER,
                    exercicio_id INTEGER,
                    completado INTEGER,
                    codigo_salvo TEXT,
                    pontos INTEGER,
                    data_conclusao TEXT,
                    tempo_gasto INTEGER,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
                )
            ''')
            
            self.conn.commit()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {str(e)}")
        
        # Criar interface principal
        self.criar_interface()

    def executar(self):
        """Inicia a execução do tutorial"""
        self.root.mainloop()

    def setup_estilos(self):
        """Configura os estilos e temas da interface"""
        # Cores
        self.cores = {
            'primaria': '#2196F3',
            'secundaria': '#FFC107',
            'sucesso': '#4CAF50',
            'erro': '#F44336',
            'fundo': '#FAFAFA',
            'texto': '#212121',
            'texto_secundario': '#757575',
            'destaque': '#E3F2FD'
        }
        
        # Fontes
        self.fontes = {
            'titulo': ('Roboto', 24, 'bold'),
            'subtitulo': ('Roboto', 18),
            'texto': ('Roboto', 12),
            'codigo': ('Fira Code', 12),
            'botao': ('Roboto', 10, 'bold')
        }
        
        # Configurar estilos personalizados
        self.style.configure(
            "Primario.TButton",
            font=self.fontes['botao'],
            background=self.cores['primaria'],
            foreground='white'
        )
        
        self.style.configure(
            "Secundario.TButton",
            font=self.fontes['botao'],
            background=self.cores['secundaria']
        )

    def setup_variaveis(self):
        """Inicializa variáveis de estado e controle"""
        self.estado_atual = {
            "usuario": None,
            "licao_atual": None,
            "exercicio_atual": 0,
            "tempo_inicio": None,
            "codigo_salvo": {},
            "historico": []
        }
        
        self.cache = {
            "resultados_exercicios": {},
            "dicas_mostradas": set(),
            "exercicios_completos": set()
        }

    def criar_widgets_principais(self):
        """Cria os widgets principais da interface"""
        # Barra de ferramentas
        self.toolbar = tk.Frame(self.root, bg=self.cores['primaria'])
        self.toolbar.pack(fill=tk.X)
        
        # Botões da barra de ferramentas
        self.criar_botoes_toolbar()
        
        # Barra de status
        self.statusbar = tk.Frame(self.root, bg=self.cores['fundo'])
        self.statusbar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(
            self.statusbar,
            text="Pronto",
            bg=self.cores['fundo']
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Indicador de progresso
        self.progress_var = tk.DoubleVar()
        self.progressbar = ttk.Progressbar(
            self.statusbar,
            variable=self.progress_var,
            mode='determinate'
        )
        self.progressbar.pack(side=tk.RIGHT, padx=5)

    def criar_botoes_toolbar(self):
        """Cria os botões da barra de ferramentas"""
        botoes = [
            ("Início", self.mostrar_menu_principal),
            ("Perfil", self.mostrar_perfil),
            ("Ranking", self.mostrar_ranking),
            ("Configurações", self.mostrar_configuracoes),
            ("Ajuda", self.mostrar_ajuda)
        ]
        
        for texto, comando in botoes:
            btn = ttk.Button(
                self.toolbar,
                text=texto,
                command=comando,
                style="Toolbar.TButton"
            )
            btn.pack(side=tk.LEFT, padx=5, pady=2)

    def mostrar_perfil(self):
        """Exibe a tela de perfil do usuário"""
        self.limpar_tela()
        if not self.estado_atual["usuario"]:
            self.mostrar_login()
            return
            
        usuario = self.estado_atual["usuario"]
        
        # Cabeçalho do perfil
        header = tk.Frame(self.scrollable_frame)
        header.pack(fill=tk.X, pady=20)
        
        # Avatar e informações básicas
        avatar_frame = tk.Frame(header)
        avatar_frame.pack(side=tk.LEFT, padx=20)
        
        # Estatísticas
        stats_frame = tk.Frame(self.scrollable_frame)
        stats_frame.pack(fill=tk.X, pady=20)
        
        stats = self.db.get_estatisticas_usuario(usuario["id"])
        self.criar_widget_estatisticas(stats_frame, stats)
        
        # Progresso nas lições
        self.mostrar_progresso_licoes()

    def mostrar_exercicio(self, exercicio: Exercicio):
        """Mostra um exercício específico"""
        self.limpar_tela()
        
        # Cabeçalho
        tk.Label(
            self.scrollable_frame,
            text=exercicio.titulo,
            font=self.fontes['titulo'],
            fg=self.cores['primaria']
        ).pack(pady=20)
        
        # Descrição com suporte a Markdown
        descricao_html = markdown2.markdown(exercicio.descricao)
        descricao_widget = tk.Label(
            self.scrollable_frame,
            text=descricao_html,
            font=self.fontes['texto'],
            wraplength=800,
            justify=tk.LEFT
        )
        descricao_widget.pack(pady=10, padx=20, anchor='w')
        
        # Editor de código
        self.criar_editor_codigo(exercicio)
        
        # Console de saída
        self.criar_console_saida()
        
        # Botões de ação
        self.criar_botoes_exercicio(exercicio)

    def criar_editor_codigo(self, exercicio: Exercicio):
        """Cria o editor de código com syntax highlighting"""
        editor_frame = tk.Frame(self.scrollable_frame)
        editor_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Números de linha
        line_numbers = tk.Text(
            editor_frame,
            width=4,
            padx=3,
            takefocus=0,
            border=0,
            background='lightgray',
            state='disabled'
        )
        line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Editor principal
        self.codigo_editor = tk.Text(
            editor_frame,
            font=self.fontes['codigo'],
            wrap=tk.NONE,
            undo=True
        )
        self.codigo_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbars
        self.adicionar_scrollbars(editor_frame, self.codigo_editor)
        
        # Configurar syntax highlighting
        self.syntax_highlighter = syntax_highlighter.PythonHighlighter(self.codigo_editor)
        
        # Inserir código inicial
        self.codigo_editor.insert('1.0', exercicio.codigo_inicial)
        self.atualizar_numeros_linha()
        
        # Bindings
        self.codigo_editor.bind('<Key>', self.atualizar_numeros_linha)
        self.codigo_editor.bind('<Control-z>', self.desfazer)
        self.codigo_editor.bind('<Control-y>', self.refazer)

    def executar_codigo(self):
        """Executa o código do usuário em um ambiente seguro"""
        codigo = self.codigo_editor.get('1.0', 'end-1c')
        
        try:
            # Criar um ambiente de execução isolado
            namespace = {}
            
            # Redirecionar stdout para capturar a saída
            import sys
            from io import StringIO
            stdout_original = sys.stdout
            sys.stdout = StringIO()
            
            # Executar o código
            exec(codigo, namespace)
            
            # Capturar a saída
            output = sys.stdout.getvalue()
            
            # Restaurar stdout
            sys.stdout = stdout_original
            
            # Mostrar resultado
            self.console_output.config(fg=self.cores['texto'])
            self.console_output.delete('1.0', 'end')
            self.console_output.insert('1.0', output)
            
        except Exception as e:
            # Mostrar erro
            self.console_output.config(fg=self.cores['erro'])
            self.console_output.delete('1.0', 'end')
            self.console_output.insert('1.0', f"Erro: {str(e)}")

    def verificar_resposta(self, exercicio: Exercicio):
        """Verifica a resposta do usuário executando os testes"""
        codigo = self.codigo_editor.get('1.0', 'end-1c')
        
        # Criar ambiente isolado para testes
        namespace = {}
        
        try:
            # Executar o código do usuário
            exec(codigo, namespace)
            
            # Verificar se houve erro de sintaxe
            if not codigo.strip():
                messagebox.showerror("Erro", "Por favor, digite seu código")
                return False
            
            # Executar os testes do exercício
            for teste in exercicio.testes:
                try:
                    # Preparar ambiente de teste
                    resultado = eval(teste['teste'], namespace)
                    esperado = eval(teste['esperado'])
                    
                    # Comparação mais flexível para listas
                    if isinstance(resultado, list) and isinstance(esperado, list):
                        if sorted(resultado) != sorted(esperado):
                            messagebox.showerror(
                                "Teste Falhou",
                                f"Teste: {teste['descricao']}\n"
                                f"Esperado: {esperado}\n"
                                f"Seu resultado: {resultado}\n\n"
                                "Dica: Verifique se sua lista contém os elementos corretos."
                            )
                            return False
                    # Comparação para outros tipos
                    elif resultado != esperado:
                        messagebox.showerror(
                            "Teste Falhou",
                            f"Teste: {teste['descricao']}\n"
                            f"Esperado: {esperado}\n"
                            f"Seu resultado: {resultado}"
                        )
                        return False
                    
                except Exception as e:
                    messagebox.showerror(
                        "Erro na Execução",
                        f"Erro ao executar teste: {teste['descricao']}\n"
                        f"Erro: {str(e)}\n\n"
                        "Dica: Verifique se você definiu todas as variáveis necessárias."
                    )
                    return False
            
            # Se chegou aqui, todos os testes passaram
            messagebox.showinfo("Sucesso!", "Parabéns! Sua resposta está correta!")
            self.exercicio_completo(exercicio)
            return True
        
        except SyntaxError as e:
            messagebox.showerror(
                "Erro de Sintaxe",
                f"Há um erro de sintaxe no seu código:\n{str(e)}\n\n"
                "Dica: Verifique se todos os parênteses e colchetes estão fechados corretamente."
            )
            return False
        except Exception as e:
            messagebox.showerror(
                "Erro",
                f"Ocorreu um erro ao executar seu código:\n{str(e)}\n\n"
                "Dica: Verifique se você está usando os nomes corretos das variáveis."
            )
            return False

    def exercicio_completo(self, exercicio: Exercicio):
        """Processa a conclusão bem-sucedida de um exercício"""
        # Atualizar pontuação
        self.estado_atual["usuario"]["pontos"] += exercicio.pontos
        
        # Registrar conclusão
        self.cache["exercicios_completos"].add(exercicio.titulo)
        
        # Calcular tempo gasto
        tempo_gasto = (datetime.now() - self.estado_atual["tempo_inicio"]).seconds
        
        # Salvar progresso
        self.db.salvar_progresso(
            self.estado_atual["usuario"]["id"],
            {
                "licao_id": self.estado_atual["licao_atual"],
                "exercicio_id": self.estado_atual["exercicio_atual"],
                "completado": 1,
                "codigo_salvo": self.codigo_editor.get('1.0', 'end-1c'),
                "pontos": exercicio.pontos,
                "data_conclusao": datetime.now().isoformat(),
                "tempo_gasto": tempo_gasto
            }
        )
        
        # Mostrar parabéns
        self.mostrar_parabens(exercicio.pontos, tempo_gasto)
        
        # Avançar para próximo exercício
        self.estado_atual["exercicio_atual"] += 1
        self.mostrar_proximo_exercicio()

    def mostrar_parabens(self, pontos: int, tempo_gasto: int):
        """Mostra uma janela de parabéns ao completar um exercício"""
        top = tk.Toplevel(self.root)
        top.title("Parabéns!")
        top.geometry("400x300")
        
        # Adicionar animação de confete
        self.animar_confete(top)
        
        tk.Label(
            top,
            text="🎉 Exercício Completo! 🎉",
            font=self.fontes['titulo'],
            fg=self.cores['sucesso']
        ).pack(pady=20)
        
        tk.Label(
            top,
            text=f"Você ganhou {pontos} pontos!",
            font=self.fontes['subtitulo']
        ).pack(pady=10)
        
        tk.Label(
            top,
            text=f"Tempo: {tempo_gasto//60}m {tempo_gasto%60}s",
            font=self.fontes['texto']
        ).pack(pady=5)
        
        ttk.Button(
            top,
            text="Continuar",
            style="Primario.TButton",
            command=top.destroy
        ).pack(pady=20)

    def animar_confete(self, window):
        """Cria uma animação de confete"""
        canvas = tk.Canvas(window, width=400, height=300)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        confetes = []
        cores = ['red', 'blue', 'yellow', 'green', 'purple', 'orange']
        
        for _ in range(50):
            x = random.randint(0, 400)
            confetes.append({
                'id': canvas.create_oval(x, 0, x+5, 5, fill=random.choice(cores)),
                'speed': random.uniform(1, 3),
                'x': random.uniform(-1, 1)
            })
        
        def update_confete():
            for conf in confetes:
                canvas.move(conf['id'], conf['x'], conf['speed'])
                pos = canvas.coords(conf['id'])
                if pos[1] > 300:
                    canvas.moveto(conf['id'], random.randint(0, 400), 0)
            window.after(20, update_confete)
        
        update_confete()

    def setup_janela(self):
        """Configura a janela principal"""
        # Usar a janela root já existente ao invés de criar uma nova
        if not hasattr(self, 'root'):
            self.root = tk.Tk()
        
        self.root.title("Tutorial Python Interativo")
        self.root.geometry("1024x768")
        self.root.minsize(800, 600)
        
        # Canvas principal com scrollbar
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.main_frame, width=1024, height=768)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # Configurar o scrollable frame no canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Configurar o canvas e a scrollbar
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Posicionar os elementos
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configurar o scroll com o mouse
        self.scrollable_frame.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollable_frame.bind('<Leave>', self._unbound_to_mousewheel)

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def setup_variaveis(self):
        """Inicializa variáveis de estado"""
        self.usuario = {
            "nome": "",
            "nivel": 1,
            "pontos": 0,
            "exercicios_completos": set(),
            "licoes_completas": set(),
            "ultima_sessao": None
        }
        
        self.estado_atual = {
            "licao_atual": None,
            "exercicio_atual": None,
            "tentativas": 0,
            "tempo_inicio": None
        }
        
        self.widgets = {}
        self.animacoes = {}

    def setup_banco_dados(self):
        """Configura o banco de dados SQLite"""
        self.conn = sqlite3.connect('tutorial_python.db')
        self.cursor = self.conn.cursor()
        
        # Criar tabelas se não existirem
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                nivel INTEGER,
                pontos INTEGER,
                ultima_sessao TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS progresso (
                usuario_id INTEGER,
                licao_id INTEGER,
                exercicio_id INTEGER,
                completado INTEGER,
                data_conclusao TEXT,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        
        self.conn.commit()

    def carregar_conteudo(self):
        """Carrega o conteúdo das lições e exercícios"""
        self.licoes = {
            1: Licao(
                titulo="Fundamentos de Python",
                descricao="Conceitos básicos da linguagem Python",
                conteudo="""
                Python é uma linguagem de programação de alto nível, interpretada e de propósito geral.
                
                Características principais:
                • Sintaxe clara e legível
                • Tipagem dinâmica
                • Gerenciamento automático de memória
                • Rica biblioteca padrão
                • Grande comunidade e ecossistema
                
                Nesta lição você aprenderá:
                1. Como criar e usar variáveis
                2. Tipos de dados básicos
                3. Operadores aritméticos e lógicos
                4. Comentários e documentação
                """,
                exemplos=[
                    "# Variáveis e tipos básicos\nx = 10\nnome = 'Python'\nativa = True\n\n# Operações básicas\ny = x + 5\nprint(f'Resultado: {y}')",
                    "# Diferentes tipos de dados\ninteiro = 42\ndecimal = 3.14\ntexto = 'Olá'\nlista = [1, 2, 3]\n\nprint(type(inteiro))\nprint(type(decimal))",
                    "# Operadores aritméticos\nsoma = 10 + 5\nsubtracao = 10 - 5\nmultiplicacao = 10 * 5\ndivisao = 10 / 5"
                ],
                exercicios=[
                    Exercicio(
                        titulo="Criando Variáveis",
                        descricao="Crie uma variável chamada 'mensagem' com o texto 'Olá, Python!'\n\n# Criando a primeira variável\nmensagem = 'Olá, Python!'\n\n# Mostrando o valor da variável\nprint(mensagem)",
                        codigo_inicial="# Digite seu código aqui",
                        codigo_resposta="mensagem = 'Olá, Python!'\nprint(mensagem)",
                        dicas=["Use o operador = para atribuição", "Strings podem usar aspas simples ou duplas"],
                        testes=[{"entrada": "", "saida": "Olá, Python!"}],
                        pontos=10
                    ),
                    Exercicio(
                        titulo="Operações Matemáticas",
                        descricao="Crie duas variáveis numéricas e realize uma multiplicação entre elas\n\n# Criando a primeira variável numérica\nnumero1 = 2\n\n# Criando a segunda variável numérica\nnumero2 = 3\n\n# Realizando a multiplicação e guardando o resultado em uma variável\nresultado = numero1 * numero2\n\n# Mostrando o resultado da multiplicação\nprint(f'A multiplicação de {numero1} x {numero2} = {resultado}')",
                        codigo_inicial="# Crie as variáveis e faça a multiplicação\n",
                        codigo_resposta="numero1 = 2\nnumero2 = 3\nresultado = numero1 * numero2\nprint(f'A multiplicação de {numero1} x {numero2} = {resultado}')",
                        dicas=["Use o operador * para multiplicação", "Você pode escolher quaisquer números"],
                        testes=[{"entrada": "", "saida": "A multiplicação de 2 x 3 = 6"}],
                        pontos=15
                    ),
                    Exercicio(
                        titulo="Strings e Formatação",
                        descricao="Use f-strings para criar uma mensagem formatada\n\n# Definindo as variáveis\nnome = 'Python'\nversao = 3.9\n\n# Criando a mensagem formatada\nmensagem = f'Linguagem {nome} versão {versao}'\n\n# Mostrando a mensagem formatada\nprint(mensagem)",
                        codigo_inicial="nome = 'Python'\nversao = 3.9\n# Crie a mensagem formatada\n",
                        codigo_resposta="nome = 'Python'\nversao = 3.9\nmensagem = f'Linguagem {nome} versão {versao}'\nprint(mensagem)",
                        dicas=["Use f antes das aspas para criar uma f-string", "Use chaves {} para inserir variáveis"],
                        testes=[{"entrada": "", "saida": "Linguagem Python versão 3.9"}],
                        pontos=20
                    )
                ],
                pontos=50,
                pre_requisitos=[],
                tags=["básico", "iniciante", "variáveis"]
            ),
            2: Licao(
                titulo="Estruturas de Dados",
                descricao="Listas, tuplas, dicionários e conjuntos em Python",
                conteudo="""
                Python oferece várias estruturas de dados poderosas:
                
                1. Listas []:
                   • Sequências mutáveis e ordenadas
                   • Podem conter diferentes tipos de dados
                   • Métodos: append(), remove(), pop(), etc.
                
                2. Tuplas ():
                   • Sequências imutáveis
                   • Mais eficientes que listas
                   • Úteis para dados que não devem mudar
                
                3. Dicionários {}:
                   • Mapeamentos chave-valor
                   • Acesso rápido por chave
                   • Muito versáteis e amplamente usados
                
                4. Conjuntos set():
                   • Coleções não ordenadas de elementos únicos
                   • Operações matemáticas de conjuntos
                   • Eliminação automática de duplicatas
                """,
                exemplos=[
                    "# Listas\nfrutas = ['maçã', 'banana', 'laranja']\nfrutas.append('uva')\nprint(frutas[0])  # primeiro elemento",
                    "# Dicionários\ncontato = {'nome': 'Ana', 'idade': 25}\ncontato['email'] = 'ana@email.com'\nprint(contato.keys())",
                    "# Conjuntos\nnumeros = {1, 2, 3, 2, 1}  # duplicatas são removidas\nprint(numeros)\nnumeros.add(4)"
                ],
                exercicios=[
                    Exercicio(
                        titulo="Manipulação de Listas",
                        descricao="Crie uma lista de números e adicione um novo número ao final",
                        codigo_inicial="# Crie a lista e adicione um número\n",
                        codigo_resposta="numeros = [1, 2, 3]\nnumeros.append(4)",
                        dicas=["Use [] para criar a lista", "Use o método append() para adicionar elementos"],
                        testes=[{"entrada": "", "saida": ""}],
                        pontos=15
                    ),
                    Exercicio(
                        titulo="Trabalhando com Dicionários",
                        descricao="Crie um dicionário com informações de uma pessoa",
                        codigo_inicial="# Crie o dicionário com nome e idade\n",
                        codigo_resposta="pessoa = {'nome': 'João', 'idade': 30}",
                        dicas=["Use {} para criar o dicionário", "Use aspas para as chaves de texto"],
                        testes=[{"entrada": "", "saida": ""}],
                        pontos=20
                    )
                ],
                pontos=50,
                pre_requisitos=[1],
                tags=["estruturas de dados", "listas", "dicionários"]
            ),
            3: Licao(
                titulo="Controle de Fluxo",
                descricao="Estruturas condicionais e loops em Python",
                conteudo="""
                O controle de fluxo permite que seu programa tome decisões e repita ações:
                
                1. Estruturas Condicionais:
                   • if, elif, else
                   • Operadores de comparação
                   • Operadores lógicos (and, or, not)
                
                2. Loops:
                   • for: para iteração definida
                   • while: para iteração com condição
                   • break e continue
                   • List comprehensions
                """,
                exemplos=[
                    "# If-elif-else\nidade = 18\nif idade >= 18:\n    print('Maior de idade')\nelse:\n    print('Menor de idade')",
                    "# Loop for\nfor i in range(5):\n    print(i)\n\n# Com lista\nfor fruta in ['maçã', 'banana']:\n    print(fruta)",
                    "# While\ncontador = 0\nwhile contador < 5:\n    print(contador)\n    contador += 1"
                ],
                exercicios=[
                    Exercicio(
                        titulo="Estrutura Condicional",
                        descricao="Crie um if-else para verificar se um número é positivo ou negativo",
                        codigo_inicial="numero = 10\n# Escreva sua condição\n",
                        codigo_resposta="numero = 10\nif numero > 0:\n    print('Positivo')\nelse:\n    print('Negativo')",
                        dicas=["Use > para maior que", "Não esqueça dos dois pontos :"],
                        testes=[{"entrada": "", "saida": ""}],
                        pontos=20
                    ),
                    Exercicio(
                        titulo="Loop For",
                        descricao="Crie um loop que imprima os números de 1 a 5",
                        codigo_inicial="# Escreva seu loop\n",
                        codigo_resposta="for i in range(1, 6):\n    print(i)",
                        dicas=["Use range() para gerar sequência", "range(1, 6) vai de 1 até 5"],
                        testes=[{"entrada": "", "saida": ""}],
                        pontos=20
                    )
                ],
                pontos=60,
                pre_requisitos=[1, 2],
                tags=["controle de fluxo", "condicionais", "loops"]
            )
        }

    def setup_estilos(self):
        """Configura os estilos visuais"""
        self.style = ttk.Style()
        
        # Cores
        self.cores = {
            'primaria': '#2196F3',
            'secundaria': '#FFC107',
            'sucesso': '#4CAF50',
            'erro': '#F44336',
            'fundo': '#F5F5F5',
            'texto': '#212121',
            'texto_secundario': '#757575'
        }
        
        # Fontes
        self.fontes = {
            'titulo': ('Helvetica', 24, 'bold'),
            'subtitulo': ('Helvetica', 18, 'bold'),
            'texto': ('Helvetica', 12),
            'codigo': ('Courier', 12),
            'botao': ('Helvetica', 10, 'bold')
        }
        
        # Estilos dos botões
        self.style.configure(
            "Primario.TButton",
            padding=10,
            relief="flat",
            background=self.cores['primaria'],
            foreground='white'
        )
        
        self.style.configure(
            "Secundario.TButton",
            padding=8,
            relief="flat",
            background=self.cores['secundaria']
        )

    def criar_tela_inicial(self):
        """Cria a tela inicial do tutorial"""
        self.limpar_tela()
        
        # Cabeçalho
        header = tk.Frame(self.scrollable_frame, bg=self.cores['fundo'])
        header.pack(fill=tk.X, pady=20)
        
        tk.Label(
            header,
            text="Tutorial Python Interativo",
            font=self.fontes['titulo'],
            fg=self.cores['primaria'],
            bg=self.cores['fundo']
        ).pack()
        
        tk.Label(
            header,
            text="Aprenda Python de forma prática e interativa",
            font=self.fontes['subtitulo'],
            fg=self.cores['texto_secundario'],
            bg=self.cores['fundo']
        ).pack(pady=10)
        
        # Área de login/registro
        login_frame = tk.Frame(self.scrollable_frame, bg=self.cores['fundo'])
        login_frame.pack(pady=30)
        
        tk.Label(
            login_frame,
            text="Digite seu nome para começar:",
            font=self.fontes['texto'],
            bg=self.cores['fundo']
        ).pack(pady=5)
        
        nome_entry = ttk.Entry(login_frame, width=30)
        nome_entry.pack(pady=5)
        
        ttk.Button(
            login_frame,
            text="Começar",
            style="Primario.TButton",
            command=lambda: self.iniciar_tutorial(nome_entry.get())
        ).pack(pady=10)
        
        # Informações adicionais
        info_frame = tk.Frame(self.scrollable_frame, bg=self.cores['fundo'])
        info_frame.pack(fill=tk.X, pady=20)
        
        features = [
            "✓ Conteúdo interativo",
            "✓ Exercícios práticos",
            "✓ Feedback instantâneo",
            "✓ Acompanhamento de progresso",
            "✓ Certificado de conclusão"
        ]
        
        for feature in features:
            tk.Label(
                info_frame,
                text=feature,
                font=self.fontes['texto'],
                fg=self.cores['texto'],
                bg=self.cores['fundo']
            ).pack(pady=5)

    def limpar_tela(self):
        """Limpa todos os widgets da tela"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def iniciar_tutorial(self, nome):
        """Inicia o tutorial para um usuário"""
        if not nome.strip():
            messagebox.showerror("Erro", "Por favor, digite seu nome")
            return
        
        self.usuario["nome"] = nome
        self.usuario["ultima_sessao"] = datetime.now().isoformat()
        
        # Inicializa o banco de dados se necessário
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    nivel INTEGER DEFAULT 1,
                    pontos INTEGER DEFAULT 0,
                    ultima_sessao TEXT
                )
            ''')
            
            # Verifica se o usuário já existe
            self.cursor.execute('SELECT id FROM usuarios WHERE nome = ?', (nome,))
            resultado = self.cursor.fetchone()
            
            if resultado:
                self.usuario['id'] = resultado[0]
            else:
                # Insere novo usuário
                self.cursor.execute('''
                    INSERT INTO usuarios (nome, nivel, pontos, ultima_sessao)
                    VALUES (?, ?, ?, ?)
                ''', (
                    self.usuario['nome'],
                    self.usuario['nivel'],
                    self.usuario['pontos'],
                    self.usuario['ultima_sessao']
                ))
                self.usuario['id'] = self.cursor.lastrowid
            
            self.conn.commit()
            self.mostrar_menu_principal()
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inicializar banco de dados: {str(e)}")

    def salvar_progresso(self):
        """Salva o progresso do usuário no banco de dados"""
        if not hasattr(self.usuario, 'id'):
            return
        
        try:
            self.cursor.execute('''
                UPDATE usuarios 
                SET nivel = ?, pontos = ?, ultima_sessao = ?
                WHERE id = ?
            ''', (
                self.usuario['nivel'],
                self.usuario['pontos'],
                datetime.now().isoformat(),
                self.usuario['id']
            ))
            
            if self.estado_atual['licao_atual'] and self.estado_atual['exercicio_atual']:
                self.cursor.execute('''
                    INSERT INTO progresso (
                        usuario_id, licao_id, exercicio_id, completado,
                        codigo_salvo, pontos, data_conclusao, tempo_gasto
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    self.usuario['id'],
                    self.estado_atual['licao_atual'],
                    self.estado_atual['exercicio_atual'],
                    1,  # completado
                    '',  # código salvo
                    self.usuario['pontos'],
                    datetime.now().isoformat(),
                    0  # tempo gasto
                ))
            
            self.conn.commit()
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar progresso: {str(e)}")

    def mostrar_menu_principal(self):
        """Mostra o menu principal com as lições disponíveis"""
        self.limpar_tela()
        
        # Cabeçalho
        tk.Label(
            self.scrollable_frame,
            text=f"Bem-vindo(a), {self.usuario['nome']}!",
            font=self.fontes['titulo'],
            fg=self.cores['primaria']
        ).pack(pady=20)
        
        # Status do usuário
        status_frame = tk.Frame(self.scrollable_frame)
        status_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            status_frame,
            text=f"Nível: {self.usuario['nivel']} | Pontos: {self.usuario['pontos']}",
            font=self.fontes['subtitulo']
        ).pack()
        
        # Lista de lições
        licoes_frame = tk.Frame(self.scrollable_frame)
        licoes_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        for licao_id, licao in self.licoes.items():
            self.criar_card_licao(licoes_frame, licao_id, licao)

    def criar_card_licao(self, parent, licao_id, licao):
        """Cria um card para uma lição"""
        card = tk.Frame(
            parent,
            relief=tk.RAISED,
            borderwidth=1
        )
        card.pack(fill=tk.X, pady=5, padx=20)
        
        tk.Label(
            card,
            text=f"Lição {licao_id}: {licao.titulo}",
            font=self.fontes['subtitulo']
        ).pack(pady=5)
        
        tk.Label(
            card,
            text=licao.descricao,
            font=self.fontes['texto']
        ).pack(pady=5)
        
        ttk.Button(
            card,
            text="Iniciar Lição",
            style="Primario.TButton",
            command=lambda: self.mostrar_licao(licao_id)
        ).pack(pady=10)

    def mostrar_licao(self, licao_id):
        """Mostra o conteúdo de uma lição específica"""
        self.limpar_tela()
        licao = self.licoes[licao_id]
        
        # Cabeçalho da lição
        header = tk.Frame(self.scrollable_frame, bg=self.cores['fundo'])
        header.pack(fill=tk.X, pady=20)
        
        tk.Label(
            header,
            text=f"Lição {licao_id}: {licao.titulo}",
            font=self.fontes['titulo'],
            fg=self.cores['primaria'],
            bg=self.cores['fundo']
        ).pack()
        
        # Descrição
        tk.Label(
            self.scrollable_frame,
            text=licao.descricao,
            font=self.fontes['subtitulo'],
            fg=self.cores['texto_secundario'],
            wraplength=800
        ).pack(pady=10)
        
        # Conteúdo principal
        content_frame = tk.Frame(self.scrollable_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=40)
        
        tk.Label(
            content_frame,
            text=licao.conteudo,
            font=self.fontes['texto'],
            justify=tk.LEFT,
            wraplength=800
        ).pack(anchor='w')
        
        # Exemplos
        if licao.exemplos:
            tk.Label(
                content_frame,
                text="\nExemplos:",
                font=self.fontes['subtitulo'],
            ).pack(anchor='w', pady=(20, 10))
            
            for exemplo in licao.exemplos:
                exemplo_frame = tk.Frame(
                    content_frame,
                    bg=self.cores['fundo'],
                    padx=10,
                    pady=10
                )
                exemplo_frame.pack(fill=tk.X, pady=5)
                
                tk.Label(
                    exemplo_frame,
                    text=exemplo,
                    font=self.fontes['codigo'],
                    bg=self.cores['fundo'],
                    justify=tk.LEFT
                ).pack(anchor='w')
        
        # Botões de navegação
        nav_frame = tk.Frame(self.scrollable_frame)
        nav_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(
            nav_frame,
            text="Voltar ao Menu",
            style="Secundario.TButton",
            command=self.mostrar_menu_principal
        ).pack(side=tk.LEFT, padx=20)
        
        if licao.exercicios:
            ttk.Button(
                nav_frame,
                text="Iniciar Exercícios",
                style="Primario.TButton",
                command=lambda: self.mostrar_exercicios(licao_id)
            ).pack(side=tk.RIGHT, padx=20)

    def mostrar_exercicios(self, licao_id):
        """Mostra os exercícios de uma lição"""
        self.limpar_tela()
        licao = self.licoes[licao_id]
        self.estado_atual["licao_atual"] = licao_id
        self.estado_atual["exercicio_atual"] = 0
        
        # Mostrar primeiro exercício
        self.mostrar_proximo_exercicio()

    def mostrar_proximo_exercicio(self):
        """Mostra o próximo exercício da lição atual"""
        licao = self.licoes[self.estado_atual["licao_atual"]]
        exercicio_idx = self.estado_atual["exercicio_atual"]
        
        if exercicio_idx >= len(licao.exercicios):
            # Todos os exercícios foram completados
            self.finalizar_licao()
            return
        
        exercicio = licao.exercicios[exercicio_idx]
        
        # Cabeçalho do exercício
        tk.Label(
            self.scrollable_frame,
            text=f"Exercício: {exercicio.titulo}",
            font=self.fontes['titulo'],
            fg=self.cores['primaria']
        ).pack(pady=20)
        
        # Descrição
        tk.Label(
            self.scrollable_frame,
            text=exercicio.descricao,
            font=self.fontes['texto'],
            wraplength=800
        ).pack(pady=10)
        
        # Área de código
        codigo_frame = tk.Frame(self.scrollable_frame)
        codigo_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        codigo_text = tk.Text(
            codigo_frame,
            font=self.fontes['codigo'],
            height=10,
            width=60
        )
        codigo_text.insert('1.0', exercicio.codigo_inicial)
        codigo_text.pack()
        
        # Botões
        botoes_frame = tk.Frame(self.scrollable_frame)
        botoes_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(
            botoes_frame,
            text="Verificar Resposta",
            style="Primario.TButton",
            command=lambda: self.verificar_resposta(codigo_text.get('1.0', 'end-1c'))
        ).pack(side=tk.RIGHT, padx=20)
        
        ttk.Button(
            botoes_frame,
            text="Voltar à Lição",
            style="Secundario.TButton",
            command=lambda: self.mostrar_licao(self.estado_atual["licao_atual"])
        ).pack(side=tk.LEFT, padx=20)

    def verificar_resposta(self, codigo_usuario):
        """Verifica a resposta do usuário para o exercício atual"""
        licao = self.licoes[self.estado_atual["licao_atual"]]
        exercicio = licao.exercicios[self.estado_atual["exercicio_atual"]]
        
        # Aqui você pode implementar a lógica de verificação do código
        # Por enquanto, vamos apenas comparar com a resposta esperada
        if codigo_usuario.strip() == exercicio.codigo_resposta.strip():
            messagebox.showinfo("Sucesso!", "Resposta correta! Parabéns!")
            self.usuario["pontos"] += exercicio.pontos
            self.estado_atual["exercicio_atual"] += 1
            self.salvar_progresso()
            self.mostrar_proximo_exercicio()
        else:
            messagebox.showerror("Erro", "Resposta incorreta. Tente novamente!")

    def finalizar_licao(self):
        """Finaliza a lição atual e mostra o resumo"""
        self.limpar_tela()
        licao = self.licoes[self.estado_atual["licao_atual"]]
        
        tk.Label(
            self.scrollable_frame,
            text="Parabéns! Você completou a lição!",
            font=self.fontes['titulo'],
            fg=self.cores['sucesso']
        ).pack(pady=20)
        
        tk.Label(
            self.scrollable_frame,
            text=f"Pontos ganhos: {licao.pontos}",
            font=self.fontes['subtitulo']
        ).pack(pady=10)
        
        ttk.Button(
            self.scrollable_frame,
            text="Voltar ao Menu Principal",
            style="Primario.TButton",
            command=self.mostrar_menu_principal
        ).pack(pady=20)

    def carregar_configuracoes(self):
        """Carrega as configurações do tutorial"""
        # Configurações padrão
        self.config = {
            'tema': 'clam',  # Alterado de 'arc' para 'clam'
            'idioma': 'pt_BR',
            'fonte_tamanho': 12,
            'auto_save': True,
            'mostrar_dicas': True,
            'tempo_maximo_exercicio': 3600,  # 1 hora em segundos
            'pontos_base': 10,
            'nivel_inicial': 1
        }
        
        # Tenta carregar configurações salvas
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
        except Exception as e:
            messagebox.showwarning(
                "Aviso",
                "Não foi possível carregar as configurações. Usando configurações padrão."
            )
        
        # Aplica as configurações
        tema = self.config['tema']
        temas_disponiveis = self.style.theme_names()
        if tema in temas_disponiveis:
            self.style.theme_use(tema)
        else:
            print(f"Tema '{tema}' não encontrado. Temas disponíveis: {temas_disponiveis}")
            self.style.theme_use('clam')  # Alterado de 'arc' para 'clam'

    def criar_interface(self):
        """Cria a interface principal do tutorial"""
        # Setup da janela principal
        self.setup_janela()
        
        # Criar widgets principais
        self.criar_widgets_principais()
        
        # Mostrar tela inicial
        self.criar_tela_inicial()

    def mostrar_ranking(self):
        """Exibe o ranking dos usuários"""
        self.limpar_tela()
        
        # Cabeçalho
        tk.Label(
            self.scrollable_frame,
            text="Ranking de Usuários",
            font=self.fontes['titulo'],
            fg=self.cores['primaria']
        ).pack(pady=20)
        
        # Buscar top 10 usuários do banco de dados
        ranking = self.db.get_ranking(limit=10)
        
        # Frame para a lista de ranking
        ranking_frame = tk.Frame(self.scrollable_frame)
        ranking_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Cabeçalho da tabela
        headers = ["Posição", "Usuário", "Nível", "Pontos", "Exercícios Completos"]
        for col, header in enumerate(headers):
            tk.Label(
                ranking_frame,
                text=header,
                font=self.fontes['subtitulo'],
                fg=self.cores['texto_secundario']
            ).grid(row=0, column=col, padx=10, pady=5)
        
        # Preencher dados do ranking
        for pos, usuario in enumerate(ranking, 1):
            tk.Label(ranking_frame, text=str(pos)).grid(row=pos, column=0, padx=10, pady=5)
            tk.Label(ranking_frame, text=usuario['username']).grid(row=pos, column=1, padx=10, pady=5)
            tk.Label(ranking_frame, text=str(usuario['nivel'])).grid(row=pos, column=2, padx=10, pady=5)
            tk.Label(ranking_frame, text=str(usuario['pontos'])).grid(row=pos, column=3, padx=10, pady=5)
            tk.Label(ranking_frame, text=str(usuario['exercicios_completos'])).grid(row=pos, column=4, padx=10, pady=5)
        
        # Botão para voltar
        ttk.Button(
            self.scrollable_frame,
            text="Voltar ao Menu",
            style="Secundario.TButton",
            command=self.mostrar_menu_principal
        ).pack(pady=20)

    def mostrar_configuracoes(self):
        """Mostra a tela de configurações do tutorial"""
        self.limpar_tela()
        
        # Cabeçalho
        tk.Label(
            self.scrollable_frame,
            text="Configurações",
            font=self.fontes['titulo'],
            fg=self.cores['primaria']
        ).pack(pady=20)
        
        # Frame para as configurações
        config_frame = tk.Frame(self.scrollable_frame)
        config_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=50)
        
        # Tema
        tk.Label(
            config_frame,
            text="Tema:",
            font=self.fontes['subtitulo']
        ).pack(anchor='w', pady=(10,5))
        
        tema_var = tk.StringVar(value=self.config['tema'])
        tema_combo = ttk.Combobox(
            config_frame,
            textvariable=tema_var,
            values=self.style.theme_names(),
            state='readonly'
        )
        tema_combo.pack(fill=tk.X, pady=(0,10))
        
        # Tamanho da fonte
        tk.Label(
            config_frame,
            text="Tamanho da Fonte:",
            font=self.fontes['subtitulo']
        ).pack(anchor='w', pady=(10,5))
        
        fonte_var = tk.IntVar(value=self.config['fonte_tamanho'])
        fonte_scale = ttk.Scale(
            config_frame,
            from_=8,
            to=24,
            variable=fonte_var,
            orient='horizontal'
        )
        fonte_scale.pack(fill=tk.X, pady=(0,10))
        
        # Auto-save
        autosave_var = tk.BooleanVar(value=self.config['auto_save'])
        ttk.Checkbutton(
            config_frame,
            text="Auto-save",
            variable=autosave_var
        ).pack(anchor='w', pady=5)
        
        # Mostrar dicas
        dicas_var = tk.BooleanVar(value=self.config['mostrar_dicas'])
        ttk.Checkbutton(
            config_frame,
            text="Mostrar Dicas",
            variable=dicas_var
        ).pack(anchor='w', pady=5)
        
        # Frame para botões
        botoes_frame = tk.Frame(self.scrollable_frame)
        botoes_frame.pack(fill=tk.X, pady=20)
        
        def salvar_configuracoes():
            """Salva as configurações alteradas"""
            self.config.update({
                'tema': tema_var.get(),
                'fonte_tamanho': fonte_var.get(),
                'auto_save': autosave_var.get(),
                'mostrar_dicas': dicas_var.get()
            })
            
            # Salvar no arquivo
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            
            # Aplicar tema
            self.style.theme_use(self.config['tema'])
            
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
            self.mostrar_menu_principal()
        
        # Botões
        ttk.Button(
            botoes_frame,
            text="Salvar",
            style="Primario.TButton",
            command=salvar_configuracoes
        ).pack(side=tk.RIGHT, padx=20)
        
        ttk.Button(
            botoes_frame,
            text="Cancelar",
            style="Secundario.TButton",
            command=self.mostrar_menu_principal
        ).pack(side=tk.LEFT, padx=20)

    def mostrar_ajuda(self):
        """Mostra a tela de ajuda do tutorial"""
        self.limpar_tela()
        
        # Cabeçalho
        tk.Label(
            self.scrollable_frame,
            text="Ajuda",
            font=self.fontes['titulo'],
            fg=self.cores['primaria']
        ).pack(pady=20)
        
        # Conteúdo da ajuda
        ajuda_frame = tk.Frame(self.scrollable_frame)
        ajuda_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=50)
        
        # Tópicos de ajuda
        topicos = [
            ("Como Usar o Tutorial", """
            1. Escolha uma lição no menu principal
            2. Leia o conteúdo teórico
            3. Complete os exercícios práticos
            4. Ganhe pontos e avance de nível
            """),
            ("Exercícios", """
            - Leia atentamente o enunciado
            - Digite seu código no editor
            - Clique em 'Verificar Resposta'
            - Se necessário, use as dicas disponíveis
            """),
            ("Atalhos do Teclado", """
            Ctrl+S: Salvar código
            Ctrl+Z: Desfazer
            Ctrl+Y: Refazer
            F5: Executar código
            """),
            ("Dúvidas Frequentes", """
            - Como salvar meu progresso?
              O progresso é salvo automaticamente

            - Como recuperar uma lição?
              Use o menu principal para voltar a qualquer lição

            - Como obter ajuda adicional?
              Entre em contato pelo menu Suporte
            """)
        ]
        
        for titulo, conteudo in topicos:
            # Título do tópico
            tk.Label(
                ajuda_frame,
                text=titulo,
                font=self.fontes['subtitulo'],
                fg=self.cores['texto_secundario']
            ).pack(anchor='w', pady=(20,5))
            
            # Conteúdo do tópico
            tk.Label(
                ajuda_frame,
                text=conteudo,
                font=self.fontes['texto'],
                justify=tk.LEFT,
                wraplength=700
            ).pack(anchor='w', padx=20)
        
        # Botão para voltar
        ttk.Button(
            self.scrollable_frame,
            text="Voltar ao Menu",
            style="Secundario.TButton",
            command=self.mostrar_menu_principal
        ).pack(pady=20)

if __name__ == "__main__":
    app = TutorialGUI()
    app.executar()
