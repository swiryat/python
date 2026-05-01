def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True

# Ввод числа с клавиатуры
num = int(input("Введите число: "))

# Проверка, является ли число простым
if is_prime(num):
    print(f"{num} - простое число")
else:
    print(f"{num} - не простое число")
