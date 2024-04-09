def count_numbers(sequence):
    count = 0
    for num in sequence:
        if num % 10 == 1 and num % 3 == 0:
            count += 1
    return count

# Ввод количества чисел в последовательности
n = int(input("Введите количество чисел в последовательности: "))

# Ввод самой последовательности чисел
sequence = []
for _ in range(n):
    number = int(input("Введите число: "))
    sequence.append(number)

# Определение количества чисел, оканчивающихся на 1 и делящихся на 3
result = count_numbers(sequence)
print(f"Количество чисел, оканчивающихся на 1 и делящихся на 3: {result}")
