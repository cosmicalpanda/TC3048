'''
lexer.py

tokeniza el codigo fuente
'''
import ply.lex as lex

# Reserved
reserved = {
    'program' : 'PROGRAM',
    'main' : 'MAIN',
    'vars' : 'VARS',
    'int' : 'INT',
    'float' : 'FLOAT',
    'string' : 'STRING',
    'char' : 'CHAR',
    'bool' : 'BOOL',
    'function' : 'FUNCTION',
    'return' : 'RETURN',
    'void' : 'VOID',
    'read' : 'READ',
    'write' : 'WRITE',
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'for' : 'FOR',
    'to' : 'TO',
    'do' : 'DO',
    'mediana' : 'MEDIANA',
    'media' : 'MEDIA',
    'moda' : 'MODA',
    'varianza' : 'VARIANZA',
    'len' : 'LEN',
    'sen' : 'SEN',
    'cos' : 'COS',
    'tan' : 'TAN',
    'senh' : 'SENH',
    'cosh' : 'COSH',
    'tanh' : 'TANH',
    'log' : 'LOG',
    'abs' : 'ABS',
    'floor' : 'FLOOR',
    'ceil' : 'CEIL',
    'rand' : 'RAND',
    'pow' : 'POW',
    'min' : 'MIN',
    'max' : 'MAX',
}

# Token list
tokens = [
    'ID',
    'VAL_INT',
    'VAL_FLOAT',
    'VAL_STRING',
    'VAL_CHAR',
    'EQUAL_TO',
    'NOT_EQUAL_TO'
]

# Literals
literals = ".,;:]}){([=+-*/><|%&"

# Simple tokens regex
t_EQUAL_TO = r'=='
t_NOT_EQUAL_TO = r'!='

t_VAL_INT = r'-?[0-9]+'
t_VAL_FLOAT = r'-?[0-9]+\.[0-9]+'


# Add reserverd list
tokens = tokens + list(reserved.values())

# ID
def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')     # Check for reserved words
    return t

# VAL_CHAR
def t_VAL_CHAR(t):
    r'\'[^\']\''
    t.type = reserved.get(t.value, 'VAL_CHAR')
    t.value = t.value[1:-1]  # Remove quotes
    # t.value = (t.value, 'char')
    return t
    
# Ignored chars, newline & errors
t_ignore = " \t"

# Ignore comments
t_ignore_COMMENT = r'%.*'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Lexer build
lexer = lex.lex()
