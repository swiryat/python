def find_max_element(matrix):
    max_value = float('-inf')
    max_row = -1
    max_col = -1

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > max_value:
                max_value = matrix[i][j]
                max_row = i
                max_col = j

    return max_value, max_row, max_col

# Пример использования
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

max_element, row, col = find_max_element(matrix)
print(f"Максимальный элемент: {max_element}")
print(f"Индексы максимального элемента: ({row}, {col})")
