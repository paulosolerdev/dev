import tkinter as tk
import re
from typing import Dict

class PythonHighlighter:
    def __init__(self, text_widget: tk.Text):
        self.text_widget = text_widget
        
        # Configure tags for different syntax elements
        self.text_widget.tag_configure("keyword", foreground="#FF7043")  # Orange for keywords
        self.text_widget.tag_configure("string", foreground="#66BB6A")   # Green for strings
        self.text_widget.tag_configure("comment", foreground="#90A4AE")  # Gray for comments
        self.text_widget.tag_configure("function", foreground="#42A5F5") # Blue for functions
        self.text_widget.tag_configure("number", foreground="#AB47BC")   # Purple for numbers
        
        # Python keywords
        self.keywords = {
            "False", "None", "True", "and", "as", "assert", "async", "await",
            "break", "class", "continue", "def", "del", "elif", "else", "except",
            "finally", "for", "from", "global", "if", "import", "in", "is",
            "lambda", "nonlocal", "not", "or", "pass", "raise", "return",
            "try", "while", "with", "yield"
        }
        
        # Bind events for real-time highlighting
        self.text_widget.bind("<KeyRelease>", self.highlight_syntax)
        self.text_widget.bind("<<Paste>>", self.highlight_syntax)
        
    def clear_tags(self):
        """Remove all syntax highlighting tags"""
        for tag in ["keyword", "string", "comment", "function", "number"]:
            self.text_widget.tag_remove(tag, "1.0", "end")
    
    def highlight_syntax(self, event=None):
        """Apply syntax highlighting to the entire text"""
        # Remove existing tags
        self.clear_tags()
        
        # Get the text content
        content = self.text_widget.get("1.0", "end-1c")
        
        # Highlight strings (both single and double quotes)
        for match in re.finditer(r'([\'"])(.*?)\1', content):
            start = self.get_text_position(content, match.start())
            end = self.get_text_position(content, match.end())
            self.text_widget.tag_add("string", start, end)
        
        # Highlight comments
        for match in re.finditer(r'#.*$', content, re.MULTILINE):
            start = self.get_text_position(content, match.start())
            end = self.get_text_position(content, match.end())
            self.text_widget.tag_add("comment", start, end)
        
        # Highlight keywords
        for keyword in self.keywords:
            start_index = "1.0"
            while True:
                start_index = self.text_widget.search(
                    r'\m{}\M'.format(keyword),
                    start_index,
                    "end",
                    regexp=True
                )
                if not start_index:
                    break
                end_index = f"{start_index}+{len(keyword)}c"
                self.text_widget.tag_add("keyword", start_index, end_index)
                start_index = end_index
        
        # Highlight function definitions
        for match in re.finditer(r'def\s+(\w+)\s*\(', content):
            func_name = match.group(1)
            start = self.get_text_position(content, match.start(1))
            end = self.get_text_position(content, match.end(1))
            self.text_widget.tag_add("function", start, end)
        
        # Highlight numbers
        for match in re.finditer(r'\b\d+\.?\d*\b', content):
            start = self.get_text_position(content, match.start())
            end = self.get_text_position(content, match.end())
            self.text_widget.tag_add("number", start, end)
    
    def get_text_position(self, text: str, index: int) -> str:
        """Convert a string index to a tkinter text position (line.char)"""
        line_start = text.rfind('\n', 0, index) + 1
        if line_start == 0:
            line = 1
            col = index
        else:
            line = text.count('\n', 0, index) + 1
            col = index - line_start
        return f"{line}.{col}"
