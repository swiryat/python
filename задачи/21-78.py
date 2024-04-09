def sum_of_divisors(n):
    if n < 1:
        print("Введите натуральное число больше 0.")
        return

    divisor_sum = 0

    for i in range(1, n):
        if n % i == 0:
            divisor_sum += i

    return divisor_sum

# Ввод натурального числа n
n = int(input("Введите натуральное число n: "))

# Вычисление и вывод суммы делителей числа n, меньших самого числа
result = sum_of_divisors(n)
print(f"Сумма делителей числа {n}, меньших самого числа: {result}")
