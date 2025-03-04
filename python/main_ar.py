# 1. Приветствие.
# 2. Правила пользования.
# 3. Вывод список валют.
# 4. Выбор имеющийся валюты.
# 5. Количество этой валюты.
# 6. Выбор валюты конвертации
# 7. Вывод результата.


import requests


def get_online_currencies():
    host = "https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_xeO8zPpvTh25UirejoCiuzElEQOdMUhhPHMoIkc1"

    response = requests.get(host)

    return response.json().get("data")


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def is_currency_available(currency, currencies: dict):
    return currency in currencies.keys()



CURRENCIES = {
    "USD": 1,
    "EUR": 1.08,
    "GBP": 1.24,
    "RUB": 0.012
}

CURRENCIES = get_online_currencies()
#надо раскомментить CURRENCIES для подключения данных их API


# 1.
print("Добро пожаловать в конвертор валют!")

# 2.
print("""
Данная программа поможет вам конвертировать вашу валюту в желаемую.
- выбор исходной валюты;
- ввод количества этой валюты;
- выбор валюты конвертации.
""")

# 3.
count = 1
for key in CURRENCIES.keys():
    print(f'{count}. {key}')
    count += 1

print()
# 4.
current_currency = input("Введите валюту: ").strip().upper()
while not is_currency_available(current_currency, CURRENCIES):
    current_currency = input("Неправильно введена валюта.\nВведите валюту: ")

# 5.
current_amount = input("Введите имеющуюся сумму: ")
while not is_float(current_amount):
    current_amount = input("Неверные данные. Введите имеющуюся сумму: ")

# 6.
conversion_currency = input("Выберите валюту для конвертации: ").strip().upper()
while not is_currency_available(conversion_currency, CURRENCIES):
    conversion_currency = input("Неправильно введена валюта.\nВведите валюту: ")

# 7.
result = CURRENCIES[current_currency] / CURRENCIES[conversion_currency] * float(current_amount)
print(f"ИТОГО: {round(result, 2)}")

