class VarsTable:
    def __init__(self, scope):
        # scope: global, local, const
        self.scope = scope

        # cada scope tiene su propia tabla de variables
        # {nombre_variable: tipo_variable, direccion}
        # cada scope tiene su propio contador de variables
        # local cuenta con un contador de variables locales
        # {nombre: tipo, dir, dims }

        if scope == 'global':
            self.table = {
                'global': {}
            }
            self.counter = {
                'global': {
                    'int': 0000,
                    'float': 1000,
                    'char': 2000,
                    'bool': 3000
                }
            }
        elif scope == 'local':
            self.table = {
                'local': {},
                'temp': {}
            }
            self.counter = {
                'local': {
                    'int': 5000,
                    'float': 6000,
                    'char': 7000,
                    'bool': 8000
                },
                'temp': {
                    'int': 10000,
                    'float': 11000,
                    'char': 12000,
                    'bool': 13000,
                    'pointer': 14000
                }
            }
        elif scope == 'const':
            self.table = {
                'const': {}
            }
            self.counter = {
                'const': {
                    'int': 20000,
                    'float': 21000,
                    # no se si char y/o str se usen en la hora de de imprimir letreros
                    'char': 22000,
                    # 'str': 23000,
                }
            }
    
    # Add
    # Funcion para agregar una variable a la tabla de variables
    # regresa la direccion de la variable
    # TODO: codigo para agregar arreglos 
    def add_var(self, type, varName=None, dim=1):
        # en caso de no tener varName es temporal
        if varName:
            # si es una variable nueva proceder
            if not self.table[self.scope].get(varName):
                # agregar a la tabla de variables con el formato:
                # {varName: (type, dir, dim)}
                # ejemplo: {'a': ('int', 5000, 2)}
                self.table[self.scope][varName] = (type, self.counter[self.scope][type], dim)
                prev_size = self.counter[self.scope][type]
                # incrementar contador
                if dim:
                    # NOTA k = -1 ya que se es indice 1 -> dim
                    self.counter[self.scope][type] += int(dim)
                else:   
                    self.counter[self.scope][type] += 1 
                if prev_size // 1000 != self.counter[self.scope][type] // 1000:
                    raise Exception('Se excedio el limite de variables de tipo {}'.format(type))
                # retorna la direccion de la variable
                # print('added var {} to scope {}'.format(varName, self.scope))
                return self.counter[self.scope][type] - 1
            # si ya existe declarar error
            else:
                raise Exception('Error llamando add_var. Variable "{}" ya declarada de tipo {}'.format(varName, self.table[self.scope][varName][0]))
        else:
            # solo se pueden agregar temporales a funciones locales
            if self.scope != 'local':
                raise Exception('No se puede agregar variable temporal a scope {}'.format(self.scope))    
            new_temp = type + str(self.counter['temp'][type] % 1000)
            # agregar a la tabla de variables temporales con el formato:
            # {new_temp: (type, dir)}
            # ejemplo: {'int10000': ('int', 10000, False)}
            self.table['temp'][new_temp] = (type, self.counter['temp'][type], dim)
            # actualiza counter
            self.counter['temp'][type] += 1
            # retorna la direccion del temporal
            return self.counter['temp'][type] - 1


    # Funcion para agregar un valor constante a la tabla de constantes
    # regresa la direccion de la constante
    def add_const(self, type, constVal):
        # checar si ya existe la constante
        # dir = self.table['const'].get(constVal)
        # print("dir->>>>>>>>>>>>>>>>:", dir, constVal)
        # si existe, regresar direccion
        if constVal in self.table['const'].keys():
            print("constante repetida", constVal, self.table['const'])
            return self.table['const'][constVal][1]
        # else, agregar a la tabla
        else:
            print("agregando constante", constVal)
            # agregar a la tabla de constantes con el formato:
            # {constVal: (type, dir)}
            self.table['const'][constVal] = (type, self.counter['const'][type])
            # actualiza counter
            self.counter['const'][type] = self.counter['const'][type] + 1
            # retorna la direccion de la constante
            return self.counter['const'][type] - 1