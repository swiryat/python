summa = 0

while True:
    num = int(input('введите число (0 для завершения): '))

    if num == 0:
        break

    if num > 0:
        summa += num

print(summa)
