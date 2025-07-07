def convert_to_base(number, base):
    if number == 0:
        return '0'
    digits = "0123456789ABCDEF"
    result = ''
    while number > 0:
        remainder = number % base
        result = digits[remainder] + result
        number //= base
    return result

def main():
    decimal_number = int(input("Введите число в десятичной системе: "))

    binary_number = convert_to_base(decimal_number, 2)
    octal_number = convert_to_base(decimal_number, 8)
    hexadecimal_number = convert_to_base(decimal_number, 16)

    print("Число в двоичной системе:", binary_number)
    print("Число в восьмеричной системе:", octal_number)
    print("Число в шестнадцатеричной системе:", hexadecimal_number)

if __name__ == "__main__":
    main()
