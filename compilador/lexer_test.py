'''
lexer_test.py
programa que prueba el funcionamiento de lexer.py
'''
import sys
import os
from lexer import lexer

# Se puede especificar un test case en particular como argumento
test_no = str(sys.argv[1]) if len(sys.argv) > 1 else None

print("---PROBANDO ANALIZADOR LEXICO---")

# Si se especifica un test case en particular, se prueba solo ese
if test_no:
    print("TEST no.", test_no)
    data = open('tests/lexer/' + 'test' + test_no + '.xcx', 'r').read()
    # print(data)
    lexer.input(data)
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        print(tok)
# Se itera sobre todos los test cases de la carpeta tests/lexer
else:
    # assign directory
    directory = 'tests/lexer'
    i = 0 # contador de test cases
    # abre el archivo que contendra los resultados
    wf = open("test_results/lexer/result.txt","w")
    listadearchivos = os.listdir(directory)
    listadearchivos.sort()
    for filename in listadearchivos:
        rf = os.path.join(directory, filename)
        i += 1
        toks = ""
        test_no = "TEST no." + str(i)
        # spacing
        if i != 1:
            wf.write( "\n")
        wf.write(test_no + "\n")
        print(test_no)
        # obtiene los tokens
        data = open(rf, 'r').read()
        lexer.input(data)
        # Tokenize
        while True:
            tok = lexer.token()
            if not tok: 
                break      # No more input
            print(tok)
            # agrega los tokens al archivo de resultados
            toks += str(tok) + "\n"
        wf.write(str(toks))
    wf.close()