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
    print("Выберите систему счисления:")
    print("1. Двоичная")
    print("2. Восьмеричная")
    print("3. Шестнадцатеричная")
    choice = int(input("Ваш выбор: "))

    decimal_number = int(input("Введите число в десятичной системе: "))

    if choice == 1:
        binary_number = convert_to_base(decimal_number, 2)
        print("Число в двоичной системе:", binary_number)
    elif choice == 2:
        octal_number = convert_to_base(decimal_number, 8)
        print("Число в восьмеричной системе:", octal_number)
    elif choice == 3:
        hexadecimal_number = convert_to_base(decimal_number, 16)
        print("Число в шестнадцатеричной системе:", hexadecimal_number)
    else:
        print("Некорректный выбор.")

if __name__ == "__main__":
    main()
