def is_valid_expression(expression):
    stack = []
    opening_brackets = {'(': 1, '[': 1, '{': 1, '<': 1}
    closing_brackets = {')': '(', ']': '[', '}': '{', '>': '<'}

    for index, char in enumerate(expression, start=1):
        if char in opening_brackets:
            # Если встречена открывающая скобка, добавляем ее и ее номер в стек
            stack.append((char, index))
        elif char in closing_brackets:
            # Если встречена закрывающая скобка
            if not stack or stack.pop()[0] != closing_brackets[char]:
                return False, index  # Несоответствие скобок
        else:
            # Пропускаем символы, не являющиеся скобками

            if stack:
                return False, stack[-1][1]  # Несбалансированные открывающие скобки

    return True, None  # Выражение правильное

# Пример использования
expression = "([]{<})"  # Замените на ваше выражение
result, error_index = is_valid_expression(expression)

if result:
    print(f"Выражение {expression} правильное.")
else:
    print(f"Выражение {expression} неправильное. Ошибка на символе {error_index}.")
