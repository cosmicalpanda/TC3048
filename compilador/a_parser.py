'''
lexer.py

tokenizer for the compiler
'''
import ply.yacc as yacc
from lexer import tokens
from vars_table import VarsTable
from semantic_cube import SemanticCube
from func_dir import FuncDir
from quadruples import Quadruples

func_dir = None
semantic_cube = None
quadruples = None

# stack de direcion y tipo [(dir, type)]
operand_stack = None
#
operator_stack = None
#
curr_func = None
curr_var_type = None
curr_var_name = None
curr_func_type = None
curr_param_name = None
curr_param_type = None

'''
main
'''
# programa
def p_programa(p):
    '''
    programa : PROGRAM np_program_start ID np_start_dirfunc ';' var_opcional func_programa_loop main   
    '''

def p_np_program_start(p):
    '''
    np_program_start : epsilon
    '''
    # crear dirFunc
    global func_dir, semantic_cube, quadruples, operand_stack, operator_stack
    func_dir = FuncDir()
    semantic_cube = SemanticCube()
    quadruples = Quadruples()
    operand_stack = []
    operator_stack = []
    
def p_np_start_dirfunc(p):
    '''
    np_start_dirfunc : epsilon
    '''
    # insertar funcion main en dirFunc
    global func_dir, curr_func, curr_func_type
    curr_func = 'global'
    curr_func_type = 'void'
    func_dir.add_func(curr_func, curr_func_type)

# main
# No se puede declarar variables en el main
def p_main(p):
    '''
    main : MAIN '(' ')' '{' loop_estatuto '}' np_fin_total
    '''

def p_np_fin_total(p):
    '''
    np_fin_total : epsilon
    '''
    # borra dirFunc y vartable global

'''
vars
'''

#var_opcional
# puede hacerse la declaracion de variables o no
def p_var_opcional(p):
    '''
    var_opcional : var_declaracion
                 | epsilon
    '''
    pass


# variable
def p_variable(p):
    '''
    variable : ID np_single_var_search
             | ID '[' hyper_exp ']'
    '''


# TODO: array logic, for now only single variables
# Variable declaration
def p_var_declaracion(p):
    '''
    var_declaracion : VARS np_var_prep var_declaracion_mismo_tipo loop_var_declaracion
    '''

# en caso de que curr_func no tenga vartable, crearla
def p_np_var_prep(p):
    '''
    np_var_prep : epsilon
    '''
    # crear vartable
    global func_dir, curr_func
    if not func_dir.has_varstable(curr_func):
        # TODO: agregar opciones de scope
        if curr_func == 'global':
            func_dir.add_varstable(curr_func, 'global')
        else:
            func_dir.add_varstable(curr_func, 'local')


def p_loop_var_declaracion(p):
    '''
    loop_var_declaracion : var_declaracion_mismo_tipo loop_var_declaracion
                         | epsilon
    '''

# declaracion bloque de variables del mismo tipo
def p_var_declaracion_mismo_tipo(p):
    '''
    var_declaracion_mismo_tipo :  tipo np_set_curr_var_type ID np_set_curr_var_name np_add_var_to_varstable loop_var_decl_mismo_tipo ';'
    '''

# TODO: rework for array
# Variable declaration loop
def p_loop_var_decl_mismo_tipo(p):
    '''
    loop_var_decl_mismo_tipo : ',' ID np_set_curr_var_name np_add_var_to_varstable loop_var_decl_mismo_tipo
                  | epsilon
    '''

#
def p_np_set_curr_var_type(p):
    '''
    np_set_curr_var_type : epsilon
    '''
    # set curr_type
    global curr_var_type
    curr_var_type = p[-1]

# 
def p_np_set_curr_var_name(p):
    '''
    np_set_curr_var_name : epsilon
    '''
    # set curr_name
    global curr_var_name
    curr_var_name = p[-1]

