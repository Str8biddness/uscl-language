"""USCL - Universal Symbolic Communication Language

A production-ready symbolic AI language for human-AI communication with quantum integration.

Modules:
    - lexer: Tokenization and lexical analysis
    - parser: Syntax parsing and AST generation
    - semantic: Semantic analysis and type checking
    - interpreter: Runtime execution engine
    - types: Type system and definitions
    - symbols: Symbol table and scope management
    - stdlib: Standard library functions
    - quantum: Quantum integration layer
    - aios_bridge: Integration with AIOS-Brain
"""

__version__ = '1.0.0'
__author__ = 'AIOS Development Team'
__license__ = 'MIT'

from .lexer import Lexer, Token, TokenType
from .parser import Parser, ASTNode
from .semantic import SemanticAnalyzer
from .interpreter import Interpreter
from .types import Type, TypeChecker
from .symbols import SymbolTable, Symbol

__all__ = [
    'Lexer',
    'Token',
    'TokenType',
    'Parser',
    'ASTNode',
    'SemanticAnalyzer',
    'Interpreter',
    'Type',
    'TypeChecker',
    'SymbolTable',
    'Symbol',
]
