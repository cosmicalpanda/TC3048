'''
parser_test.py
'''
from parser import parser
import sys
import os
# import json

# Se puede especificar un test case en particular como argumento
test_no = str(sys.argv[1]) if len(sys.argv) > 1 else None

print("---PROBANDO ANALIZADOR SINTACTICO---")

# Si se especifica un test case en particular, se prueba solo ese
if test_no:
    pass
    # try:
    #     s = open('compiler/tests/parser/' + 'test' +
    #              test_no + '.gmc', 'r').read()
    #     parser.parse(s, tracking=True)
    #     print('test no.', test_no, ': apropiado')
    # except Exception as e:
    #     error_msg = "test " + str(test_no) + " : " + str(e)
    #     # Save ovejota as error
    #     with open('ovejota.json', "w") as output_file:
    #         json.dump({'error': error_msg}, output_file, indent=2)
    #     raise e
else:
    # for i, test in enumerate(test_files):
    #     try:
    #         s = open('compiler/tests/parser/' + test, 'r').read()
    #         parser.parse(s, tracking=True)
    #         print('test no.', i + 1, ': apropiado')
    #     except Exception as e:
    #         print(e, "for test", i + 1)
    #     except EOFError:
    #         break

    # assign directory
    directory = 'tests/parser'
    i = 0 # contador de test cases
    # abre el archivo que contendra los resultados
    wf = open("test_results/parser/result.txt","w")
    listadearchivos = os.listdir(directory)
    listadearchivos.sort()

    for filename in listadearchivos:
        try:
            rf = os.path.join(directory, filename)
            i += 1
            test_no = "TEST no." + str(i)
            # spacing
            if i != 1:
                wf.write( "\n")
            wf.write(test_no + "\n")
            print(test_no)
            # obtien el el texto a parsear
            data = open(rf, 'r').read()

            res = parser.parse(data, tracking=True)
            wf.write("apropiado\n")

        except Exception as e:
            error_msg = str(e)
            wf.write("error: " + error_msg + "\n")
        
        except EOFError:
            break

    wf.close()
