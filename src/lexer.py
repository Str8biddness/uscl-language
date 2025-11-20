"""USCL Lexer - Tokenization and lexical analysis for USCL language.

Handles conversion of source code into tokens for parsing.
"""

import re
import logging
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

logger = logging.getLogger(__name__)


class TokenType(Enum):
    """Token types for USCL language."""
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    SYMBOL = auto()
    BOOLEAN = auto()
    
    # Keywords
    DEF = auto()
    LET = auto()
    IF = auto()
    ELSE = auto()
    LAMBDA = auto()
    MATCH = auto()
    QUANTUM = auto()
    ASYNC = auto()
    AWAIT = auto()
    RETURN = auto()
    IMPORT = auto()
    MODULE = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    POW = auto()
    EQ = auto()
    NEQ = auto()
    LT = auto()
    GT = auto()
    LE = auto()
    GE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    ASSIGN = auto()
    ARROW = auto()
    PIPE = auto()
    DOT = auto()
    COLON = auto()
    SEMICOLON = auto()
    COMMA = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()
    
    # Special
    IDENTIFIER = auto()
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()
    EOF = auto()
    WHITESPACE = auto()
    COMMENT = auto()


@dataclass
class Token:
    """Represents a lexical token."""
    type: TokenType
    value: Any
    line: int
    column: int
    
    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"


