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

import json

func_dir = FuncDir()
semantic_cube = None
quadruples = Quadruples()

cuad = []
fd = []
counters = {}
constants = {}

# stack de direcion y tipo [(dir, type)]
operand_stack = None
operator_stack = None
jump_stack = None
curr_func = None
curr_var_type = None
curr_var_name = None
curr_func_type = None
curr_param_name = None
curr_param_type = None
# multiple input counter
input_counter = None
dir_uno = None
dir_menos_uno = None
curr_dir_for = None
curr_type_for = None
call_stack = None
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
    global  semantic_cube, quadruples, operand_stack, operator_stack
    global input_counter, jump_stack, dir_uno, call_stack, dir_menos_uno
    # func_dir = FuncDir()
    semantic_cube = SemanticCube()
    quadruples = Quadruples()
    operand_stack = []
    operator_stack = []
    jump_stack = []
    input_counter = 0
    call_stack = []

    # Agregar constante 1 para funcionalidad for
    dir_uno = func_dir.add_const('int', '1')
    # agregar k para arrays
    dir_menos_uno = func_dir.add_const('int', '-1')


def p_np_start_dirfunc(p):
    '''
    np_start_dirfunc : epsilon
    '''
    # insertar funcion global en dirFunc, guarda la function actual en curr_func
    global func_dir, curr_func, curr_func_type
    curr_func = 'global'
    curr_func_type = 'void'
    # print(curr_func, curr_func_type)
    func_dir.add_func(curr_func, curr_func_type)
    # GOTO, cuadruplo inicial de todo el programa
    quadruples.gen_quad('GOTO', -1, -1, None)

# main
# No se puede declarar variables en el main
def p_main(p):
    '''
    main : MAIN np_prep_main '(' ')' '{' loop_estatuto '}' np_fin_total
    '''
def p_np_prep_main(p):
    '''
    np_prep_main : epsilon
    '''
    # crear vartable
    global func_dir, curr_func, curr_func_type, quadruples
    # rellena GOTO main con el primer cuadruplo del main
    quadruples.fill_quad(0, 3, quadruples.counter)
    curr_func = 'main'
    curr_func_type = 'void'
    # no agregamos main a func_dir ya que fue instanciado en la clase
    # agregamos cuadruplo de inicio de main
    func_dir.dir[curr_func][3] = quadruples.counter
    quadruples.gen_quad('INIT', -1, -1, -1)

def p_np_fin_total(p):
    '''
    np_fin_total : epsilon
    '''
    # cuadruplo final del programa
    quadruples.gen_quad('ENDPROG', -1, -1, -1)
    # for q in quadruples.list:
    #     print(q)
    
    cont_q = 0
    for i in func_dir.dir:
        fd.append( (i, func_dir.dir[i][0], func_dir.dir[i][1].table , func_dir.dir[i][2],func_dir.dir[i][3],func_dir.dir[i][4] ))
    # fd = func_dir.dir['global'][1].table
    obj = {"function_directory": fd,
           "quads":  quadruples.list}
    with open('obj.json', "w") as output_file:
        json.dump(obj, output_file, indent=4)
    # borra dirFunc y vartable global
    for q in quadruples.list:
        cuad.append(q)
    # print(fd)

    for func in func_dir.dir.keys():
        counters[func] = func_dir.get_counter(func)
    # print(counters)
    cdict = func_dir.get_const_table().copy()
    for c in cdict:
        constants[c] = (cdict[c][0], cdict[c][1])
    print("CONST", constants)
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

