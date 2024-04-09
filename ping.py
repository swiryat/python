import os

# Запрос адреса у пользователя
hostname = input("Введите адрес для пинга: ")

# Осуществляем пинг
response = os.system(f"ping {hostname}")

# Анализ результата
if response == 0:
    print(f"Адрес {hostname} доступен и отвечает на пинг.")
else:
    print(f"Адрес {hostname} недоступен или не отвечает на пинг.")
