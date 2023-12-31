
'''
func_dir.py

Clase para el directorio de funciones

Tiene las funciones para agregar funciones y a estas modificar variables, parametros, cuadruplo inicial y cuadruplo de retorno
'''
from vars_table import VarsTable

class FuncDir:
    # formato de directorio de funciones:
    # 
    # 'nombre': [retType, varsTable, params, cuadruplo_inicial , retorno],
    # 
    #  nombre: puede ser global, const, "funcion"
    def __init__(self):
        self.dir = {
            'main': ['void', VarsTable('local'), [], None, None]
        }   
 
    # agregar funcion a dirFunc
    # si ya existe, lanzar excepcion
    def add_func(self, func, retType):
        if not self.dir.get(func):
            self.dir[func] = [retType, None, [], None, None]
        else:
            raise Exception('Error llamando add_func. Funcion {} ya declarada'.format(func))
        
    # agregar tabla de variables a funcion
    # si no existe la funcion, lanzar excepcion
    def add_varstable(self, func, scope):
        if self.dir.get(func):
            self.dir[func][1] = VarsTable(scope)
        else:
            raise Exception('Error llamando add_varstable. Funcion {} no declarada'.format(func))

    # agregar variable a varstable
    # retorna la direccion de la variable en caso correcto
    def add_var(self, func, type, varName=None, dim=None):
        if self.dir.get(func):
            # print('adding var {} to func {}'.format(varName, func))
            return self.dir[func][1].add_var(type, varName, dim)
        else:
            raise Exception('Error llamando add_var. Funcion {} no declarada'.format(func))
    
    # agregar constante a dirFunc
    # retorna la direccion de la constante agregada
    def add_const(self, type, constVal):
        # si no existia, crear tabla de constantes 
        if 'const' not in self.dir.keys():
            self.dir['const'] = ['void', VarsTable('const'), None, None, None]
        #  const : varstable.add_const(type, constVal)
        return self.dir['const'][1].add_const(type, constVal)
        
    # agregar parametro a funcion
    # a su vez agrega el parametro a la varstable de dicha funcion
    # retorna la direccion del parametro agregado
    def add_param(self, func, type, param):
        if self.dir.get(func):
            # print('adding param {} to func {}'.format(param, func))
            self.dir[func][2].append((type, param))
            #  const : varstable.add_var(type, varName)
            return self.add_var(func, type, param)
        else:
            raise Exception('Error llamando add_param. Funcion {} no declarada'.format(func))
        
    # saber si existe varsTable en funcion
    # retorna True si existe, False si no
    # si no existe la funcion, lanzar excepcion
    def has_varstable(self, func):
        if self.dir.get(func):
            return self.dir[func][1] != None
        else:
            raise Exception('Error llamando has_varstable. Funcion {} no declarada'.format(func))
        
    # encontrar variable en dirFunc
    # busca func -> global
    # retorna tipo, direccion
    def search_var(self, func, varName):
        # print("searching var {} in func {}".format(varName, func))
        if self.dir[func][1]:
            var = self.dir[func][1].table['local'].get(varName)
            if var:
                return var[0], var[1]
        if self.dir['global'][1]:
            var = self.dir['global'][1].table['global'].get(varName)
            if var:
                return var[0], var[1]
        raise Exception('Error llamando search_var. Variable {} no declarada'.format(varName))

    # add_return
    # agregar cuadruplo donde se guarda el valor de retorno de una funcion
    # si no existe la funcion, lanzar excepcion
    def add_return(self, func, return_dir):
        if self.dir.get(func):
            self.dir[func][4] = return_dir
        else:
            raise Exception('Error llamando add_return. Funcion {} no declarada'.format(func))

    # regresa la tabla de constantes
    def get_const_table(self):
        if 'const' in self.dir.keys():
            return self.dir['const'][1].table['const']
        
    # get counter
    # se utiliza para la tabla de contadores de una funcion
    def get_counter(self, func):
        if self.dir[func][1]:
            return self.dir[func][1].counter
        else:
           return None
        
    # obtiene el cuadruplo inicial de una funcion
    def get_quad(self, func):
        if self.dir.get(func):
            return self.dir[func][3]
        else:
            raise Exception('Error llamando get_quad. Funcion {} no declarada'.format(func))

    # obtiene el tipo de retorno de una funcion
    def get_func_type(self, func):
        if self.dir.get(func):
            return self.dir[func][0]
        else:
            raise Exception('Error llamando get_func_type. Funcion {} no declarada'.format(func))

    # obtiene las dimensiones de una variable
    # primero busca en la tabla de variables locales, despues en la global
    def get_dims(self, func, varName):
        if self.dir[func][1]:
            var = self.dir[func][1].table['local'].get(varName)
            if var:
                return var[2]
        if self.dir['global'][1]:
            var = self.dir['global'][1].table['global'].get(varName)
            if var:
                return var[2]
        else:
            raise Exception('Error llamando get_dims. Funcion {} no declarada'.format(func))