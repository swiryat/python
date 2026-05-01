i = 10  # Задайте желаемое конечное значение
bunny_counter = ''

for num in range(i):
    bunny_counter = bunny_counter + str(num) + ', '

print(bunny_counter + 'вышел зайчик погулять!')




i = 10  # Задайте желаемое конечное значение
bunny_counter = ', '.join(map(str, range(i)))

print(bunny_counter + ' вышел зайчик погулять!')
i = 10  # Задайте желаемое конечное значение
bunny_counter = ', '.join(map(str, range(i)))

print(bunny_counter + ' вышел зайчик погулять!')


# Запросить пользователя ввести число
user_input = input("Введите желаемое конечное значение: ")

# Преобразовать введенное значение в целое число
try:
    i = int(user_input)
except ValueError:
    print("Ошибка: Введите целое число.")
    exit()

# Создать строку с числами от 0 до введенного значения
bunny_counter = ', '.join(map(str, range(i)))

# Вывести результат
print(bunny_counter + ' вышел зайчик погулять!')