# TODO: add array logic
#             | ID '[' hyper_exp ']'
# variable
def p_variable(p):
    '''
    variable : ID np_single_var_process
             | ID '[' np_push_operator_stack hyper_exp ']' np_pop_operator_stack np_array_var_process

    '''
    # if len(p) == 2:
    #     p[0] = p[1]

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
    var_declaracion_mismo_tipo :  tipo np_set_curr_var_type ID np_set_curr_var_name array_opcional np_add_var_to_varstable loop_var_decl_mismo_tipo ';'
    '''

def p_array_opcional(p):
    '''
    array_opcional : '[' VAL_INT np_push_const_int ']'
                   | epsilon
    '''
    # print(len(p))
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = p[2]


# Variable declaration loop
def p_loop_var_decl_mismo_tipo(p):
    '''
    loop_var_decl_mismo_tipo : ',' ID np_set_curr_var_name array_opcional np_add_var_to_varstable loop_var_decl_mismo_tipo
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
    # print(curr_func, curr_var_type, curr_var_name, p[-1])
    func_dir.add_var(curr_func, curr_var_type, curr_var_name, p[-1])
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
    func_definicion : FUNCTION func_tipo_retorno np_func_tipo_retorno ID np_func_id np_add_to_func_dir '(' np_prep_func_params func_parametro ')' ';' var_opcional np_save_curr_func_quad '{' loop_estatuto '}' np_kill_func
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
    # print(curr_func, curr_func_type)
    func_dir.add_func(curr_func, curr_func_type)
    # si la funcion tiene valor de retorno crear el valor global para almacenarlo
    if curr_func_type != 'void':
        # si no se creo una tabla de valores globales crearla
        if not func_dir.has_varstable('global'):
            func_dir.add_varstable('global', 'global')
        # agregar variable global para almacenar el valor de retorno
        dirRet = func_dir.add_var('global', curr_func_type, '_' + curr_func)
        func_dir.add_return(curr_func, dirRet)
        # func_dir.add_var(curr_func, curr_func_type, 'return')
    # print("OK")

def p_np_save_curr_func_quad(p):
    '''
    np_save_curr_func_quad : epsilon
    '''
    global func_dir, curr_func
    # guarda el cuadruplo de inicio de la funcion
    func_dir.dir[curr_func][3] = quadruples.counter

def p_np_kill_func(p):
    '''
    np_kill_func : epsilon
    '''
    # kill curr_func
    quadruples.gen_quad('ENDFUNC', -1, -1, -1)

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
    parametro : tipo ID np_add_param loop_parametro
    '''

# Parameter loop
# loop parametro es para loopear los parametros del mismo tipo
def p_loop_parametro(p):
    '''
    loop_parametro : ',' tipo ID np_add_param loop_parametro
                   | epsilon
    '''

def p_np_add_param(p):
    '''
    np_add_param : epsilon
    '''
    # agregar a func_dir
    global func_dir, curr_func, curr_param_type, curr_param_name
    func_dir.add_param(curr_func, p[-2], p[-1])

# Type
def p_tipo(p):
    '''
    tipo : INT
         | FLOAT
         | CHAR
         | BOOL
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
    # obtener datos de operandos
    op2 = operand_stack.pop()
    op1 = operand_stack.pop()
    # tipos iguales
    if op1[1] != op2[1]:
        raise Exception('Error: tipos incompatibles en asignacion. {} = {}'.format(op1[1], op2[1]))
    # agregar cuadruplo
    quadruples.gen_quad('=', op2[0], -1, op1[0])
    
# Funcion llamada
def p_func_llamada(p):
    '''
    func_llamada : ID np_fc_1 '(' np_push_operator_stack argumento_loop ')' np_pop_operator_stack
    '''
    # verifica que los argumentos sean exactos
    if call_stack[-1][1][0] < call_stack[-1][1][1]:
        raise Exception('Error: llamada a funcion con parametros faltantes')
    # agregar cuadruplo
    quadruples.gen_quad('GOSUB', -1, -1, func_dir.get_quad(p[1]))
    # obtener tipo esperado de llamada
    ret_tipo = func_dir.get_func_type(call_stack[-1][0])
    # en caso de tener retorno:
    if ret_tipo != 'void':
        # TODO: usar global en vez de call stack 
        # primero busca en funcion, luego en global
        _, ret_dir = func_dir.search_var(call_stack[-1][0], '_' + call_stack[-1][0])
        call_stack.pop()
        # guarda en temporal el valor de retorno en caso de multiples llamadas
        ret_temp = func_dir.add_var(call_stack[-1][0], ret_tipo)
        # agregar cuadruplo para guardar retorno temporal a global
        quadruples.gen_quad('=', ret_dir, -1, ret_temp)
        operand_stack.append((ret_temp, ret_tipo)) # agregar a operand stack
       
    # fin llamada actual
    call_stack.pop()


def p_np_fc_1(p):
    '''
    np_fc_1 : epsilon
    '''
    func = func_dir.dir.get(p[-1])
    # call stack tendra el orden de llamadas realizadas
    call_stack.append((curr_func, []))
    if func:
        call_stack.append((p[-1], []))
        # agregar cuadruplo
        quadruples.gen_quad('ERA', -1, -1, p[-1])
        # [contador de argumentos, contador de parametros esperados] 
        call_stack[-1][1].append(0)
        call_stack[-1][1].append(len(func[2]))
    else:
        raise Exception('Error: funcion {} no declarada'.format(p[-1]))

