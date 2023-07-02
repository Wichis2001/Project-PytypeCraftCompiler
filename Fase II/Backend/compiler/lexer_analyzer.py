"""
Analizador Lexico

Utiliza Ply para la construccion de regex que cumplan con los tokens de TypeScript

Fecha: 05/06/2023
"""
from compiler.ply import lex
#import ply.lex as lex

errores = []

reserved = { ## Reserved Words
    'true': 'TRUE',
    'interface': 'INTERFACE',
    'null': 'NULL_TYPE',
    'number': 'NUMBER_TYPE',
    'string': 'STRING_TYPE',
    'boolean': 'BOOLEAN_TYPE',
    'any': 'ANY_TYPE',
    'false': 'FALSE',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'of': 'OF',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'function': 'FUNCTION',
    'let': 'LET',
    'concat' : 'CONCAT',
    'String':   'FUNC_STRING',
    'console': 'CONSOLE',
    'log': 'LOG',
    'void': 'VOID',
    'push': 'PUSH',
    'pop':  'POP'
}

tokens = [ ## Tokens Definition
    'COMMENT_LINE', ## Comments
    'COMMENT_MULT',
    'DOT', ## Punctuation Marks
    'COMMA',
    'SEMICOLON',
    'COLON',
    'L_PAREN', ## Delimiters
    'R_PAREN',
    'L_BRACKET',
    'R_BRACKET',
    'L_BRACE',
    'R_BRACE',
    'GREATHER_THAN_OR_EQUAL', ## Comparison Operators
    'LESS_THAN_OR_EQUAL',
    'GREATHER_THAN',
    'LESS_THAN',
    'EQUAL',
    'UNEQUAL',
    'AND', ## Logical Operators
    'OR',
    'NOT',
    'PLUS', ## Mathematical Operators
    'MINUS',
    'MULT',
    'DIV',
    'POW',
    'MOD',
    'INCREMENT',
    'DECREMENT',
    'ASSIGN', ## Assignment Operators
    'ID', ## Other Tokens
    'NUMBER',
    'STRING'
] + list(reserved.values())

states = (
    ('string', 'exclusive'),
)

## Regex Definitions
t_DOT       = r'\.' ## Punctuation Marks
t_COMMA     = r','
t_SEMICOLON = r';'
t_COLON     = r':'

t_L_PAREN   = r'\(' ## Deliminters
t_R_PAREN   = r'\)'
t_L_BRACKET = r'\['
t_R_BRACKET = r'\]'
t_L_BRACE   = r'\{'
t_R_BRACE   = r'\}'

t_GREATHER_THAN_OR_EQUAL = r'>=' ## Comparison Operators
t_LESS_THAN_OR_EQUAL    = r'<='
t_GREATHER_THAN          = r'>'
t_LESS_THAN             = r'<'
t_EQUAL                 = r'==='
t_UNEQUAL               = r'!=='

t_AND   = r'&&' ## Logical Operators
t_OR    = r'\|\|'
t_NOT   = r'!'

t_INCREMENT         = r'\+\+' ## Arithmetic Operators
t_DECREMENT         = r'--'
t_PLUS              = r'\+'
t_MINUS             = r'-'
t_MULT              = r'\*'
t_DIV               = r'/'
t_POW               = r'\^'
t_MOD               = r'%'

t_ASSIGN        = r'=' ## Assignment Operators

t_ignore = ' \t'

## Regex for other tokens
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

def t_string(t):
    r'(\"|\'|`)'
    t.lexer.begin('string')
    t.lexer.string_start = t.lexer.lexpos
    t.lexer.string_char_open = t.value
    
def t_string_end(t):
    r'(\"|\'|`)'
    if t.lexer.string_char_open == t.value:
        t.lexer.begin('INITIAL')
        t.value = t.lexer.lexdata[t.lexer.string_start:t.lexer.lexpos - 1]
        t.value = t.value.replace('\\t', '\t')
        t.value = t.value.replace('\\n', '\n')
        t.value = t.value.replace('\\"', '\"')
        t.value = t.value.replace("\\'", "\'")
        t.value = t.value.replace('\\\\', '\\')
        t.type = 'STRING'
        return t

t_string_ignore = r'.'
    
def t_string_error(t):
    t.lexer.skip(1)

def t_COMMENT_LINE(t):
    r'//.*\n'
    t.lexer.lineno += 1

def t_COMMENT_MULT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    t.lexer.skip(1)
    
def find_column(inp, tk):
    line_start = inp.rfind('\n', 0, tk.lexpos) + 1
    return (tk.lexpos - line_start) + 1

lexer = lex.lex()