def p_np_add_var_to_varstable(p):
    '''
    np_add_var_to_varstable : epsilon
    '''
    # no se tiene que validar, si ya existe se lanza error
    global func_dir, curr_func, curr_var_type, curr_var_name
    # agregar a func_dir y stack de operandos
    print(curr_func, curr_var_type, curr_var_name)
    func_dir.add_var(curr_func, curr_var_type, curr_var_name)
    operand_stack.append((curr_var_name, curr_var_type))

'''
funciones
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
    func_definicion : FUNCTION func_tipo_retorno np_func_tipo_retorno ID np_func_id np_add_to_func_dir '(' np_prep_func_params func_parametro ')' ';' var_opcional '{' loop_estatuto '}' np_kill_func
    '''
    # insert function into function directory
    # func_dir.insert_func(p[3], p[2])

#function return type
def p_func_tipo_retorno(p):
    '''
    func_tipo_retorno : tipo
                      | VOID
    '''
    p[0] = p[1]

def p_np_func_tipo_retorno(p):
    '''
    np_func_tipo_retorno : epsilon
    '''
    # set curr_func_type
    global curr_func_type
    curr_func_type = p[-1]

def p_np_func_id(p):
    '''
    np_func_id : epsilon
    '''
    # set curr_func
    global curr_func
    curr_func = p[-1]

def p_np_add_to_func_dir(p):
    '''
    np_add_to_func_dir : epsilon
    '''
    # agregar a func_dir
    global func_dir, curr_func, curr_func_type
    print(curr_func, curr_func_type)
    func_dir.add_func(curr_func, curr_func_type)
    print("OK")

def p_np_kill_func(p):
    '''
    np_kill_func : epsilon
    '''
    # kill curr_func

def p_np_prep_func_params(p):
    '''
    np_prep_func_params : epsilon
    '''
    # crear vartable
    global func_dir, curr_func
    if not func_dir.has_varstable(curr_func):
        func_dir.add_varstable(curr_func, 'local')

#function parameter
def p_func_parametro(p):
    '''
    func_parametro : parametro
                   | epsilon
    '''
    # logica en caso de no params, quiza agregar params vacio de una vez ?

#TODO: logica para agregar params a func en func_dir
# Parameter
# Solo declara parametros del mismo tipo, para otro tipo se tiene que volver a invocar
def p_parametro(p):
    '''
    parametro : tipo ID loop_parametro
    '''
    # agregar a func_dir 
    # se agrega a stack de operandos? no vdd 
    if len(p) == 2:
        pass
    else:
        for i in p:
            print(i)
        print(curr_func, p[1], p[2])
        func_dir.add_var(curr_func, p[1], p[2])
        # operand_stack.append((p[1], p[2]))


# Parameter loop
# loop parametro es para loopear los parametros del mismo tipo
def p_loop_parametro(p):
    '''
    loop_parametro : ',' tipo ID loop_parametro
                   | epsilon
    '''
    if len(p) == 2:
        pass
    else:
        # agregar a func_dir 
        # se agrega a stack de operandos? no vdd 
        for i in p:
            print(i)
        print(curr_func, p[2], p[3])
        func_dir.add_var(curr_func, p[2], p[3])
        # operand_stack.append((p[1], p[2]))

# Type
def p_tipo(p):
    '''
    tipo : INT
         | FLOAT
         | CHAR
    '''
    p[0] = p[1]

# TODO: logica para arrays
# # List of IDs
# def p_lista_ids(p):
#     '''
#     lista_ids : ID loop_lista_ids
#               | ID '[' INT ']' loop_lista_ids
#     '''

# # loop_lista_ids
# def p_loop_lista_ids(p):
#     '''
#     loop_lista_ids : ',' ID loop_lista_ids
#                    | ',' ID '[' INT ']' loop_lista_ids
#                    | epsilon
#     '''

# # Estatuto
# def p_estatuto(p):
#     '''
#     estatuto : asignacion
#              | func_llamada ';'
#              | read
#              | write
#              | decision
#              | repeticion
#     '''
#     p[0] = p[1]
#     pass

# Estatuto
def p_estatuto(p):
    '''
    estatuto : asignacion
             | func_llamada ';'
             | read
             | write
             | decision
             | repeticion
             | func_return 
    '''
    p[0] = p[1]
    pass

