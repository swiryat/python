def multiply(x, y):
    # Инициализируем результат как 0
    result = 0
    
    # Определяем знак результата
    sign = 1
    if (x < 0) != (y < 0):
        sign = -1
    
    # Приводим оба числа к положительному виду
    x, y = abs(x), abs(y)
    
    # Складываем x с собой y раз
    for _ in range(y):
        result += x
    
    # Применяем знак
    result *= sign
    
    return result

# Ввод двух чисел
num1 = int(input("Введите первое число: "))
num2 = int(input("Введите второе число: "))

# Вычисление произведения
result = multiply(num1, num2)

# Вывод результата
print(f"Произведение чисел: {result}")
