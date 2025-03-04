def count_nonzero_elements(matrix):
    size = len(matrix)
    count = 0

    for i in range(size):
        if matrix[i][size - 1 - i] != 0:
            count += 1

    return count

# Пример использования
matrix = [
    [1, 2, 0, 0],
    [1, 2, 0, 0],
    [0, 0, 3, 0],
    [8, 0, 0, 4]
]

result = count_nonzero_elements(matrix)
print(f"Количество ненулевых элементов побочной диагонали: {result}")
