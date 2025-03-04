def print_digits_in_column(number):
    # Преобразование числа в строку для удобства обработки цифр
    str_number = str(number)

    # Вывод цифр в столбик, начиная с последней
    for digit in reversed(str_number):
        print(digit)

# Пример использования
input_number = int(input("Введите число: "))
print_digits_in_column(input_number)
