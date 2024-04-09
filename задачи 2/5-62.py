a = [2, 7, 35, 8, 11]

for i in a:
    if i % 5 == 0 and i % 7 == 0:
        is_devisible = True
    else:
        is_devisible = False

if is_devisible == True:
    print('в массиве есть число, делящееся на 5 и 7')
else:
    print('нет')