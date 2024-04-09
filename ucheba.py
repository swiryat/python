import math
import re

# Задача 1: Выполнение математических операций
input_str = input("Введите два целых числа через пробел: ")
a, b = map(int, input_str.split())

sum_result = a + b
difference_result = a - b
product_result = a * b
division_result = a / b
remainder_result = a % b
logarithm_result = math.log10(a)
exponentiation_result = a ** b
square_root_result = math.sqrt(a)
e_times_b_result = math.e * b

print("Сумма a и b:", sum_result)
print("Разность a и b:", difference_result)
print("Произведение a и b:", product_result)
print("Частное от деления a на b:", division_result)
print("Остаток от деления a на b:", remainder_result)
print("Десятичный логарифм числа a:", logarithm_result)
print("Результат возведения числа a в степень b:", exponentiation_result)
print("Квадратный корень из числа a:", square_root_result)
print("Результат умножения числа e на b:", e_times_b_result)

# Задача 2: Создание списка чисел с шагом 3
number_list = list(range(1, 20, 3))

print("Длина списка:", len(number_list))
print("Элементы списка, начиная со второй позиции:", number_list[1:])
print("Четные элементы списка:", [num for num in number_list if num % 2 == 0])
divisible_by_5 = [num for num in number_list if num % 5 == 0]
if divisible_by_5:
    print("Элементы списка, делящиеся на 5 без остатка:", divisible_by_5)
else:
    print("Элементов, делящихся на 5, нет")
sorted_list = sorted(number_list, reverse=True)
print("Список, отсортированный в порядке убывания:", sorted_list)
squared_list = list(map(lambda x: x ** 2, number_list))
print("Квадраты элементов исходного списка:", squared_list)
reversed_list = number_list[::-1]
print("Элементы списка в обратном порядке:", reversed_list)
average = sum(number_list) / len(number_list)
print("Выборочное среднее элементов списка:", average)

# Задача 3: Создание структуры для данных о температуре
temperature_data = {
    "понедельник": 12.0,
    "вторник": 12.0,
    "среда": 17.0,
    "четверг": 17.0,
    "пятница": 14.3,
    "суббота": 11.9,
    "воскресенье": 12.0,
}

# Задача 4: Вычисление температуры по Фаренгейту
def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

celsius_to_fahrenheit_data = {day: (temp, celsius_to_fahrenheit(temp)) for day, temp in temperature_data.items()}

print("Температуры по Цельсию и Фаренгейту для каждого дня:")
for day, (celsius, fahrenheit) in celsius_to_fahrenheit_data.items():
    print(f"{day}: {celsius}°C, {fahrenheit}°F")

# Задача 5: Определение максимальной и минимальной температуры
max_temp_day = max(temperature_data, key=temperature_data.get)
min_temp_day = min(temperature_data, key=temperature_data.get)

print("День с максимальной температурой:", max_temp_day)
print("День с минимальной температурой:", min_temp_day)

# Задача 6: Анализ текста
text = """
Взвейтесь кострами, синие ночи!
Мы пионеры - дети рабочих
Близится время светлых годов
Клич пионера: "Всегда будь готов!"
Радостным шагом с песней веселой
Мы выступаем за комсомолом
Близится время светлых годов
Клич пионера: "Всегда будь готов!"
Мы поднимаем красное знамя
Дети рабочих, смело за нами!
Близится время светлых годов
Клич пионера: "Всегда будь готов!"
Взвейтесь кострами, синие ночи!
Мы пионеры - дети рабочих
Близится время светлых годов
Клич пионера: "Всегда будь готов!"
Клич пионера: "Всегда будь готов!"
"""

text = text.lower()
lines = text.strip().split('\n')
num_lines = len(lines)

sentences = [s.strip() for s in re.split(r'[.!?]', text) if s.strip()]
num_sentences = len(sentences)

words = re.findall(r'\b\w+\b', text)
unique_words = set(words)
num_unique_words = len(unique_words)

word_frequency = {}
for word in words:
    word_frequency[word] = word_frequency.get(word, 0) + 1

letters = re.findall(r'\b\w\b', text)
unique_letters = set(letters)
num_unique_letters = len(unique_letters)

print("Количество строк в тексте:", num_lines)
print("Количество предложений в тексте:", num_sentences)
print("Количество уникальных слов в тексте:", num_unique_words)
print("Частотная таблица слов:")
for word, frequency in word_frequency.items():
    print(f"{word}: {frequency} раз(а)")
print("Количество уникальных букв в тексте:", num_unique_letters)

