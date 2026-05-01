
# Задание 1: Нахождение площади круга.

import math

# Определение функции для нахождения площади круга.
def calculate_circle_area(radius):
    area = math.pi * radius**2
    return area

# Вызов функции и вывод результата.
radius = 1
circle_area = calculate_circle_area(radius)
print(f"Площадь круга радиуса {radius} равна {circle_area:.2f} кв.ед.")

# Задание 2: Нахождение суммы n элементов списка.

# Определение функции для нахождения суммы n элементов списка.
def calculate_sum(lst, n=None):
    if n is None:
        result = sum(lst)
    else:
        result = sum(lst[:n])
    return result

# Пример использования функции.
list_example = list(range(-10, 10))
n = 2
result1 = calculate_sum(list_example, n)
print(f"Сумма первых {n} элементов списка равна {result1}.")

result2 = calculate_sum(list_example)
print(f"Сумма всех элементов списка равна {result2}.")

# Задание 3: Нахождение выборочного среднего, медианы и моды.

# Определение функции для вычисления выборочных статистик.
def calculate_statistics(values):
    if len(values) == 0:
        return None, None, None

    mean_value = sum(values) / len(values)

    sorted_values = sorted(values)
    n = len(sorted_values)
    if n % 2 == 1:
        median_value = sorted_values[n // 2]
    else:
        median_value = (sorted_values[(n // 2) - 1] + sorted_values[n // 2]) / 2

    counts = {}
    for value in values:
        if value in counts:
            counts[value] += 1
        else:
            counts[value] = 1
    max_count = max(counts.values())
    mode_values = [value for value, count in counts.items() if count == max_count]

    return mean_value, median_value, mode_values

# Пример использования функции.
value = [12, 13, 2, 4, 13, 5, 6, 7, 8, 8, 8, 8, 8, 10]
mean_result, median_result, mode_result = calculate_statistics(value)

print(f"Выборочное среднее равно {mean_result}.")
print(f"Медиана равна {median_result}.")
print(f"Мода равна {mode_result}.")

# №4
# Определение функции для рассчета общего дохода.
def income(*args):
    total_income = sum(args)
    return total_income

# Вызов функции для расчета общего дохода с использованием кортежа или списка.
income_result1 = income(100)
print(f"Общий доход равен {income_result1}.")

income_result2 = income(100, 10)
print(f"Общий доход равен {income_result2}.")

# Вызов функции для расчета общего дохода с использованием словаря.
income_result3 = income(*[100])
print(f"Общий доход равен {income_result3}.")

income_result4 = income(*[100, 10])
print(f"Общий доход равен {income_result4}.")