# argumento

def p_argumento_loop(p):
    '''
    argumento_loop : hyper_exp np_fc_2 argumento_loop_1
                   | epsilon
    '''
def p_argumento_loop_1(p):
    '''
    argumento_loop_1 : ',' hyper_exp np_fc_2 argumento_loop_1
                     | epsilon
    '''

#loop hyper_exp
def p_hyper_exp_loop(p):
    '''
    hyper_exp_loop : hyper_exp np_add_to_input_counter hyper_exp_loop_1
    '''

#loop hyper_exp_1
def p_hyper_exp_loop_1(p):
    '''
    hyper_exp_loop_1 : ',' hyper_exp np_add_to_input_counter hyper_exp_loop_1
                     | epsilon
    '''

def p_np_fc_2(p):
    '''
    np_fc_2 : epsilon
    '''
    curr_p_count = call_stack[-1][1][0]
    curr_p_len = call_stack[-1][1][1]
    curr_f_name = call_stack[-1][0]

    # Verifica si se llamo con parametros extra
    if curr_p_count >= curr_p_len:
        raise Exception('Error: llamada a funcion con parametros extra')
    dir, tipo = operand_stack.pop()
    #[func] -> [params] ->[param][type]
    # obtiene el tipo esperado del parametro
    curr_p_type, curr_p_name = func_dir.dir[curr_f_name][2][curr_p_count]
    # verifica si los tipos son iguales
    if curr_p_type != tipo:
        raise Exception('Error: tipos incompatibles en llamada a funcion. {} != {}'.format(curr_p_type, tipo))
    else:
        _,p_dir = func_dir.search_var(curr_f_name, curr_p_name)
    # agregar cuadruplo
    quadruples.gen_quad('PARAM', dir, -1, p_dir)
    # aumentar contador de parametros (k)
    call_stack[-1][1][0] += 1

# func return
def p_func_return(p):
    '''
    func_return : RETURN '(' hyper_exp ')' ';'
    '''
    dir, tipo = operand_stack.pop()
    # se busca la variable global de retorno
    tipoRet, dirRet = func_dir.search_var(curr_func, '_' + curr_func)
    if tipo != tipoRet:
        raise Exception('Error: tipos incompatibles en return. {} != {}'.format(tipo, tipoRet))
    quadruples.gen_quad('RETURN', dir, -1, dirRet)

# Read
def p_read(p):
    '''
    read : READ '(' variable_loop ')' ';'
    '''
    global input_counter, operand_stack, quadruples
    for i in range(0,input_counter):
        # obtener datos de operandos
        opdir, _ = operand_stack.pop()
        # agregar cuadruplo
        quadruples.gen_quad('READ', -1, -1, opdir)
    input_counter = 0
    

# Variable loop
def p_variable_loop(p):
    '''
    variable_loop : variable np_add_to_input_counter variable_loop_1
    '''
    # p[0] = [p[1]] + p[2]

# Variable loop 1
def p_variable_loop_1(p):
    '''
    variable_loop_1 : ',' variable np_add_to_input_counter variable_loop_1
                    | epsilon
    '''
    # if len(p) == 4:
    #     p[0] = [p[2]] + p[3]
    # else:
    #     p[0] = []

def p_np_add_to_input_counter(p):
    '''
    np_add_to_input_counter : epsilon
    '''
    # agregar a input counter
    global input_counter
    input_counter += 1

# Write
def p_write(p):
    '''
    write : WRITE '(' hyper_exp_loop ')' ';'
    '''
    global input_counter, operand_stack, quadruples
    for i in range(0,input_counter):
        # obtener datos de operandos
        opdir, _ = operand_stack.pop()
        # agregar cuadruplo
        quadruples.gen_quad('WRITE', -1, -1, opdir)
    input_counter = 0

# Decision
def p_decision(p):
    '''
    decision : IF '(' hyper_exp ')' np_decision_1 THEN '{' loop_estatuto '}'  decision_else
    '''
    #obtener fin de condicion
    fin_decision = jump_stack.pop()
    # agregar cuadruplo
    quadruples.fill_quad(fin_decision, 3, quadruples.counter)

# Decision 1
def p_decision_else(p):
    '''
    decision_else : ELSE np_decision_2 '{' loop_estatuto '}' 
                  | epsilon
    '''

