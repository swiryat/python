import pyfiglet
import sys
import socket
from datetime import datetime

ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
print(ascii_banner)

# Проверка аргументов командной строки
if len(sys.argv) != 3:
    print("Неверное количество аргументов!")
    print("Правильный формат: python scanerportov.py <target> <port_range>")
    print("Пример: python scanerportov.py 192.168.1.1 100")
    sys.exit(1)

# Устанавливаем целевой IP и диапазон портов
target = socket.gethostbyname(sys.argv[1])
port_range = int(sys.argv[2])

print("-" * 50)
print("Scanning Target: " + target)
print("Scanning started at:" + str(datetime.now()))
print("-" * 50)

try:
    for port in range(1, port_range + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)

        # Отладочное сообщение для каждого порта
        print(f"Проверка порта {port}...")

        result = s.connect_ex((target, port))
        if result == 0:
            print(f"Port {port} is open")
        s.close()
except KeyboardInterrupt:
    print("\nExiting Program")
    sys.exit()
except socket.gaierror:
    print("\nHostname Could Not Be Resolved")
    sys.exit()
except socket.error:
    print("\nServer not responding")
    sys.exit()

print("-" * 50)
print("Scanning completed.")
