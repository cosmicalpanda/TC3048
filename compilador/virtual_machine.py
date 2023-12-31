'''
virtual_machine.py

Maquina virtual que corre los cuadruplos generados por el compilador
requiere una lista de cuadruplos, un diccionario de contadores y un diccionario de constantes
'''
# Virtual Machine
from memory import Memory
import pprint
import math
import random
import numpy as np

class VM:
    def __init__(self,quadruples, counters, constants):
        self.quadruples = quadruples
        self.pointer_stack = [0]
        self.counters = counters
        self.memory = Memory()
        self.constants = constants

    def run(self):
        while (self.pointer_stack[-1] < len(self.quadruples)):
            opcode = self.quadruples[self.pointer_stack[-1]][0]
            op1 = self.quadruples[self.pointer_stack[-1]][1]
            op2 = self.quadruples[self.pointer_stack[-1]][2]
            dir = self.quadruples[self.pointer_stack[-1]][3]
            # check for pointers
            # print(opcode, op1, op2, dir)
            if opcode not in ['ERA', '+dir']:
                if op1 >= 14000 and op1 < 15000:
                    op1 = self.memory.search_space(op1)
                if op2 >= 14000 and op2 < 15000:
                    op2 = self.memory.search_space(op2)
                if dir >= 14000 and dir < 15000:
                    dir = self.memory.search_space(dir)
            # aritmetica
            if opcode == '+':
                # print( "dir: {} + dir: {} goes to dir: {}".format(op1,op2,dir))
                # self.memory.assign_space(dir,  )
                self.memory.assign_space(dir, self.memory.search_space(op1) + self.memory.search_space(op2))
            elif opcode == '-':
                # print( "dir: {} - dir: {} goes to dir: {}".format(op1,op2,dir))
                # print( "val: {} - val: {} goes to dir: {}".format(self.memory.search_space(op1),self.memory.search_space(op2),dir))
                self.memory.assign_space(dir, self.memory.search_space(op1) - self.memory.search_space(op2))
            elif opcode == '*':
                self.memory.assign_space(dir, self.memory.search_space(op1) * self.memory.search_space(op2))    
            elif opcode == '/':
                if self.memory.dir_type(dir) == 'float': 
                    self.memory.assign_space(dir, self.memory.search_space(op1) / self.memory.search_space(op2))
                else:
                    self.memory.assign_space(dir, self.memory.search_space(op1) // self.memory.search_space(op2))
            elif opcode == '&':
                # print( " {} and {} ".format(self.memory.search_space(op1), self.memory.search_space(op2)))
                # print( self.memory.search_space(op1) and self.memory.search_space(op2))
                self.memory.assign_space(dir, self.memory.search_space(op1) and self.memory.search_space(op2))
            elif opcode == '|':
                # print( " {} or {} ".format(self.memory.search_space(op1), self.memory.search_space(op2)))
                # print( self.memory.search_space(op1) or self.memory.search_space(op2))
                self.memory.assign_space(dir, self.memory.search_space(op1) or self.memory.search_space(op2))
            elif opcode == '<':
                self.memory.assign_space(dir, self.memory.search_space(op1) < self.memory.search_space(op2))
            elif opcode == '>':
                self.memory.assign_space(dir, self.memory.search_space(op1) > self.memory.search_space(op2))
            elif opcode == '==':
                self.memory.assign_space(dir, self.memory.search_space(op1) == self.memory.search_space(op2))
            elif opcode == '!=':
                self.memory.assign_space(dir, self.memory.search_space(op1) != self.memory.search_space(op2))
            elif opcode == '=':
                # print("dir1: {} = dir2: {}".format(dir, op1))
                self.memory.assign_space(dir, self.memory.search_space(op1))
            elif opcode == '+dir':
                if op1 >= 14000 and op1 < 15000:
                    op1 = self.memory.search_space(op1)
                # print("dir1: {}, {}, {} ".format(dir, self.memory.search_space(op1) -1, op2))
                self.memory.assign_space(dir, self.memory.search_space(op1) + op2 -1)
                # self.memory.assign_space(dir, self.memory.search_space(op1) + op2 )
            elif opcode == 'VER':
                temp = self.memory.search_space(dir)
                #arrays start in 1
                temp -= 1
                if temp <0 or temp >=op2:
                    raise Exception("Error: indice {} fuera de rango: {} -> {}".format(temp, 1,op2))
            elif opcode == 'WRITE':
                # print("write: ", self.memory.search_space(dir))
                print(self.memory.search_space(dir))
            elif opcode == 'READ':
                temp = input()
                if self.memory.dir_type(dir) == 'int':
                    temp = int(temp)
                elif self.memory.dir_type(dir) == 'float':
                    temp = float(temp)
                self.memory.assign_space(dir, temp)
            #funciones especiales
            elif opcode == 'rand':
                rand = random.randint(self.memory.search_space(op1), self.memory.search_space(op2))
                self.memory.assign_space(dir, rand)
            elif opcode == 'media':
                sum = 0
                limit = self.memory.search_space(op2)
                # print("Obteniendo media de {} elementos".format(limit))
                for i in range(limit):
                    # print (i, op1+i)
                    sum += self.memory.search_space(op1 + i)
                    # print(sum)
                media = sum / limit
                self.memory.assign_space(dir, media)
            elif opcode == 'mediana':
                values = []
                limit = self.memory.search_space(op2)
                for i in range(limit):
                    values.append(self.memory.search_space(op1 + i))
                values_sorted = sorted(values)
                if limit % 2:
                    mediana = values_sorted[limit // 2]
                else:
                    mediana = (values_sorted[limit // 2] + values_sorted[(limit // 2 ) + 1]) / 2
                self.memory.assign_space(dir, mediana)
            elif opcode == 'moda':
                values = {}
                limit = self.memory.search_space(op2)
                for i in range(limit):
                    value = self.memory.search_space(op1 + i)
                    if value in values.keys():
                        values[value] += 1
                    else:
                        values[value] = 1
                maxVal = max(values, key=values.get)
                self.memory.assign_space(dir, maxVal)
            elif opcode == 'varianza':
                values = []
                limit = self.memory.search_space(op2)
                for i in range(limit):
                    values.append(self.memory.search_space(op1 + i))
                varianza = np.var(values)
                self.memory.assign_space(dir, varianza)
            elif opcode == 'len':
                limit = self.memory.search_space(op2)
                self.memory.assign_space(dir, limit)
            elif opcode == 'sen':
                self.memory.assign_space(dir, math.sin(self.memory.search_space(op1)))
            elif opcode == 'cos':
                self.memory.assign_space(dir, math.cos(self.memory.search_space(op1)))
            elif opcode == 'tan':
                self.memory.assign_space(dir, math.tan(self.memory.search_space(op1)))
            elif opcode == 'senh':
                self.memory.assign_space(dir, math.sinh(self.memory.search_space(op1)))
            elif opcode == 'cosh':
                self.memory.assign_space(dir, math.cosh(self.memory.search_space(op1)))
            elif opcode == 'tanh':
                self.memory.assign_space(dir, math.tanh(self.memory.search_space(op1)))
            elif opcode == 'log':
                self.memory.assign_space(dir, math.log(self.memory.search_space(op1)))
            elif opcode == 'abs':
                self.memory.assign_space(dir, abs(self.memory.search_space(op1)))
            elif opcode == 'floor':
                self.memory.assign_space(dir, math.floor(self.memory.search_space(op1)))
            elif opcode == 'ceil':
                self.memory.assign_space(dir, math.ceil(self.memory.search_space(op1)))
            elif opcode == 'pow':
                self.memory.assign_space(dir, math.pow(self.memory.search_space(op1), self.memory.search_space(op2)))
            elif opcode == 'min':
                self.memory.assign_space(dir, min(self.memory.search_space(op1), self.memory.search_space(op2)))
            elif opcode == 'max':
                self.memory.assign_space(dir, max(self.memory.search_space(op1), self.memory.search_space(op2)))
            # control de flujo
            elif opcode == 'GOTO':
                # print("goto: ", dir)
                self.pointer_stack[-1] = dir - 1
            elif opcode == 'GOTOF':
                if not self.memory.search_space(op1):
                    self.pointer_stack[-1] = dir - 1
            elif opcode == 'GOTOV':
                if self.memory.search_space(op1):
                    self.pointer_stack[-1] = dir - 1
            elif opcode == 'GOSUB':
                self.pointer_stack.append(dir - 1)
                self.memory.mem_stack()
            elif opcode == 'RETURN':
                self.memory.assign_space(dir, self.memory.search_space(op1))
            elif opcode == 'ENDFUNC':
                self.memory.mem_unstack()
                self.pointer_stack.pop()
                pass
            elif opcode == 'PARAM':
                self.memory.param(op1, dir)
                pass
            elif opcode == 'ERA':
                self.memory.era(self.counters[dir])
            elif opcode == 'ENDPROG':
                print("ENDPROG")
                pass
            elif opcode == 'INIT':
                self.memory.init('main', self.counters['main'])
                self.memory.init('global', self.counters['global'])
                self.memory.init('const', self.counters['const'])
                self.memory.init_const(self.constants)
                print("INIT")
            else:
                raise Exception("ERROR: opcode {} not found".format(opcode))
                # print("ERROR: opcode {} not found".format(opcode))
            self.pointer_stack[-1] += 1

    def imprimir_memoria(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.memory.global_mem.table)
        pp.pprint(self.memory.const_mem.table)
        

        print(str(len(self.memory.func_stack)) + " stack de memoria")
        for m in self.memory.func_stack:
            pp.pprint(m.table)