def p_np_decision_1(p):
    '''
    np_decision_1 : epsilon
    '''
    dir, tipo = operand_stack.pop()
    if tipo != 'bool':
        raise Exception('Error: tipos incompatibles en decision. {} != bool'.format(tipo))
    else:
        # agregar cuadruplo
        quadruples.gen_quad('GOTOF', dir, -1, None)
        # agregar a jump stack
        jump_stack.append(quadruples.counter - 1)

def p_np_decision_2(p):
    '''
    np_decision_2 : epsilon
    '''
    # Crea cuadruplo
    quadruples.gen_quad('GOTO', -1, -1, None)
	# guarda el cuadruplo en el stack de saltos
    false_way = jump_stack.pop()
    jump_stack.append(quadruples.counter - 1)
	# rellena el cuadruplo anterior
    quadruples.fill_quad(false_way, 3, quadruples.counter)



# loop estatuto
# TODO: determinar si es necesario ya que creo que todas las instancias de estatuto son opcionales
# manda un estatuto obligatorio y luego opcionales
def p_loop_estatuto(p):
    '''
    loop_estatuto : estatuto loop_estatuto
                  | epsilon
    '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

# Repeticion
def p_repeticion(p):
    '''
    repeticion : condicional
               | no_condicional
    '''

# Condicional
def p_condicional(p):
    '''
    condicional : WHILE np_cond_1 '(' hyper_exp ')' np_cond_2 DO '{' loop_estatuto '}' np_cond_3
    '''

def p_np_cond_1(p):
    '''
    np_cond_1 : epsilon
    '''
    # agregar a jump stack
    global jump_stack, quadruples
    jump_stack.append(quadruples.counter)

def p_np_cond_2(p):
    '''
    np_cond_2 : epsilon
    '''
    # obtener datos de operandos
    dir, tipo = operand_stack.pop()
    if tipo != 'bool':
        raise Exception('Error: tipos incompatibles en condicional. {} != bool'.format(tipo))
    else:
        # agregar cuadruplo
        quadruples.gen_quad('GOTOF', dir, -1, None)
        # agregar a jump stack
        jump_stack.append(quadruples.counter - 1)

def p_np_cond_3(p):
    '''
    np_cond_3 : epsilon
    '''
    # obtener fin de condicion
    fin_cond = jump_stack.pop()
    # obtener inicio repeticion de condicion
    repeticion_cond = jump_stack.pop()
    # agregar cuadruplo
    quadruples.gen_quad('GOTO', -1, -1, repeticion_cond)
    # agregar a jump stack
    jump_stack.append(quadruples.counter - 1)
    # rellenar cuadruplo
    quadruples.fill_quad(fin_cond, 3, quadruples.counter)

# No condicional
# usar id en lugar de variable, por que usaria una casilla de algun array en un for ?
def p_no_condicional(p):
    '''
    no_condicional : FOR variable '=' hyper_exp np_for_1 TO hyper_exp np_for_2 DO np_for_3 '{' loop_estatuto '}' 
    '''
    # global curr_dir
    quadruples.gen_quad('+', curr_dir_for, dir_uno, curr_dir_for)
    # obtener fin de condicion
    fin_cond = jump_stack.pop()
    # obtener inicio repeticion de condicion
    repeticion_cond = jump_stack.pop()
    
    # agregar cuadruplos: suma 1 a la variable de control, GOTO
    # quadruples.gen_quad('+', curr_dir, dir_uno, curr_dir)
    quadruples.gen_quad('GOTO', -1, -1, repeticion_cond)
    # agregar a jump stack
    jump_stack.append(quadruples.counter - 1)
    # rellenar cuadruplo
    quadruples.fill_quad(fin_cond, 3, quadruples.counter)
    

# se realiza la asignacion con la diferencia que se guarda
# la direccion de la asignacion en el stack de operandos
def p_np_for_1(p):
    '''
    np_for_1 : epsilon
    '''
    # obtener datos de operandos
    global curr_dir_for, curr_type_for
    dir2, tipo2 = operand_stack.pop()
    curr_dir_for, curr_type_for = operand_stack.pop()
    # tipos iguales
    if curr_type_for != 'int' or tipo2 != 'int':
        raise Exception('Error: tipos incompatibles en no_condicional. Se esperaba: int,int. Se obtuvo: {} '.format(curr_type_for, tipo2))        
    # agregar cuadruplo
    quadruples.gen_quad('=', dir2, -1, curr_dir_for)
    # agregar a operand stack
    operand_stack.append((curr_dir_for, curr_type_for))

def p_np_for_2(p):
    '''
    np_for_2 : epsilon
    '''
    # obtener datos de operando
    _, tipo = operand_stack[-1]
    # validar tipo
    if tipo != 'int':
        raise Exception('Error: tipo incompatibles en segundo valor no_condicional. Se esperaba: int. Se obtuvo: {} '.format(tipo))
    # # agregar cuadruplo
    # one_dir = func_dir.add_const('int', '1')
    # quadruples.gen_quad('-', dir, one_dir, dir)

def p_np_for_3(p):
    '''
    np_for_3 : epsilon
    '''
    # agregar a jump stack
    global jump_stack, quadruples
    jump_stack.append(quadruples.counter) # apunta al codigo que se va a repetir
    # obtener datos de operandos
    limite_sup, _ = operand_stack.pop()
    curr_dir, _ = operand_stack.pop()
    dir_bool = func_dir.add_var(curr_func, 'bool')
    # se compara val1 > val2, esto hace incluyente con
    quadruples.gen_quad('>', curr_dir, limite_sup, dir_bool)
    quadruples.gen_quad('GOTOV', dir_bool, -1, None)
    # agregar a jump stack
    jump_stack.append(quadruples.counter - 1) # el gotov que quiero llena
  



 

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
        result_type = semantic_cube.is_match((operator,op1[1], op2[1]))
        # direccion
        result_dir = func_dir.add_var(curr_func, result_type)
        if result_type:
            # agregar cuadruplo
            quadruples.gen_quad(operator, op1[0], op2[0],result_dir)
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
        result_type = semantic_cube.is_match((operator,op1[1], op2[1]))
        # direccion
        result_dir = func_dir.add_var(curr_func, result_type)
        if result_type:
            # agregar cuadruplo
            quadruples.gen_quad(operator, op1[0], op2[0],result_dir)
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
        result_type = semantic_cube.is_match((operator,op1[1], op2[1]))
        # direccion
        result_dir = func_dir.add_var(curr_func, result_type)
        if result_type:
            # agregar cuadruplo
            quadruples.gen_quad(operator, op1[0], op2[0],result_dir)
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
        result_type = semantic_cube.is_match((operator,op1[1], op2[1]))
        # direccion
        result_dir = func_dir.add_var(curr_func, result_type)
        if result_type:
            # agregar cuadruplo
            quadruples.gen_quad(operator, op1[0], op2[0],result_dir)
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

# push and pop
def p_np_push_operator_stack(p):
    '''
    np_push_operator_stack : epsilon
    '''
    # push operador a stack
    global operator_stack
    operator_stack.append(p[-1])

def p_np_pop_operator_stack(p):
    '''
    np_pop_operator_stack : epsilon
    '''
    # push operador a stack
    global operator_stack
    operator_stack.pop()

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
# TODO: read?
def p_factor(p):
    '''
    factor : constant
           | variable
           | '(' hyper_exp ')'
           | func_llamada
           | read
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
    np_push_const_int : epsilon
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