class Lexer:
    """Lexer for USCL language."""
    
    KEYWORDS = {
        'def': TokenType.DEF,
        'let': TokenType.LET,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'lambda': TokenType.LAMBDA,
        'match': TokenType.MATCH,
        'quantum': TokenType.QUANTUM,
        'async': TokenType.ASYNC,
        'await': TokenType.AWAIT,
        'return': TokenType.RETURN,
        'import': TokenType.IMPORT,
        'module': TokenType.MODULE,
        'true': TokenType.BOOLEAN,
        'false': TokenType.BOOLEAN,
        'and': TokenType.AND,
        'or': TokenType.OR,
        'not': TokenType.NOT,
    }
    
    def __init__(self, source: str) -> None:
        """Initialize lexer with source code."""
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        self.indent_stack = [0]
        
    def tokenize(self) -> List[Token]:
        """Tokenize the entire source code."""
        logger.debug(f"Tokenizing {len(self.source)} characters")
        while self.position < len(self.source):
            self._skip_whitespace_and_comments()
            if self.position >= len(self.source):
                break
            
            char = self.source[self.position]
            
            if char == '\n':
                self.position += 1
                self.line += 1
                self.column = 1
                self.tokens.append(Token(TokenType.NEWLINE, '\n', self.line - 1, self.column))
            elif char.isdigit():
                self._read_number()
            elif char.isalpha() or char == '_':
                self._read_identifier()
            elif char == '"' or char == "'":
                self._read_string(char)
            elif char == ':':
                self._add_token(TokenType.COLON, ':')
                self.position += 1
                self.column += 1
            elif char == ';':
                self._add_token(TokenType.SEMICOLON, ';')
                self.position += 1
                self.column += 1
            elif char == ',':
                self._add_token(TokenType.COMMA, ',')
                self.position += 1
                self.column += 1
            elif char == '.':
                self._add_token(TokenType.DOT, '.')
                self.position += 1
                self.column += 1
            elif char == '(':
                self._add_token(TokenType.LPAREN, '(')
                self.position += 1
                self.column += 1
            elif char == ')':
                self._add_token(TokenType.RPAREN, ')')
                self.position += 1
                self.column += 1
            elif char == '[':
                self._add_token(TokenType.LBRACKET, '[')
                self.position += 1
                self.column += 1
            elif char == ']':
                self._add_token(TokenType.RBRACKET, ']')
                self.position += 1
                self.column += 1
            elif char == '{':
                self._add_token(TokenType.LBRACE, '{')
                self.position += 1
                self.column += 1
            elif char == '}':
                self._add_token(TokenType.RBRACE, '}')
                self.position += 1
                self.column += 1
            else:
                self._read_operator()
        
        self._add_token(TokenType.EOF, None)
        logger.debug(f"Tokenized {len(self.tokens)} tokens")
        return self.tokens
    
    def _skip_whitespace_and_comments(self) -> None:
        """Skip whitespace and comments."""
        while self.position < len(self.source):
            char = self.source[self.position]
            if char in ' \t':
                self.position += 1
                self.column += 1
            elif char == '#':
                while self.position < len(self.source) and self.source[self.position] != '\n':
                    self.position += 1
            else:
                break
    
    def _read_number(self) -> None:
        """Read a numeric literal."""
        start_pos = self.position
        start_col = self.column
        
        while self.position < len(self.source) and self.source[self.position].isdigit():
            self.position += 1
            self.column += 1
        
        if self.position < len(self.source) and self.source[self.position] == '.':
            self.position += 1
            self.column += 1
            while self.position < len(self.source) and self.source[self.position].isdigit():
                self.position += 1
                self.column += 1
            value = float(self.source[start_pos:self.position])
            self._add_token(TokenType.FLOAT, value)
        else:
            value = int(self.source[start_pos:self.position])
            self._add_token(TokenType.INTEGER, value)
    
    def _read_identifier(self) -> None:
        """Read an identifier or keyword."""
        start_pos = self.position
        start_col = self.column
        
        while (self.position < len(self.source) and 
               (self.source[self.position].isalnum() or self.source[self.position] in '_?!')):
            self.position += 1
            self.column += 1
        
        value = self.source[start_pos:self.position]
        token_type = self.KEYWORDS.get(value, TokenType.IDENTIFIER)
        self._add_token(token_type, value)
    
    def _read_string(self, quote: str) -> None:
        """Read a string literal."""
        start_col = self.column
        self.position += 1
        self.column += 1
        start_pos = self.position
        value = ""
        
        while self.position < len(self.source) and self.source[self.position] != quote:
            if self.source[self.position] == '\\':
                self.position += 1
                self.column += 1
                if self.position < len(self.source):
                    escape_char = self.source[self.position]
                    if escape_char == 'n':
                        value += '\n'
                    elif escape_char == 't':
                        value += '\t'
                    elif escape_char == '\\':
                        value += '\\'
                    else:
                        value += escape_char
            else:
                value += self.source[self.position]
            
            self.position += 1
            self.column += 1
        
        if self.position < len(self.source):
            self.position += 1
            self.column += 1
        
        self._add_token(TokenType.STRING, value)
    
    def _read_operator(self) -> None:
        """Read an operator."""
        char = self.source[self.position]
        
        if self.position + 1 < len(self.source):
            two_char = self.source[self.position:self.position+2]
            if two_char == '==':
                self._add_token(TokenType.EQ, '==')
                self.position += 2
                self.column += 2
                return
            elif two_char == '!=':
                self._add_token(TokenType.NEQ, '!=')
                self.position += 2
                self.column += 2
                return
            elif two_char == '<=':
                self._add_token(TokenType.LE, '<=')
                self.position += 2
                self.column += 2
                return
            elif two_char == '>=':
                self._add_token(TokenType.GE, '>=')
                self.position += 2
                self.column += 2
                return
            elif two_char == '->':
                self._add_token(TokenType.ARROW, '->')
                self.position += 2
                self.column += 2
                return
            elif two_char == '**':
                self._add_token(TokenType.POW, '**')
                self.position += 2
                self.column += 2
                return
            elif two_char == '|>':
                self._add_token(TokenType.PIPE, '|>')
                self.position += 2
                self.column += 2
                return
        
        if char == '+':
            self._add_token(TokenType.PLUS, '+')
        elif char == '-':
            self._add_token(TokenType.MINUS, '-')
        elif char == '*':
            self._add_token(TokenType.STAR, '*')
        elif char == '/':
            self._add_token(TokenType.SLASH, '/')
        elif char == '%':
            self._add_token(TokenType.PERCENT, '%')
        elif char == '=':
            self._add_token(TokenType.ASSIGN, '=')
        elif char == '<':
            self._add_token(TokenType.LT, '<')
        elif char == '>':
            self._add_token(TokenType.GT, '>')
        elif char == '|':
            self._add_token(TokenType.PIPE, '|')
        else:
            logger.warning(f"Unknown character: {char} at {self.line}:{self.column}")
        
        self.position += 1
        self.column += 1
    
    def _add_token(self, token_type: TokenType, value: Any) -> None:
        """Add a token to the token list."""
        self.tokens.append(Token(token_type, value, self.line, self.column))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    # Demo code
    source = '''def add(x, y) -> x + y
    let result = add(5, 3)
    quantum entangle(state) { |state> }
    if result > 5 {
        return true
    } else {
        return false
    }
    '''
    
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    for token in tokens:
        print(token)
