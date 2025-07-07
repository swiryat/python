import random

from colorama import init
from colorama import Fore, Back, Style


init()



quotes = [
    "Успех — это способность идти от одного неудачного предприятия к другому, не теряя энтузиазма. - Уинстон Черчилль",
    "Не бойтесь делать то, что вам не нравится. Вероятно, вы это будете делать плохо. Но вам понравится процесс. - Уоррен Баффетт",
    "Когда работа вам нравится, вы никогда не будете работать ни одного дня в своей жизни. - Конфуций",
    "Не стоит засыпать со сном, ожидающим будильника. - Стив Джобс",
    "Мечты – это нечто, что приходит только так. Вам нужно много работать, чтобы они сбылись. - Шон Мендес"
]

def get_random_quote():
    return random.choice(quotes)

print(Back.RESET + Back.GREEN)

def get_quote_by_number(number):
    if number >= 1 and number <= len(quotes):
        return quotes[number - 1]
    else:
        return None

def add_quote(quote):
    quotes.append(quote)
    print("Цитата успешно добавлена!")

def save_quotes_to_file(filename):
    with open(filename, "w") as file:
        for quote in quotes:
            file.write(quote + "\n")
    print("Список цитат сохранен в файле:", filename)

while True:
    print("1. Получить случайную цитату")
    print("2. Получить цитату по номеру")
    print("3. Добавить новую цитату")
    print("4. Сохранить список цитат в файл")
    print("5. Выйти из программы")
    choice = int(input("Выберите вариант (1-5): "))

    if choice == 1:
        random_quote = get_random_quote()
        print("Случайная цитата:", random_quote)
    elif choice == 2:
        number = int(input("Введите номер цитаты: "))
        quote = get_quote_by_number(number)
        if quote:
            print("Цитата номер", number, ":", quote)
        else:
            print("Неверный номер цитаты!")
    elif choice == 3:
        new_quote = input("Введите новую цитату: ")
        add_quote(new_quote)
    elif choice == 4:
        filename = input("Введите имя файла для сохранения цитат: ")
        save_quotes_to_file(filename)
    elif choice == 5:
        print("Программа завершена.")
        break
    else:
        print("Неверный выбор!")

    input("Нажмите Enter для продолжения...")

