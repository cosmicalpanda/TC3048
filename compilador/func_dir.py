from vars_table import varsTable

'''
    formato de directorio de funciones:
    {
        'funcion': [tipo, varsTable]
    }

'''

class funcDir:
    def __init__(self):
        self.dir = {
            'global': ['void', varsTable('global')]
        }

    def insert_func(self, func, tipo):
        if (not self.dir.get(func)):
            self.dir[func] = [tipo, varsTable('local')]
