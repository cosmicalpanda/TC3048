# clase para comparar los tipos de expresiones 
# dict que mapea todas las combinaciones validas de operador con operandos y retorno
# combinaciones que no estan en el diccionario son invalidas
class SemanticCube:
    def __init__(self):
        '''
        Tipos de datos:
        - int
        - float
        - bool 
        - char

        Operadores:
        - suma (+)
        - resta (-)
        - multiplicacion (*)
        - division (/)
        - and (&)
        - or (|)
        - mayor que (>)
        - menor que (<)
        - igual que (==)
        - diferente que (!=)
        '''
        self.cubo = {
            # suma
            ('+', 'int', 'int')         : 'int',
            ('+', 'int', 'float')       : 'float',
            ('+', 'float', 'int')       : 'float',
            ('+', 'float', 'float')     : 'float',

            # resta
            ('-', 'int', 'int')         : 'int',
            ('-', 'int', 'float')       : 'float',
            ('-', 'float', 'int')       : 'float',
            ('-', 'float', 'float')     : 'float',

            # multiplicacion
            ('*', 'int', 'int')         : 'int',
            ('*', 'int', 'float')       : 'float',
            ('*', 'float', 'int')       : 'float',
            ('*', 'float', 'float')     : 'float',

            # division
            ('/', 'int', 'int')         : 'int',
            ('/', 'int', 'float')       : 'float',
            ('/', 'float', 'int')       : 'float',
            ('/', 'float', 'float')     : 'float',

            # logicos
            ('&', 'bool', 'bool')       : 'bool',
            ('|', 'bool', 'bool')       : 'bool',

            # relacionales
            # mayor que
            ('>', 'int', 'int')         : 'bool',
            ('>', 'int', 'float')       : 'bool',
            ('>', 'float', 'int')       : 'bool',
            ('>', 'float', 'float')     : 'bool',
            # menor que
            ('<', 'int', 'int')         : 'bool',
            ('<', 'int', 'float')       : 'bool',
            ('<', 'float', 'int')       : 'bool',
            ('<', 'float', 'float')     : 'bool',
            # igual que
            ('==', 'int', 'int')        : 'bool',
            ('==', 'int', 'float')      : 'bool',
            ('==', 'float', 'int')      : 'bool',
            ('==', 'float', 'float')    : 'bool',
            ('==', 'char', 'char')    : 'bool',
            ('==', 'bool', 'bool')    : 'bool',
            # diferente que
            ('!=', 'int', 'int')        : 'bool',
            ('!=', 'int', 'float')      : 'bool',
            ('!=', 'float', 'int')      : 'bool',
            ('!=', 'float', 'float')    : 'bool',
            ('!=', 'char', 'char')      : 'bool',
            ('!=', 'bool', 'bool')      : 'bool',
        }

    # funcion para retornar el tipo correspondiente para la expresion
    def is_match(self, tupla):
        tipo = self.cubo.get(tupla)
        if tipo:
            return tipo
        else:
            raise Exception("Tipos incompatibles: " + tupla[1] + " " + tupla[0] + " " + tupla[2])