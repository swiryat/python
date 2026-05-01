product = 1

while True:
    number = int(input('Введите число (0 для завершения): '))
    
    if number == 0:
        break
    product *= number

print('Произведение чисел:', product)
