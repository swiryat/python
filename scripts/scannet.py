import os
import socket
import subprocess
from scapy.all import *
import json
import time

# Функция для получения IP-адресов в локальной сети
def get_local_ip():
    local_ip = socket.gethostbyname(socket.gethostname())
    return local_ip

# Функция для выполнения ARP-запроса и получения MAC-адресов устройств в локальной сети
def scan_network(network):
    print(f"Сканирование сети {network}...")
    devices = []
    # ARP запрос
    ans, unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF") / ARP(pdst=network), timeout=3)
    
    for s, r in ans:
        devices.append({'ip': r[ARP].psrc, 'mac': r[Ether].src})
    
    return devices

# Функция для получения информации о маршрутах
def get_routes():
    result = subprocess.run(['route', 'print'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    routes = result.stdout.decode('cp1251', errors='ignore')  # Используем cp1251 для Windows
    return routes


def get_dns():
    result = subprocess.run('ipconfig /all', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    try:
        dns_info = result.stdout.decode('utf-8')  # Попробуем UTF-8
    except UnicodeDecodeError:
        dns_info = result.stdout.decode('cp1251')  # Пытаемся с cp1251 для русскоязычных систем
    return dns_info


# Функция для получения информации о сетевых интерфейсах
def get_network_interfaces():
    interfaces = []
    # Получаем информацию о сетевых интерфейсах
    result = subprocess.run(['ip', 'a'], stdout=subprocess.PIPE)
    interfaces_info = result.stdout.decode('utf-8')
    
    interfaces.append(interfaces_info)
    return interfaces

# Основная функция
def main():
    # Получаем локальный IP-адрес
    local_ip = get_local_ip()
    print(f"Локальный IP-адрес: {local_ip}")

    # Сканируем сеть
    network = "192.168.1.0/24"  # Замените на вашу сеть
    devices = scan_network(network)
    print(f"Устройства в сети {network}: {devices}")

    # Получаем маршруты
    routes = get_routes()
    print(f"Маршруты: {routes}")

    # Получаем DNS-серверы
    dns_servers = get_dns()
    print(f"DNS-серверы: {dns_servers}")

    # Получаем информацию о сетевых интерфейсах
    interfaces = get_network_interfaces()
    print(f"Интерфейсы: {interfaces}")

    # Сохраняем данные в JSON файл
    network_data = {
        "local_ip": local_ip,
        "devices": devices,
        "routes": routes,
        "dns_servers": dns_servers,
        "interfaces": interfaces
    }

    # Сохраняем информацию в файл
    with open("network_info.json", "w") as f:
        json.dump(network_data, f, indent=4)

    print("Информация о сети сохранена в 'network_info.json'.")

# Запуск программы
if __name__ == "__main__":
    main()