# Asignacion
def p_asignacion(p):
    '''
    asignacion : variable '=' hyper_exp ';'
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
    hyper_exp_loop : hyper_exp hyper_exp_loop_1
    '''

#loop hyper_exp_1
def p_hyper_exp_loop_1(p):
    '''
    hyper_exp_loop_1 : ',' hyper_exp hyper_exp_loop_1
                     | epsilon
    '''

# func return
def p_func_return(p):
    '''
    func_return : RETURN '(' hyper_exp ')' ';'
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


# loop estatuto
# TODO: determinar si es necesario ya que creo que todas las instancias de estatuto son opcionales
# manda un estatuto obligatorio y luego opcionales
def p_loop_estatuto(p):
    '''
    loop_estatuto : estatuto loop_estatuto
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
def p_no_condicional(p):
    '''
    no_condicional : FOR variable '=' hyper_exp TO hyper_exp DO '{' loop_estatuto '}' 
    '''

# Hyper exp
def p_hyper_exp(p):
    '''
    hyper_exp : super_exp hyper_exp_1
    '''
    if operator_stack and (operator_stack[-1] in ['&', '|']):
        # obtener operandos
        op2 = operand_stack.pop()
        op1 = operand_stack.pop()
        # obtener operador
        operator = operator_stack.pop()
        # verificar si se puede hacer la operacion
        result_type = semantic_cube.is_match((op1[1], op2[1], operator))
        # direccion
        result_dir = func_dir.add_var(curr_func, result_type)
        if result_type:
            # agregar cuadruplo
            quadruples.gen_quad(operator, op1, op2,result_dir)
            # agregar resultado a operand stack
            temp = (result_dir, result_type)
            operand_stack.append(temp)
        else:
            raise Exception('Error: tipos incompatibles en operacion')
    


# Hyper exp 1
def p_hyper_exp_1(p):
    '''
    hyper_exp_1 : '&' np_push_operator_stack super_exp
                | '|' np_push_operator_stack super_exp
                | epsilon
    '''

# Super exp
def p_super_exp(p):
    '''
    super_exp : exp super_exp_1
    '''
    if operator_stack and (operator_stack[-1] in ['>', '<', "==", "!="]):
        # obtener operandos
        op2 = operand_stack.pop()
        op1 = operand_stack.pop()
        # obtener operador
        operator = operator_stack.pop()
        # verificar si se puede hacer la operacion
        result_type = semantic_cube.is_match((op1[1], op2[1], operator))
        # direccion
        result_dir = func_dir.add_var(curr_func, result_type)
        if result_type:
            # agregar cuadruplo
            quadruples.gen_quad(operator, op1, op2,result_dir)
            # agregar resultado a operand stack
            temp = (result_dir, result_type)
            operand_stack.append(temp)
        else:
            raise Exception('Error: tipos incompatibles en operacion')
    

# Super exp 1
def p_super_exp_1(p):
    '''
    super_exp_1 : '<' np_push_operator_stack exp
                | '>' np_push_operator_stack exp
                | EQUAL_TO np_push_operator_stack exp
                | NOT_EQUAL_TO np_push_operator_stack exp
                | epsilon
    '''

# Exp
def p_exp(p):
    '''
    exp : term exp_1
    '''
    if operator_stack and (operator_stack[-1] in ['+', '-']):
        # obtener operandos
        op2 = operand_stack.pop()
        op1 = operand_stack.pop()
        # obtener operador
        operator = operator_stack.pop()
        # verificar si se puede hacer la operacion
        result_type = semantic_cube.is_match((op1[1], op2[1], operator))
        # direccion
        result_dir = func_dir.add_var(curr_func, result_type)
        if result_type:
            # agregar cuadruplo
            quadruples.gen_quad(operator, op1, op2,result_dir)
            # agregar resultado a operand stack
            temp = (result_dir, result_type)
            operand_stack.append(temp)
        else:
            raise Exception('Error: tipos incompatibles en operacion')
    

# Exp 1
def p_exp_1(p):
    '''
    exp_1 : '+' np_push_operator_stack term
          | '-' np_push_operator_stack term
          | epsilon
    '''

