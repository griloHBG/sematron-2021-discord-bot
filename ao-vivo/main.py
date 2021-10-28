from my_package import print_with_type as printwt

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f"REIA, *{name:/>10}*")  # Press Ctrl+F8 to toggle the breakpoint.
    for number in range(10):
        print(number, end="")
    print()
    print([number for number in range(10)])
    print(list(range(1000)))
    i = 0
    f = 1.7
    t = (1,)
    #t[0] = 10
    d = {"python":"uma das linguagens de programação mais populares do mundo"}
    l = ['juvenal', 10, (0,1,2,3,4,5)]
    print(type(i), i)
    print(type(f), f)
    print(type(t), t)
    print(type(d), d)
    print(type(l), l)

    print('-'*30)
    for var in [i, f, t, d, l]:
        printwt(var)
    print('-'*30)

    print(d["python"])

    dd = {0:1, 878:3, 1005:4, 10:2}
    for key in dd.keys():
        print(f'o número {key} tem {dd[key]} caracteres')

    for value in dd.values():
        print(f'oia só {value} caracteres')

    for dict_tuple in dd.items():
        print(f'o número {dict_tuple[0]} tem {dict_tuple[1]} caracteres')

    for k, v in dd.items():
        print(f'o número {k} tem {v} {"caracter" if v == 1 else "caracteres"}')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
