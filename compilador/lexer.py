import ply.lex as lex
'''
lexer.py

tokenizer for the compiler
'''


# Reserved
reserved = {
    'program' : 'PROGRAM',
    'main' : 'MAIN',
    'vars' : 'VARS',
    'int' : 'INT',
    'float' : 'FLOAT',
    'string' : 'STRING',
    'char' : 'CHAR',
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


# Add reserverd list
tokens = tokens + list(reserved.values())

# ID
def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')     # Check for reserved words
    return t

# VAL_INT
def t_VAL_INT(t):
    r'\d+'
    t.type = reserved.get(t.value,'VAL_INT')
    t.value = (t.value,'int')
    return t

# VAL_FLOAT
def t_VAL_FLOAT(t):
    r'\d+\.\d+'
    t.type = reserved.get(t.value,'VAL_FLOAT')
    t.value = (t.value,'float')
    return t

# VAL_STRING
def t_VAL_STRING(t):
    r'"[^"]*"'
    t.type = reserved.get(t.value, 'VAL_STRING')
    t.value = t.value[1:len(t.value)-1]  # Remove quotes
    t.value = (t.value, 'string')
    return t

# VAL_BOOL
def t_VAL_BOOL(t):
    r'true|false'
    t.type = reserved.get(t.value,'VAL_BOOL') 
    t.value = (t.value, 'bool')
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

def t_print(t):
    r'print'
    t.type = reserved.get(t.value,'PRINT')     # Check for reserved words
    return t

# Lexer build
lexer = lex.lex()
