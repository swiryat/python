def count_numbers(sequence):
    count = 0
    for num in sequence:
        if 10 <= num <= 99 and num % 10 == 3 and num % 7 == 0:
            count += 1
    return count

# Ввод количества чисел в последовательности
n = int(input("Введите количество чисел в последовательности: "))

# Ввод самой последовательности чисел
sequence = []
for _ in range(n):
    number = int(input("Введите число: "))
    sequence.append(number)

# Определение количества двузначных чисел, оканчивающихся на 3 и делящихся на 7
result = count_numbers(sequence)
print(f"Количество двузначных чисел, оканчивающихся на 3 и делящихся на 7: {result}")
