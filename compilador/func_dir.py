from vars_table import VarsTable

class FuncDir:
    # formato de directorio de funciones:
    # 
    # 'nombre': [tipo, varsTable, params, ret],
    # 
    #  nombre: puede ser global, const, "funcion"
    def __init__(self):
        self.dir = {}   

    # agregar funcion a dirFunc
    def add_func(self, func, tipo):
        if not self.dir.get(func):
            self.dir[func] = [tipo, None, [], None]
        else:
            raise Exception('Funcion {} ya declarada'.format(func))
        
    # agregar tabla de variables a funcion
    def add_varstable(self, func, scope):
        if self.dir.get(func):
            self.dir[func][1] = VarsTable(scope)
        else:
            raise Exception('Funcion {} no declarada'.format(func))

    # agregar variable a varstable
    def add_var(self, func, type, varName):
        if self.dir.get(func):
            return self.dir[func][1].add_var(type, varName)
        else:
            raise Exception('Funcion {} no declarada'.format(func))
    
    # agregar constante a dirFunc
    def add_const(self, func, type, constVal):
        # si no existia, crear tabla de constantes 
        if 'const' not in self.dir.keys():
            self.dir['const'] = ['void', VarsTable('const'), None, None]
        else:
           #  const : varstable.add_const(type, constVal)
           return self.dir['const'][1].add_const(type, constVal)
        
    # agregar parametro a funcion
    # a su vez agrega el parametro a la varstable de dicha funcion
    def add_param(self, func, type, param):
        if self.dir.get(func):
            self.dir[func][2].append((type, param))
            #  const : varstable.add_var(type, varName)
            return self.add_var(func, type, param)
        else:
            raise Exception('Funcion {} no declarada'.format(func))
        

    # saber si existe varsTable en funcion
    def has_varstable(self, func):
        if self.dir.get(func):
            return self.dir[func][1] != None
        else:
            raise Exception('Funcion {} no declarada'.format(func))