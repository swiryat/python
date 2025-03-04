# 1. Приветствие
# 2. Правила пользования
# 3. Вывод списка валют
# 4. Выбор имеющейся валюты
# 5. Количество этой валюты
# 6. Выбор валюты для конвертации
# 7. Вывод результата

import requests

def get_online_currencies():
    host = "https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_5EOppvQamDo61mkUbx7INGKHpwV6w9XkE9rf6UwQ&currencies=EUR%2CUSD%2CRUB%2CGBP"

    response = requests.get(host)

    return response.json().get("data")

currencies = get_online_currencies()



# 1.
print("Добро пожаловать в конвертор валют!")

# 2.
print("""
Данная программа поможет Вам конвертировать вашу валюту в желаемую.
- выбор исходной валюты;
- ввод количества этой валюты;
- выбор валюты конвертации.
""")

# 3.
count = 1
for key in currencies.keys():
    print(f"{count}. {key}")
    count += 1

# 4.

def input_current_currency():
    current_currency = input("Выберите валюту для конвертации: ").upper().strip()
    if current_currency in currencies:
        return current_currency
    else:
        print("Данная валюта отсутствует, введите корректную валюту")
        input_current_currency()
current_currency_result = input_current_currency()


    

# 5.
while True:
    try:
        current_amount = float(input('Введите сумму в формате "100.00": '))
        break
    except ValueError:
        print('Неверный формат ввода')
        
# 6.

def input_conversion_currency():
    conversion_currency = input("Выберите валюту для конвертации: ").upper().strip()
    if conversion_currency in currencies:
        return conversion_currency
    else:
        print("Данная валюта отсутствует, введите корректную валюту")
        input_conversion_currency()
conversion_currency_result = input_conversion_currency()


# 7.
result = currencies[current_currency_result] / currencies[conversion_currency_result] * current_amount
print(f"ИТОГО: {round(result, 2)}")