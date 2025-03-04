import subprocess

def ping_host(hostname):
    try:
        result = subprocess.run(['ping', '-c', '4', hostname], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        output = result.stdout
        return "TTL=" in output
    except subprocess.CalledProcessError:
        return False

while True:
    # Запрос адреса у пользователя
    hostname = input("Введите адрес для пинга: ")

    # Осуществляем пинг
    is_reachable = ping_host(hostname)

    if is_reachable:
        print(f"Адрес {hostname} доступен и отвечает на пинг.")
    else:
        print(f"Адрес {hostname} недоступен или не отвечает на пинг.")

    # Предложение ввести другой адрес или выход
    another = input("Хотите проверить другой адрес? (да/нет): ")
    if another.lower() != "да":
        break
