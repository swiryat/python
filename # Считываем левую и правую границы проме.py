# Считываем левую и правую границы промежутка
left_boundary = int(input())
right_boundary = int(input())

# Считываем числа до тех пор, пока не встретим пустую строку
numbers = []
while True:
    try:
        num_str = input()
        if not num_str:
            break
        numbers.append(int(num_str))
    except EOFError:
        break

# Проверяем, входят ли все введенные числа в промежуток
all_in_range = all(left_boundary <= num <= right_boundary for num in numbers)

# Выводим результат
print(all_in_range)
