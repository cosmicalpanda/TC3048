'''
memory_table.py

Clase que instancia espacios de memoria vacios dependiendo de los contadores especificados
'''
class MemoryTable:
    def __init__(self):
        self.table = {}

    '''
    global: {
        int: []
        float: []
        char: []
        bool: []
    }

    Or ->
    local: {
        int: []
        float: []
        char: []
        bool: []
    }
    temp: {
        int: []
        float: []
        char: []
        bool: []
    }

    or ->
    const: {
        int: []
        float: []
        char: []
    }
    
    '''
    # para cada alcance, crea una tabla de memoria con la cantidad de espacios especificados por tipo
    def init(self, counter):
        if counter:
            for scope in counter.keys():
                # crea un nuevo espacio de memoria para el alcance
                # puede ser: Global, Local, Temporal, Constante
                self.table[scope] = {}
                # Para cada tipo de valor en el alcance
                for tipo in counter[scope].keys():
                    tam = counter[scope][tipo]
                    self.table[scope][tipo] = [None] * (tam % 1000)