def p_np_single_var_process(p):
    '''
    np_single_var_process : epsilon
    '''
    # buscar variable en dirFunc
    global func_dir, curr_func
    #
    tipo, dir = func_dir.search_var(curr_func, p[-1])
    operand_stack.append((dir, tipo))

def p_np_array_var_process(p):
    '''
    np_array_var_process : epsilon
    '''
    # buscar variable en dirFunc
    global func_dir, curr_func
    # obteniendo datos para la formula 
    s1_dir, s1_type = operand_stack.pop()
    type_base, dir_base = func_dir.search_var(curr_func, p[-6])
    dim = func_dir.get_dims(curr_func, p[-6])
    if dim :
        dim = int(dim)
    if s1_type != 'int':
        raise Exception('Error: tipos incompatibles en array. {} != int'.format(s1_type))
    
    # formula
    # print( dim, s1_dir)
    quadruples.gen_quad('VER', 1, dim, s1_dir)
    point = func_dir.add_var(curr_func, 'pointer')
    quadruples.gen_quad('+', s1_dir, dir_menos_uno, s1_dir)
    quadruples.gen_quad('+dir', s1_dir, dir_base, point)
    # quadruples.gen_quad('+dir', point, dir_menos_uno, point)
    operand_stack.append((point, type_base ))

def p_epsilon(p):
    '''epsilon : '''
    p[0] = 'epsilon'

def p_error(p):
    if not p:
        error_msg = "Syntax error"
    else:
        error_msg = 'syntax error in line ' + \
            str(p.lineno) + ' when parsing ' + str(p)
    raise SyntaxError(error_msg)

parser = yacc.yacc()
