class VarsTable:
    def __init__(self, scope):
        # scope: global, local, const
        # cada scope tiene su propia tabla de variables
        # {nombre_variable: tipo_variable, lugar}
        # cada scope tiene su propio contador de variables
        # local cuenta con un contador de variables locales
        # {tipo_variable: contador}

        if scope == 'global':
            self.table = {
                'global': {}
            }
            self.counter = {
                'global': {
                    'int': 0,
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
                    'bool': 13000
                }
            }
        elif scope == 'const':
            self.table = {
                'const': {}
            }
            self.counter = {
                'const': {
                    'int': 16000,
                    'float': 17000,
                    'char': 18000,
                    'bool': 19000
                }
            }