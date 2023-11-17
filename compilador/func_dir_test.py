from func_dir import FuncDir

def test_add_func():
    print("Probando add_func\n")
    fd = FuncDir()
    fd.add_func('func1', 'int')
    fd.add_func('func2', 'float')
    fd.add_func('func3', 'void')
    print(fd.dir, "\n")
    fd.add_func('func1', 'int')

def test_add_varstable():
    print("Probando add_varstable\n")
    fd = FuncDir()
    fd.add_func('func1', 'int')
    fd.add_varstable('func1', 'local')
    fd.add_varstable('func1', 'temp')
    fd.add_varstable('func1', 'const')
    print(fd.dir, "\n")
    fd.add_varstable('func2', 'local')

def test_add_var():
    print("Probando add_var\n")
    fd = FuncDir()
    fd.add_func('func1', 'int')
    fd.add_varstable('func1', 'local')
    fd.add_var('func1', 'int', 'a')
    fd.add_var('func1', 'float', 'b')
    fd.add_var('func1', 'int')
    for i in range(0, 10):
        fd.add_var('func1', 'int')
    print(fd.dir, "\n")
    print(fd.dir['func1'][1].table, "\n")
    fd.add_var('func2', 'int', 'a')

def test_add_const():
    print("Probando add_const\n")
    fd = FuncDir()
    fd.add_const('int',  100)
    fd.add_const('float', 200)
    fd.add_const('float', 200)
    # for i in range(0, 10):
    #     fd.add_const('int', i)
    print(fd.dir, "\n")
    print(fd.dir['const'][1].table, "\n")
    # fd.add_const('int', 100)

def test_add_param():
    print("Probando add_param\n")
    fd = FuncDir()
    fd.add_func('func1', 'int')
    fd.add_varstable('func1', 'local')
    fd.add_param('func1', 'int', 'a')
    fd.add_param('func1', 'float', 'b')
    # fd.add_param('func1', 'int')
    print(fd.dir, "\n")
    print(fd.dir['func1'][1].table, "\n")
    fd.add_param('func2', 'int', 'a')

def test_has_varstable():
    print("Probando has_varstable\n")
    fd = FuncDir()
    fd.add_func('func1', 'int')
    fd.add_func('func2', 'int')
    fd.add_varstable('func1', 'local')
    print(fd.has_varstable('func1'))
    print(fd.has_varstable('func2'))
    print(fd.has_varstable('func3'))

def test_search_var():
    print("Probando search_var\n")
    fd = FuncDir()
    fd.add_func('global', 'void')
    fd.add_varstable('global', 'global')
    fd.add_func('func1', 'int')
    fd.add_varstable('func1', 'local')
    fd.add_var('func1', 'int', 'a')
    fd.add_var('func1', 'int', 'b')
    fd.add_var('global', 'int', 'b')
    fd.add_var('global', 'int', 'c')

    print(fd.search_var('func1', 'a'))
    print(fd.search_var('func1', 'b'))
    print(fd.search_var('func1', 'c'))
    print(fd.search_var('func1', 'd'))

def main():
    try:
        test_add_func()
    except Exception as e:
        print(e)
    print("\n")

    try:
        test_add_varstable()
    except Exception as e:
        print(e)
    print("\n")

    try:
        test_add_var()
    except Exception as e:
        print(e)
    print("\n")

    try:
        test_add_const()
    except Exception as e:
        print(e)
    print("\n")

    try:
        test_add_param()
    except Exception as e:
        print(e)
    print("\n")

    try:
        test_has_varstable()
    except Exception as e:
        print(e)
    print("\n")

    try:
        test_search_var()
    except Exception as e:
        print(e)
    print("\n")


if __name__ == "__main__":
    main()