a = [1, 3, 4, 5, 7]

for i in a:
    if i % 2 == 0:
        evens = True
    else:
        evens = False

if evens == True:
    print('в массиве есть чётные числа')
else:
    print('в массиве нет чётных чисел')