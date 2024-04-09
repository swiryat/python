a = [2, 17, 53, 8, 34, 63, 123, 85]  # Замените на свой массив

max_ending_with_3 = None  # Инициализируем переменную максимума

for value in a:
    if value % 10 == 3:
        if max_ending_with_3 is None or value > max_ending_with_3:
            max_ending_with_3 = value

if max_ending_with_3 is not None:
    print(f"Максимальный элемент, оканчивающийся на 3: {max_ending_with_3}")
else:
    print("Нет элементов, оканчивающихся на 3 в массиве.")
