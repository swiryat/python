def evaluate_prefix_expression(expression):
    stack = []
    operators = set(['+', '-', '*', '/'])

    tokens = expression.split()

    for token in reversed(tokens):
        if token.isdigit() or (token[0] == '-' and token[1:].isdigit()):
            # Если токен - число (возможно, со знаком минус)
            stack.append(int(token))
        elif token in operators:
            # Если токен - оператор
            operand1 = stack.pop()
            operand2 = stack.pop()

            if token == '+':
                result = operand1 + operand2
            elif token == '-':
                result = operand1 - operand2
            elif token == '*':
                result = operand1 * operand2
            elif token == '/':
                result = operand1 / operand2  # Обратите внимание, что это деление Python 3

            stack.append(result)

    return stack.pop()

# Пример использования
prefix_expression = "- * + 4 5 3 2"
result = evaluate_prefix_expression(prefix_expression)
print(f"Результат выражения {prefix_expression} равен {result}")
