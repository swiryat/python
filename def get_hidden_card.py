def get_hidden_card(card_number, stars_count=4):
    visible_digits_line = card_number[-4:]
    stars_string = '*' * stars_count
    hidden_card_number = f"{stars_string}{visible_digits_line}"
    return hidden_card_number

# Запрашиваем у пользователя номер карты
while True:
    card_number_input = input("Введите номер кредитной карты (16 цифр): ")
    if len(card_number_input) == 16 and card_number_input.isdigit():
        break
    print("Номер карты должен состоять из 16 цифр. Пожалуйста, повторите ввод.")

# Запрашиваем у пользователя количество звездочек
stars_count_input = int(input("Введите количество звездочек для скрытия (по умолчанию 4): ") or 4)

# Получаем скрытую версию номера карты с помощью функции
hidden_card = get_hidden_card(card_number_input, stars_count_input)

# Выводим скрытую версию номера карты
print("Скрытая версия номера карты:", hidden_card)

