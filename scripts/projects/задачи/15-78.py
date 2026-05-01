def generate_even_numbers(n):
    if n < 1:
        print("Введите натуральное число больше 0.")
        return

    even_numbers = []
    current_number = 2

    while len(even_numbers) < n:
        even_numbers.append(current_number)
        current_number += 2

    return even_numbers

# Ввод натурального числа n
n = int(input("Введите натуральное число n: "))

# Генерация и вывод первых n четных натуральных чисел
result = generate_even_numbers(n)
print(f"Первые {n} четных натуральных чисел: {result}")
