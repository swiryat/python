t = 5
while t == 5:
    from colorama import init
    from colorama import Fore, Back, Style
    init()
    print(Back.GREEN)
    what = input("Что делаем? (+, -): ")
    print(Fore.BLACK)
    print(Back.CYAN)
    a = float(input("Введи первое число: "))
    b = float(input("Введи второе число: "))
    print(Back.YELLOW)
    if what == "+":
        c = a + b
        print("Результат: " + str(c))
    elif what == "-":
        c = a - b
        print("Результат: " + str(c))
    else:
        print("Выбрана неверная операция!")  