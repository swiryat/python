from colorama import Fore, Back, Style
init()
print(back.GREEN)
what = input("Что делаем? (+, -): ")
print(fore.BLACK)
print(back.CYAN)
a = float(input("Введи первое число: "))
b = float(input("Введи второе число: "))
print(back.YELLOW)
if what == "+":
    c = a + b
    print("Результат: " + str(c))
elif what == "-":
    c = a - b
    print("Результат: " + str(c))
else:
    print("Выбрана неверная операция!")
input()