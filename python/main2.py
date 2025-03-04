# 1. Приветствие.
# 2. Правила пользования.
# 3. Вывод список валют.
# 4. Выбор имеющийся валюты.
# 5. Количество этой валюты.
# 6. Выбор валюты конвертации
# 7. Вывод результата.

CURRENCIES = {
    "USD": 1,
    "EUR": 1.08,
    "GBP": 1.24,
    "RUB": 0.012
}

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
current_currency = input("Введите имеющийся валюту: ")

# 5.
current_amount = int(input("Введите имеющуюся сумму: "))

# 6.
conversion_currency = input("Выберите валюту для конвертации: ")

# 7.
result = CURRENCIES[current_currency] / CURRENCIES[conversion_currency] * current_amount
print(f"ИТОГО: {round(result, 2)}")