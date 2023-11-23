# Virtual Machine
from memory import Memory
import pprint


class VM:
    def __init__(self,quadruples, counters, constants):
        self.quadruples = quadruples
        self.pointer_stack = [0]
        self.counters = counters
        # self.func_dir = func_dir
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
                self.memory.assign_space(dir, self.memory.search_space(op1) + op2)
            elif opcode == 'VER':
                temp = self.memory.search_space(dir)
                if temp <=0 or temp > op2:
                    raise Exception("Error: indice {} fuera de rango: {} -> {}".format(temp, 0,op2))
            elif opcode == 'WRITE':
                print("write: ", self.memory.search_space(dir))
                # print(self.memory.search_space(dir))
            elif opcode == 'READ':
                temp = input()
                self.memory.assign_space(dir, temp)
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
                #TODO
                self.memory.mem_unstack()
                self.pointer_stack.pop()
                pass
            elif opcode == 'PARAM':
                # TODO
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
                # self.pointer_stack[-1] = dir - 1
            else:
                print("ERROR: opcode {} not found".format(opcode))
            self.pointer_stack[-1] += 1

    def imprimir_memoria(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.memory.global_mem.table)
        pp.pprint(self.memory.const_mem.table)
        

        print(str(len(self.memory.func_stack)) + " stack de memoria")
        for m in self.memory.func_stack:
            pp.pprint(m.table)