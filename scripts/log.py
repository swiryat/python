import math

while True:
    print("Выберите тип логарифма:")
    print("1. Натуральный логарифм (ln)")
    print("2. Десятичный логарифм (log10)")
    print("3. Выход")
    
    choice = input("Введите номер выбора: ")
    
    if choice == '1':
        x = float(input("Введите число для вычисления натурального логарифма: "))
        result = math.log(x)
        print(f"Натуральный логарифм числа {x} равен {result}")
    elif choice == '2':
        x = float(input("Введите число для вычисления десятичного логарифма: "))
        result = math.log10(x)
        print(f"Десятичный логарифм числа {x} равен {result}")
    elif choice == '3':
        print("Выход из калькулятора.")
        break
    else:
        print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")
