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
    i = 0
    wf = open("test_results/lexer/result.txt","w")
    # iterate over files in that directory
    for filename in os.listdir(directory):
        rf = os.path.join(directory, filename)
        i += 1
        toks = ""
        test_no = "TEST no." + str(i)
        # spacing
        if i != 1:
            wf.write( "\n")
        wf.write(test_no + "\n")
        print(test_no)
        data = open(rf, 'r').read()
        lexer.input(data)
        # Tokenize
        while True:
            tok = lexer.token()
            if not tok: 
                break      # No more input
            print(tok)
            toks += str(tok) + "\n"
        wf.write(str(toks))
    wf.close()




# ###
# import sys
# from lexer import lexer

# no_tests = 2
# test_no = str(sys.argv[1]) if len(sys.argv) > 1 else None
# test_files = ['test' + str(i) + '.xcx' for i in range(1, no_tests + 1)]

# print("##### LEXER TESTS ####")

# if test_no:
#     print("TEST no.", test_no)
#     data = open('tests/lexer/' + 'test' + test_no + '.xcx', 'r').read()
#     lexer.input(data)
#     # Tokenize
#     while True:
#         tok = lexer.token()
#         if not tok: 
#             break      # No more input
#         print(tok)
# else:
#     # Give the lexer some input
#     f= open("test_results/lexer/result.txt","w")
#     for i, test in enumerate(test_files):
#         # print("\n")
#         f.write( "\n")
#         test_no = "TEST no." + str(i + 1)
#         toks = ""
#         # print(test_no)
#         f.write(test_no + "\n")
#         data = open('tests/lexer/' + test, 'r').read()        
#         lexer.input(data)
#         # toks += test_no + "\n"
#         # Tokenize
#         while True:
#             tok = lexer.token()
#             if not tok: 
#                 break      # No more input
#             # print(tok)
#             toks += str(tok) + "\n"
        
#         f.write(str(toks))
#     f.close()