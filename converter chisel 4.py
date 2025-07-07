def convert_to_base(decimal_number, base):
    if decimal_number == 0:
        return '0'
    digits = "0123456789ABCDEF"
    result = ''
    while decimal_number > 0:
        remainder = decimal_number % base
        result = digits[remainder] + result
        decimal_number //= base
    return result

def main():
    print("Выберите систему счисления для ввода:")
    print("1. Двоичная")
    print("2. Восьмеричная")
    print("3. Шестнадцатеричная")
    input_choice = int(input("Ваш выбор: "))

    number_input = input("Введите число: ")

    if input_choice == 1:
        decimal_number = int(number_input, 2)
    elif input_choice == 2:
        decimal_number = int(number_input, 8)
    elif input_choice == 3:
        decimal_number = int(number_input, 16)
    else:
        print("Некорректный выбор.")
        return

    binary_number = convert_to_base(decimal_number, 2)
    octal_number = convert_to_base(decimal_number, 8)
    hexadecimal_number = convert_to_base(decimal_number, 16)

    print("Число в двоичной системе:", binary_number)
    print("Число в восьмеричной системе:", octal_number)
    print("Число в шестнадцатеричной системе:", hexadecimal_number)
    print("Число в десятичной системе:", decimal_number)

if __name__ == "__main__":
    main()
