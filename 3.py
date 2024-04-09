import subprocess
import socket
import subprocess

def ping_host(target):
    try:
        # Попытка определить тип адреса (IP или доменное имя)
        is_ip_address = True
        try:
            socket.inet_aton(target)
        except socket.error:
            is_ip_address = False

        if is_ip_address:
            result = subprocess.run(['ping', '-c', '4', target], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        else:
            result = subprocess.run(['ping', '-c', '4', '-n', target], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        output = result.stdout
        return "TTL=" in output
    except subprocess.CalledProcessError:
        return False
    

      # Вывести, какой исполняемый файл ping используется
    ping_path = subprocess.check_output(['where', 'ping'], text=True)
    print(f"Исполняемый файл ping: {ping_path.strip()}")


while True:
    # Запрос адреса у пользователя
    target = input("Введите адрес для пинга (IP-адрес или доменное имя): ")

    # Осуществляем пинг
    is_reachable = ping_host(target)

    if is_reachable:
        print(f"Адрес {target} доступен и отвечает на пинг.")
    else:
        print(f"Адрес {target} недоступен или не отвечает на пинг.")

    # Предложение ввести другой адрес или выход
    another = input("Хотите проверить другой адрес? (да/нет): ")
    if another.lower() != "да":
        break
