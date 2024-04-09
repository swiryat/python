a = [2, -7, 1, 8, 4, 6, -3, 5]  # Замените на свой массив

min_positive = float('inf')  # Инициализируем переменную минимума бесконечностью

for value in a:
    if value > 0 and value < min_positive:
        min_positive = value

if min_positive != float('inf'):
    print(f"Минимальный положительный элемент: {min_positive}")
else:
    print("Нет положительных элементов в массиве.")
