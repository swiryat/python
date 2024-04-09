# Предположим, что у вас есть матрица matrix
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Вычисление суммы элементов главной диагонали
diagonal_sum = sum(matrix[i][i] for i in range(min(len(matrix), len(matrix[0]))))

# Вывод результата
print(f"Сумма элементов главной диагонали: {diagonal_sum}")
