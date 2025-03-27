import tkinter as tk
from tkinter import ttk, messagebox
import json
import sqlite3
from datetime import datetime
import hashlib
from typing import Dict, List, Optional
from dataclasses import dataclass
import syntax_highlighter
import markdown2
from ttkthemes import ThemedStyle

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
        self.setup_estilos()
        self.setup_janela()
        self.carregar_configuracoes()
        self.db = BancoDados()
        self.setup_variaveis()
        self.criar_widgets_principais()
        self.carregar_licoes()
        
    def setup_estilos(self):
        """Configura os estilos e temas da interface"""
        self.style = ThemedStyle()
        self.style.set_theme("arc")  # Tema moderno
        
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
        
        for teste in exercicio.testes:
            try:
                # Preparar ambiente de teste
                namespace = {}
                exec(codigo, namespace)
                
                # Executar teste
                resultado = eval(teste['teste'], namespace)
                
                if resultado != eval(teste['esperado']):
                    messagebox.showerror(
                        "Teste Falhou",
                        f"Teste: {teste['descricao']}\n"
                        f"Esperado: {teste['esperado']}\n"
                        f"Obtido: {resultado}"
                    )
                    return False
                    
            except Exception as e:
                messagebox.showerror(
                    "Erro na Execução",
                    f"Erro ao executar teste: {teste['descricao']}\n{str(e)}"
                )
                return False
        
        # Todos os testes passaram
        self.exercicio_completo(exercicio)
        return True

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

        # Criar janela no canvas que conterá o frame
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

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
        self.licoes: Dict[int, Licao] = {
            1: Licao(
                titulo="Fundamentos de Python",
                descricao="Conceitos básicos da linguagem Python",
                conteudo="""
                Python é uma linguagem de programação de alto nível, interpretada e de propósito geral.
                Suas principais características são:
                
                • Sintaxe clara e legível
                • Tipagem dinâmica
                • Gerenciamento automático de memória
                • Rica biblioteca padrão
                • Grande comunidade e ecossistema
                """,
                exemplos=[
                    "# Variáveis e tipos básicos\nx = 10\nnome = 'Python'\nativa = True",
                    "# Estruturas de controle\nif x > 0:\n    print('Positivo')\nelse:\n    print('Negativo')",
                    "# Loops\nfor i in range(5):\n    print(i)"
                ],
                exercicios=[
                    Exercicio(
                        titulo="Calculadora Simples",
                        descricao="Crie uma função que recebe dois números e retorna a soma",
                        codigo_inicial="def soma(a, b):\n    # Seu código aqui\n    pass",
                        codigo_resposta="def soma(a, b):\n    return a + b",
                        dicas=["Utilize o operador +", "Não esqueça do return"],
                        pontos=10
                    )
                ],
                nivel_requerido=1,
                pontos=100
            ),
            2: Licao(
                titulo="Estruturas de Dados",
                descricao="Listas, tuplas, dicionários e conjuntos",
                conteudo="""
                Python oferece várias estruturas de dados built-in:
                
                • Listas: Sequências mutáveis [1, 2, 3]
                • Tuplas: Sequências imutáveis (1, 2, 3)
                • Dicionários: Mapeamentos chave-valor {'a': 1, 'b': 2}
                • Conjuntos: Coleções não ordenadas de elementos únicos {1, 2, 3}
                """,
                exemplos=[
                    "# Listas\nlista = [1, 2, 3]\nlista.append(4)",
                    "# Dicionários\ndict = {'nome': 'Python'}\ndict['versao'] = '3.9'",
                    "# Conjuntos\nconjunto = {1, 2, 3}\nconjunto.add(4)"
                ],
                exercicios=[
                    Exercicio(
                        titulo="Manipulação de Listas",
                        descricao="Crie uma função que remove duplicatas de uma lista",
                        codigo_inicial="def remove_duplicatas(lista):\n    # Seu código aqui\n    pass",
                        codigo_resposta="def remove_duplicatas(lista):\n    return list(set(lista))",
                        dicas=["Use set() para remover duplicatas", "Converta de volta para lista"],
                        pontos=15
                    )
                ],
                nivel_requerido=1,
                pontos=150
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
        self.salvar_progresso()
        self.mostrar_menu_principal()

    def salvar_progresso(self):
        """Salva o progresso do usuário no banco de dados"""
        self.cursor.execute('''
            INSERT OR REPLACE INTO usuarios (nome, nivel, pontos, ultima_sessao)
            VALUES (?, ?, ?, ?)
        ''', (
            self.usuario["nome"],
            self.usuario["nivel"],
            self.usuario["pontos"],
            self.usuario["ultima_sessao"]
        ))
        self.conn.commit()

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

    def executar(self):
        """Inicia a execução do programa"""
        self.root.mainloop()

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

if __name__ == "__main__":
    app = TutorialGUI()
    app.executar()
