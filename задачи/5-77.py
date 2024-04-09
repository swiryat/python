power = 10  # Начальная степень
while power >= 2:
    result = 2 ** power
    if result % 2 == 0:
        print(f"2^{power} = {result}")
    power -= 2  # Уменьшаем степень на 2
