'''
a_test_suite.py

Este archivo se encarga de correr todos los test cases en la carpeta test_suite, o un archivo en especifio
'''
from a_parser import parser, cuad, counters, constants
import sys
import os
import json
from virtual_machine import VM
from prettytable import PrettyTable

# Se puede especificar un test case en particular como argumento
print(sys.argv)
test_no = str(sys.argv[1]) if len(sys.argv) > 1 else None


print("---PROBANDO---")


# Si se especifica un test case en particular, se prueba solo ese
if test_no:
    pass
    try:
        print("---PARSING---")
        data = open('test_suite/' + 'test' + test_no + '.xcx', 'r').read()
        parser.parse(data, tracking=True)
        # print(constants)
        tabla_cuadruplos = PrettyTable(['#', 'operator', 'op1', 'op2', 'res'])
        for c in range(len(cuad)):
            tabla_cuadruplos.add_row([c] + cuad[c])
        print(tabla_cuadruplos)
        maquina = VM(cuad,counters, constants)
        print("-----RUNNING-----")
        maquina.run()
        maquina.imprimir_memoria()
        print("-----FINISHED-----")
        print('test no.', test_no, ': apropiado')
    except Exception as e:
        error_msg = "test " + str(test_no) + " : " + str(e)
        # Save obj as error
        with open('obj.json', "w") as output_file:
            json.dump({'error': error_msg}, output_file, indent=2)
        raise e
else:
    # assign directory
    directory = 'test_suite/'
    i = 0 # contador de test cases
    # abre el archivo que contendra los resultados
    wf = open("test_results/ts/result.txt","w")
    listadearchivos = os.listdir(directory)
    listadearchivos.sort()

    for filename in listadearchivos:
        try:
            rf = os.path.join(directory, filename)
            i += 1
            test_no = "TEST: " + str(filename)
            # spacing
            if i != 1:
                wf.write( "\n")
            wf.write(test_no + "\n")
            print(test_no)
            # obtien el el texto a parsear
            data = open(rf, 'r').read()
            # proceso
            parser.parse(data, tracking=True)
            # print(func_dir)
            # print(fd)
            # print(constants)
            tabla_cuadruplos = PrettyTable(['#', 'operator', 'op1', 'op2', 'res'])
            for c in range(len(cuad)):
                tabla_cuadruplos.add_row([c] + cuad[c])
            print(tabla_cuadruplos)
            maquina = VM(cuad,counters, constants)
            print("-----RUNNING-----")
            maquina.run()
            maquina.imprimir_memoria()
            print("-----FINISHED-----")
            wf.write("apropiado\n")

        except Exception as e:
            error_msg = str(e)
            wf.write("error: " + error_msg + "\n")
        
        except EOFError:
            break

    wf.close()
