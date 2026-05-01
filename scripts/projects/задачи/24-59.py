a = float(input('a: '))
b = float(input('b: '))

if a != 0:
    x = b / a
    print(f'x = {x}')
else:
    if b == 0:
        print('любое значение x')
    else:
        print('нет решений')
