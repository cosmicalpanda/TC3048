'''
lexer_test.py
programa que prueba el funcionamiento de lexer.py
'''
import sys
from lexer import lexer

# especifica la cantidad de test cases que hay en la carpeta tests/lexer
no_tests = 1
# Se puede especificar un test case en particular como argumento
test_no = str(sys.argv[1]) if len(sys.argv) > 1 else None
test_files = ['test' + str(i) + '.xcx' for i in range(1, no_tests + 1)]

print("---PROBANDO ANALIZADOR LEXICO---")

if test_no:
    print("TEST no.", test_no)
    data = open('tests/' + 'test' + test_no + '.xcx', 'r').read()
    print(data)
    lexer.input(data)
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        print(tok)
else:
    for i, test in enumerate(test_files):
        print("TEST no.", i + 1)
        data = open('tests/lexer/' + test, 'r').read()
        lexer.input(data)
        # Tokenize
        while True:
            tok = lexer.token()
            if not tok: 
                break      # No more input
            print(tok)


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