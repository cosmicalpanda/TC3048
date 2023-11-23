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
                self.memory.assign_space(dir, self.memory.search_space(op1) and self.memory.search_space(op2))
            elif opcode == '|':
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
                print("dir1: {} = dir2: {}".format(dir, op1))
                self.memory.assign_space(dir, self.memory.search_space(op1))
            
            # funciones

            elif opcode == 'ERA':
                self.memory.era(dir)
            elif opcode == 'ENDPROG':
                print("ENDPROG")
                pass
            elif opcode == 'GOTOMAIN':
                self.memory.init('main', self.counters['main'])
                self.memory.init('global', self.counters['global'])
                self.memory.init('const', self.counters['const'])
                self.memory.init_const(self.constants)
                print("GOTOMAIN")
                pass
            else:
                print("ERROR: opcode {} not found".format(opcode))
            self.pointer_stack[-1] += 1

    def imprimir_memoria(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.memory.global_mem.table)
        pp.pprint(self.memory.const_mem.table)
        

        print(str(len(self.memory.func_stack)) + " stack de memoria")
        for m in self.memory.func_stack:
            pp.pprint(m.stack)