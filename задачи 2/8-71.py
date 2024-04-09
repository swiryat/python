a = [2, 7, 1, 8, 4, 6, 3, 5]  # Замените на свой массив

min_even = float('inf')  # Инициализируем переменную минимума бесконечностью
min_even_index = -1  # Инициализируем переменную индекса минимального чётного элемента

for index, value in enumerate(a):
    if value % 2 == 0 and value < min_even:
        min_even = value
        min_even_index = index

if min_even_index != -1:
    print(f"Минимальный чётный элемент: {min_even}, его индекс: {min_even_index}")
else:
    print("Нет чётных элементов в массиве.")
