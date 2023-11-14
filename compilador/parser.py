'''
lexer.py

tokenizer for the compiler
'''
import ply.yacc as yacc
from lexer import tokens
    
# programa
def p_programa(p):
    '''
    programa : PROGRAM ID ';' var_opcional func_programa_loop MAIN '(' ')' '{' loop_estatuto '}' 
    '''

#var_opcional
def p_var_opcional(p):
    '''
    var_opcional : var_declaracion
                 | epsilon
    '''

# Variable declaration
def p_var_declaracion(p):
    '''
    var_declaracion : VARS tipo lista_ids ';' loop_var_decl
    '''

# Variable declaration loop
def p_loop_var_decl(p):
    '''
    loop_var_decl : tipo lista_ids ';' loop_var_decl
                  | epsilon
    '''

#func_programa_loop
def p_func_programa_loop(p):
    '''
    func_programa_loop : func_definicion func_programa_loop
                       | epsilon
    '''

# function definition
def p_func_definicion(p):
    '''
    func_definicion : FUNCTION func_tipo_retorno ID '(' func_parametro ')' ';' var_opcional '{' loop_estatuto '}' 
    '''

#function return type
def p_func_tipo_retorno(p):
    '''
    func_tipo_retorno : tipo
                      | VOID
    '''

#function parameter
def p_func_parametro(p):
    '''
    func_parametro : parametro func_parametro
                   | epsilon
    '''

# Parameter
# Solo declara parametros del mismo tipo, para otro tipo se tiene que volver a invocar
def p_parametro(p):
    '''
    parametro : tipo ID loop_parametro
    '''

# Parameter loop
# loop parametro es para loopear los parametros del mismo tipo
def p_loop_parametro(p):
    '''
    loop_parametro : ',' tipo ID loop_parametro
                   | epsilon
    '''

# loop parametro
def p_loop_parametro(p):
    '''
    loop_parametro : ',' ID loop_parametro
                   | epsilon
    '''

# Type
def p_tipo(p):
    '''
    tipo : INT
         | FLOAT
         | CHAR
         | STRING
    '''

# List of IDs
def p_lista_ids(p):
    '''
    lista_ids : ID loop_lista_ids
              | ID '[' INT ']' loop_lista_ids
    '''

# loop_lista_ids
def p_loop_lista_ids(p):
    '''
    loop_lista_ids : ',' ID loop_lista_ids
                   | ',' ID '[' INT ']' loop_lista_ids
                   | epsilon
    '''

# Estatuto
def p_estatuto(p):
    '''
    estatuto : asignacion
             | func_llamada
             | io
             | decision
             | repeticion
    '''

# Asignacion
def p_asignacion(p):
    '''
    asignacion : variable '=' hyper_exp
    '''

# Funcion llamada
def p_func_llamada(p):
    '''
    func_llamada : ID '(' ')' 
                 | ID '(' hyper_exp_loop ')' 
    '''

#loop hyper_exp
def p_hyper_exp_loop(p):
    '''
    hyper_exp_loop : hyper_exp ',' hyper_exp_loop_1
    '''

#loop hyper_exp_1
def p_hyper_exp_loop_1(p):
    '''
    hyper_exp_loop_1 : ',' hyper_exp_loop_1
                     | epsilon
    '''

# func return
def p_func_return(p):
    '''
    func_return : RETURN '(' hyper_exp ')' ';'
    '''


# IO
def p_io(p):
    '''
    io : read
        | write
    '''

# Read
def p_read(p):
    '''
    read : READ '(' variable_loop ')' ';'
    '''

# Variable loop
def p_variable_loop(p):
    '''
    variable_loop : variable variable_loop_1
    '''

# Variable loop 1
def p_variable_loop_1(p):
    '''
    variable_loop_1 : ',' variable variable_loop_1
                    | epsilon
    '''

# Write
def p_write(p):
    '''
    write : WRITE '(' hyper_exp_loop ')' ';'
    '''

# Decision
def p_decision(p):
    '''
    decision : IF '(' hyper_exp ')' THEN '{' loop_estatuto '}'  decision_1
    '''

# Decision 1
def p_decision_1(p):
    '''
    decision_1 : ELSE '{' loop_estatuto '}' 
               | epsilon
    '''

# variable
def p_variable(p):
    '''
    variable : ID
             | ID '[' hyper_exp ']'
    '''

# loop estatuto
# TODO: determinar si es necesario ya que creo que todas las instancias de estatuto son opcionales
# manda un estatuto obligatorio y luego opcionales
def p_loop_estatuto(p):
    '''
    loop_estatuto : estatuto loop_estatuto_1
    '''

# loop estatuto 1  
def p_loop_estatuto_1(p):
    '''
    loop_estatuto_1 : estatuto loop_estatuto_1
                    | epsilon
    '''

# Repeticion
def p_repeticion(p):
    '''
    repeticion : condicional
               | no_condicional
    '''

# Condicional
def p_condicional(p):
    '''
    condicional : WHILE '(' hyper_exp ')' DO '{' loop_estatuto '}' 
    '''

# No condicional
# usar id en lugar de variable, por que usaria una casilla de algun array en un for ?
# llamo loop_estatuto_1 para que sea opcional
def p_no_condicional(p):
    '''
    no_condicional : FOR variable '=' hyper_exp TO hyper_exp DO '{' loop_estatuto_1 '}' 
    '''

# Hyper exp
def p_hyper_exp(p):
    '''
    hyper_exp : super_exp hyper_exp_1
    '''

# Hyper exp 1
def p_hyper_exp_1(p):
    '''
    hyper_exp_1 : '&' super_exp
                | '|' super_exp
                | epsilon
    '''

# Super exp
def p_super_exp(p):
    '''
    super_exp : exp super_exp_1
    '''

# Super exp 1
def p_super_exp_1(p):
    '''
    super_exp_1 : '<' exp
                | '>' exp
                | EQUAL_TO exp
                | NOT_EQUAL_TO exp
                | epsilon
    '''

# Exp
def p_exp(p):
    '''
    exp : termino exp_1
    '''

# Exp 1
def p_exp_1(p):
    '''
    exp_1 : '+' term
          | '-' term
          | epsilon
    '''

# Term
def p_term(p):
    '''
    term : factor term_1
    '''

# Term 1
def p_term_1(p):
    '''
    term_1 : '*' factor term_1
           | '/' factor term_1
           | epsilon
    '''

# Factor
def p_factor(p):
    '''
    factor : func_llamada
           | VAL_INT
           | VAL_FLOAT
           | VAL_STRING
           | VAL_BOOL
           | variable
           | '(' hyper_exp ')'
    '''

def p_epsilon(p):
    '''epsilon : '''
    p[0] = 'epsilon'
