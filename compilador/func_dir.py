from vars_table import VarsTable

'''
    formato de directorio de funciones:
    {
        'funcion': [tipo, varsTable]
    }

'''

class FuncDir:
    def __init__(self):
        self.dir = {
            'global': ['void', VarsTable('global')]
        }

    def insert_func(self, func, tipo):
        if (not self.dir.get(func)):
            self.dir[func] = [tipo, VarsTable('local')]
