# ТЗ
# Валютный курс берется из API.
# Валюта: отсечение неправильного ввода валюты - при вводе недопустимых значений программа останавливается,
#          введение как буквенных обозначений (в любых регистрах) так и цифрами 1 - 4 (1 - это EUR  и т.д.).
# Кол-во валюты: ошибочно введенный знак "минус" игнорируется, доступно введение дробных чисел,
#                ошибочное введение НЕ цифр блокируется.
#  отредактирован ИТОГО

import requests
import sys

def get_online_currencies():
    host = ('https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_lHWdJ9F57DqM4p6cfXASt9rUX59hQX9'
            'VKPfA8Omf&currencies=EUR%2CUSD%2CGBP%2CRUB')
    response = requests.get(host)

    return response.json().get("data")

currency = get_online_currencies()

# Создание словарей, где валюты нумеруются как в цикле ниже (то есть, начиная с "1")
currency_values = list(currency.values())
nr = (1, 2, 3, 4)
currency_nr_val = dict(zip(nr, currency_values))

currency_keys = list(currency.keys())
nr = (1, 2, 3, 4)
currency_nr_key = dict(zip(nr, currency_keys))

print('Добро пожаловать в конвертор основных валют!')

print('''Данная программа поможет Вам конвертировать Вашу валюту в желаемую.

АЛГОРИТМ КОНВЕРТАЦИИ:
- выбор исходной валюты;
- ввод количества исходной валюты;
- выбор валюты конвертации.
''')

# вывод допустимых валют на экран с их номерами-кодами и прайсами.
count = 0
for a, b in currency.items():
    count += 1
    print(f'{count}. {a} = {round(float(b), 2)} за 1.0 USD')
print()

# список допустимых вариантов вызова валют
allowed_curr = ["EUR", "GBP", "RUB", "USD", "1", "2", "3", "4"]

# Допустимо введение как буквенных обозначений (в любых регистрах) так и цифрами 1 - 4 (1 - это EUR  и т.д.).
# Отсечение неправильного ввода валюты: при вводе недопустимых значений программа останавливается,
converted_currency = (input('Введите имеющуюся у Вас валюту (например, EUR) или ее номер из списка) '
                            '(например, 1): ')).upper()
if converted_currency not in allowed_curr:
    print('Неправильно ведена валюта! Вводите "EUR", "GBP", "RUB", "USD" или цифры 1 - 4')
    sys.exit()

# ошибочно введенный знак "минус" игнорируется, доступно введение дробных чисел, ошибочное введение НЕ цифр блокируется.
converted_currency_amount_input = input('Введите имеющуюся сумму: ')

if ',' in converted_currency_amount_input or converted_currency_amount_input.isalpha():
    print("Вы ввели запятую вместо точки или буквы вместо цифр")
    sys.exit()

converted_currency_amount = abs(float(converted_currency_amount_input))

converting_currency = (input('Выберите валюту для конвертации или ее номер из списка выше: ')).upper()
if converting_currency not in allowed_curr:
    print('Неправильно ведена валюта! Вводите "EUR", "GBP", "RUB", "USD" или цифры 1 - 4')
    sys.exit()

if converted_currency.isalpha() and converting_currency.isalpha():
    result = converted_currency_amount * currency[converting_currency] / currency[converted_currency]
    converting_currency_3letter = converting_currency
    converted_currency_3letter = converted_currency

elif converted_currency.isalpha() and converting_currency.isdigit():
    result = converted_currency_amount * currency_nr_val[int(converting_currency)] / currency[converted_currency]
    converting_currency_3letter =  currency_nr_key[int(converting_currency)]
    converted_currency_3letter = converted_currency

elif converted_currency.isdigit() and converting_currency.isalpha():
    result = converted_currency_amount * currency[converting_currency] / currency_nr_val[int(converted_currency)]
    converted_currency_3letter = currency_nr_key[int(converted_currency)]
    converting_currency_3letter = converting_currency

else:
    result = converted_currency_amount * currency_nr_val[int(converting_currency)] / currency_nr_val[int(converted_currency)]
    converting_currency_3letter = currency_nr_key[int(converting_currency)]
    converted_currency_3letter = currency_nr_key[int(converted_currency)]

print(f'ИТОГО: Вы покупаете {round(result, 2)} {converting_currency_3letter} за {converted_currency_amount_input} {converted_currency_3letter}')

