# Введите три числа
num1 = float(input('Введите первое число: '))
num2 = float(input('Введите второе число: '))
num3 = float(input('Введите третье число: '))

# Находим максимальное и минимальное из трех чисел
maximum = num1
minimum = num1

if num2 > maximum:
    maximum = num2
elif num2 < minimum:
    minimum = num2

if num3 > maximum:
    maximum = num3
elif num3 < minimum:
    minimum = num3

print(f"Максимальное число: {maximum}")
print(f"Минимальное число: {minimum}")
