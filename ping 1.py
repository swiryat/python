import subprocess

# Запрос адреса у пользователя
hostname = input("Введите адрес для пинга: ")

# Осуществляем пинг и захватываем вывод
try:
    result = subprocess.run(['ping', '-c', '4', hostname], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    output = result.stdout
    if "TTL=" in output:
        print(f"Адрес {hostname} доступен и отвечает на пинг.")
    else:
        print(f"Адрес {hostname} недоступен или не отвечает на пинг.")
except subprocess.CalledProcessError:
    print("Ошибка при выполнении команды ping.")
