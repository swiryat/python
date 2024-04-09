import random

array_size = 25
a = [random.randint(100, 999) for _ in range(array_size)]

max_sum_digits = 0  # Инициализируем переменную максимальной суммы цифр
index_of_max_sum_digits = -1  # Инициализируем индекс элемента с максимальной суммой цифр

for i, value in enumerate(a):
    sum_digits = sum(int(digit) for digit in str(value))
    if sum_digits > max_sum_digits:
        max_sum_digits = sum_digits
        index_of_max_sum_digits = i

if index_of_max_sum_digits != -1:
    print(f"Элемент с наибольшей суммой цифр: {a[index_of_max_sum_digits]}, индекс: {index_of_max_sum_digits}")
else:
    print("Массив пуст.")