# Term
def p_term(p):
    '''
    term : factor term_1
    '''
    if operator_stack and (operator_stack[-1] in ['*', '/']):
        # obtener operandos
        op2 = operand_stack.pop()
        op1 = operand_stack.pop()
        # obtener operador
        operator = operator_stack.pop()
        # verificar si se puede hacer la operacion
        result_type = semantic_cube.is_match((op1[1], op2[1], operator))
        # direccion
        result_dir = func_dir.add_var(curr_func, result_type)
        if result_type:
            # agregar cuadruplo
            quadruples.gen_quad(operator, op1, op2,result_dir)
            # agregar resultado a operand stack
            temp = (result_dir, result_type)
            operand_stack.append(temp)
        else:
            raise Exception('Error: tipos incompatibles en operacion')

# Term 1
def p_term_1(p):
    '''
    term_1 : '*' np_push_operator_stack factor 
           | '/' np_push_operator_stack factor
           | epsilon
    '''
def p_np_push_operator_stack(p):
    '''
    np_push_operator_stack : epsilon
    '''
    # push operador a stack
    # global operator_stack
    operator_stack.append(p[-1])
# # Factor
# def p_factor(p):
#     '''
#     factor : func_llamada
#            | VAL_INT
#            | VAL_FLOAT
#            | VAL_STRING
#            | variable
#            | '(' hyper_exp ')'
#     '''

# Factor
# TODO: factor logic
# TODO: define factor values
def p_factor(p):
    '''
    factor : constant
           | variable
           | '(' hyper_exp ')'
    '''
    # # en caso de encontrar una variable, agregar temporalmente solo el nombre al stack
    # if len(p) == 2:
    #     temp_tuple = p[1]
    #     operand_stack.append(temp_tuple)

# Constant
# TODO:  agregar string ?
def p_constant(p):
    '''
    constant : VAL_INT np_push_const_int
             | VAL_FLOAT np_push_const_float
             | VAL_CHAR np_push_const_char
    '''

# TODO: how to do constants 
def p_np_push_const_int(p):
    '''
    np_push_const : epsilon
    '''
    # push constante a operand stack
    dir = func_dir.add_const('int', p[-1])
    operand_stack.append((dir, 'int'))

def p_np_push_const_float(p):
    '''
    np_push_const_float : epsilon
    '''
    # push constante a operand stack
    dir = func_dir.add_const('float', p[-1])
    operand_stack.append((dir, 'float'))

def p_np_push_const_char(p):
    '''
    np_push_const_char : epsilon
    '''
    # push constante a operand stack
    dir = func_dir.add_const('char', p[-1])
    operand_stack.append((dir, 'char'))

def np_single_var_search(p):
    '''
    np_single_var_search : epsilon
    '''
    # buscar variable en dirFunc
    # global func_dir, curr_func
    #
    tipo, dir = func_dir.search_var(curr_func, p[-1])
    operand_stack.append((dir, tipo))

def p_epsilon(p):
    '''epsilon : '''
    p[0] = 'epsilon'


# def p_error(p):
#     if not p:
#         error_msg = "Syntax error"
#     else:
#         error_msg = 'syntax error in line ' + \
#             str(p.lineno) + ' when parsing ' + str(p)
#     raise SyntaxError(error_msg)

'''

TODO: fix bool problem
# '''
# codigo = '''

# program test1 ; 
# vars int  a , b ;  float c, d ;
# function int f1 ( int x, int y ) ; vars int a, b ; { 
#     a = 1 ;
#     b [2] = c [a] ;
#  }
#  main () {
#     x = 1 ;

#     f0();
#     f1 (1);
#     f2 (1, 2);
    
#     read (a, b, c);

#     write (a, b, c);

#     if (a == 1) then {
#         a = 1;
#     } 

#     if (a > 1) then {
#         a = 1;
#     } else {
#         a = 2;
#     }

#     while (a == 1) do {
#         a = 1;
#     }

#     for x = 1 to 10 do {
#         a = 1;
#     }
#  }
# '''
parser = yacc.yacc()
