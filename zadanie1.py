import math

# Запрос ввода двух целых чисел через пробел
input_str = input("Введите два целых числа через пробел: ")
a, b = map(int, input_str.split())

# Выполнение математических операций
sum_result = a + b
difference_result = a - b
product_result = a * b
division_result = a / b
remainder_result = a % b
logarithm_result = math.log10(a)
exponentiation_result = a ** b
square_root_result = math.sqrt(a)
e_times_b_result = math.e * b

# Вывод результатов на экран
print("Сумма a и b:", sum_result)
print("Разность a и b:", difference_result)
print("Произведение a и b:", product_result)
print("Частное от деления a на b:", division_result)
print("Остаток от деления a на b:", remainder_result)
print("Десятичный логарифм числа a:", logarithm_result)
print("Результат возведения числа a в степень b:", exponentiation_result)
print("Квадратный корень из числа a:", square_root_result)
print("Результат умножения числа e на b:", e_times_b_result)
