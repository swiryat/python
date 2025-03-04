def average_diagonal_and_below(matrix):
    size = len(matrix)
    total_sum = 0
    count = 0

    for i in range(size):
        for j in range(i, size):
            total_sum += matrix[i][j]
            count += 1

    if count > 0:
        average = total_sum / count
        return average
    else:
        return 0

# Пример использования
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

result = average_diagonal_and_below(matrix)
print(f"Среднее арифметическое элементов в главной диагонали и под ней: {result}")
