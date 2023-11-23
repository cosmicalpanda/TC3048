from memory_table import MemoryTable
class Memory:
    def __init__(self) :
        # Modelada de acuerdo a varstable
        '''
        Global
        0000 - 0999 : int
        1000 - 1999 : float
        2000 - 2999 : char
        3000 - 3999 : bool

        Local
        5000 - 5999 : int
        6000 - 6999 : float
        7000 - 7999 : char
        8000 - 8999 : bool

        Temp
        10000 - 10999 : int
        11000 - 11999 : float
        12000 - 12999 : char
        13000 - 13999 : bool

        Constantes
        20000 - 20999 : int
        21000 - 21999 : float
        22000 - 22999 : char (?)
        '''
        self.func_stack = []    
        self.mem = []
        self.global_mem = MemoryTable()
        self.const_mem = MemoryTable()
        self.total_mem = 0

    # crear la tabla de espacios dependiendo del scope
    def init(self, scope, counter):
        if scope == 'global':
            self.global_mem.init(counter)
        elif scope == 'const':
            self.const_mem.init(counter)
        elif scope == 'main':
            # creamos la memoria para el main y agregamos al stack
            self.era(counter)
            self.mem_stack()

    # stack
    def mem_stack(self):
        #agregamos memoria al stack
        self.func_stack.append(self.mem.pop())


    # era
    def era(self, counter):
        self.mem.append(MemoryTable())
        self.mem[-1].init(counter)
        # self.func_stack.append(self.mem.pop())
        print("era", counter)

    # param
    def param(self):
        pass
    
    # asign space
    def assign_space(self, dir, value):
        scope = self.dir_scope(dir)
        tipo = self.dir_type(dir)
        index = dir % 1000
        print("assign", scope, tipo, index, dir, value)
        if scope == 'local' or scope == 'temp':
            print("cobo1")
            print(len(self.func_stack))
            for i in self.func_stack[-1].table.keys():
                print(i)
            self.func_stack[-1].table[scope][tipo][index] = value
        elif scope == 'global':
            print("cobo3",value)
            self.global_mem.table[scope][tipo][index] = value
            print(self.global_mem.table[scope][tipo][index])
        elif scope == 'const':
            print("cobo2")
            self.const_mem.table[scope][tipo][index] = value

    # search space
    def search_space(self, dir):
        scope = self.dir_scope(dir)
        tipo =  self.dir_type(dir)
        index = dir % 1000
        if scope == 'local' or scope == 'temp':
            ans = self.func_stack[-1].table[scope][tipo][index]
            if ans == None:
                raise Exception("Error: Casilla {} no inicializada".format(dir))
            return ans            
        elif scope == 'global':
            # print(scope, tipo, index)
            for a in self.global_mem.table.keys():
                print(a, self.global_mem.table[a])
            print ("aja")
            ans = self.global_mem.table[scope][tipo][index]
            if ans == None:
                raise Exception("Error: Casilla {} no inicializada".format(dir))
            return ans
        elif scope == 'const':
            ans = self.const_mem.table[scope][tipo][index]
            print(ans)
            if ans == None:
                raise Exception("Error: Casilla {} no inicializada".format(dir))
            return ans
        pass

    # init const  │{'1': ('int', 20000)}
    #
    def init_const(self, constants):
        for c in constants:
            print(c)
            if constants[c][0] == 'int':
                self.assign_space(constants[c][1], int(c))
            elif constants[c][0] == 'float':
                self.assign_space(constants[c][1], float(c))
        pass

    def dir_scope(self,dir):
        if dir < 5000:
            return 'global'
        elif dir < 10000:
            return 'local'
        elif dir < 20000:
            return 'temp'
        else:
            return 'const'
        
    def dir_type(self,dir):
        if dir < 1000 or (dir >= 5000 and dir < 6000) or (dir >= 10000 and dir < 11000) or (dir >= 20000 and dir < 21000):
            return 'int'
        elif dir < 2000 or (dir >= 6000 and dir < 7000) or (dir >= 11000 and dir < 12000) or (dir >= 21000 and dir < 22000):
            return 'float'
        elif dir < 3000 or (dir >= 7000 and dir < 8000) or (dir >= 12000 and dir < 13000) or (dir >= 22000 and dir < 23000):
            return 'char'
        else:
            return 'bool'