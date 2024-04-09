def evaluate_expression(expression):
    # Инициализируем результат значением первого числа в выражении
    result = 0
    # Инициализируем текущий оператор значением "+" (если первое число положительное)
    current_operator = "+"
    # Инициализируем текущее число значением "0"
    current_number = 0

    # Проходим по каждому символу в выражении
    for char in expression:
        if char.isdigit():
            # Если символ - цифра, добавляем его к текущему числу
            current_number = current_number * 10 + int(char)
        elif char in "+-":
            # Если символ - оператор, обновляем результат в соответствии с предыдущим оператором и текущим числом
            if current_operator == "+":
                result += current_number
            elif current_operator == "-":
                result -= current_number

            # Обновляем текущий оператор и сбрасываем текущее число
            current_operator = char
            current_number = 0

    # Обновляем результат в соответствии с последним оператором и последним числом
    if current_operator == "+":
        result += current_number
    elif current_operator == "-":
        result -= current_number

    return result

# Получаем ввод от пользователя
expression = input("Введите арифметическое выражение: ")

# Вычисляем и выводим результат
result = evaluate_expression(expression)
print("Результат выражения:", result)
