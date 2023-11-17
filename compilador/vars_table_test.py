from vars_table import VarsTable

def test_vars_table_global():
    print("Probando global\n")
    vt = VarsTable('global')
    vt.add_var('int', 'a')
    vt.add_var('float', 'b')
    print(vt.table, "\n")
    vt.add_var('int', 'a')

def test_vars_table_local():
    print("Probando local\n")
    vt = VarsTable('local')
    vt.add_var('int', 'a')
    vt.add_var('float', 'b')
    vt.add_var('int')
    for i in range(0, 10):
        vt.add_var('int')
    for v in vt.table.items():
        print(v)
        print("\n")
    vt.add_var('int', 'a')

def test_vars_table_const():
    print("Probando const\n")
    vt = VarsTable('const')
    vt.add_const('int',  100)
    vt.add_const('float', 200)
    vt.add_const('float', 200)
    # for i in range(0, 10):
    #     vt.add_const('int', i)
    # vt.add_const('int', 'a')
    print(vt.table, "\n")

def main():
    try:
        test_vars_table_global()
    except Exception as e:
        print(e)

    print("\n")
    try:
        test_vars_table_local()
    except Exception as e:
        print(e)
    
    print("\n")
    try:
        test_vars_table_const()
    except Exception as e:
        print(e)
    

if __name__ == "__main__":
    main()