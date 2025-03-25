from urllib.request import urlopen
from urllib.parse import urlparse
from html.parser import HTMLParser
from pip._vendor.rich.console import Console
from pip._vendor.rich.text import Text
from pip._vendor.rich.panel import Panel
import sys
import chardet

class TextBrowserParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.in_title = False
        self.title = ""
        
    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.in_title = True
        elif tag == 'br':
            self.text.append('\n')
        elif tag == 'p':
            self.text.append('\n\n')
            
    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
            
    def handle_data(self, data):
        if self.in_title:
            self.title += data
        else:
            self.text.append(data.strip())

class TextBrowser:
    def __init__(self):
        self.console = Console()
        self.history = []
        
    def detect_encoding(self, content):
        # Detecta a codificação do conteúdo
        result = chardet.detect(content)
        return result['encoding'] or 'utf-8'
        
    def fetch_page(self, url):
        try:
            # Adiciona http:// se não existir
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
                
            response = urlopen(url)
            content = response.read()
            
            # Detecta e usa a codificação correta
            encoding = self.detect_encoding(content)
            html = content.decode(encoding, errors='replace')
            
            parser = TextBrowserParser()
            parser.feed(html)
            
            # Limpa a tela
            self.console.clear()
            
            # Mostra o título
            title = Text(parser.title, style="bold blue")
            self.console.print(Panel(title))
            
            # Mostra o conteúdo
            content = ' '.join(parser.text)
            self.console.print(content)
            
            # Adiciona à história
            self.history.append(url)
            
        except Exception as e:
            self.console.print(f"Erro ao carregar a página: {str(e)}", style="bold red")
            
    def run(self):
        while True:
            self.console.print("\nComandos:", style="bold green")
            self.console.print("- Digite uma URL para navegar")
            self.console.print("- 'voltar' para página anterior")
            self.console.print("- 'sair' para encerrar")
            
            command = input("\n> ").strip().lower()
            
            if command == 'sair':
                break
            elif command == 'voltar':
                if len(self.history) > 1:
                    self.history.pop()  # Remove atual
                    last_url = self.history.pop()  # Pega anterior
                    self.fetch_page(last_url)
                else:
                    self.console.print("Não há páginas anteriores!", style="yellow")
            else:
                self.fetch_page(command)

if __name__ == "__main__":
    browser = TextBrowser()
    browser.run()
