import os
import socket
import psutil
import platform
import uuid
import subprocess
import json
import pandas as pd


# Функции для получения информации о сети

def get_hostname():
    return socket.gethostname()

def get_local_ip():
    try:
        return socket.gethostbyname(get_hostname())
    except socket.gaierror:
        return "Не удалось определить"

def get_mac_address():
    return ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2*6, 8)][::-1])

def get_network_interfaces():
    interfaces = {}
    for interface_name, interface_info in psutil.net_if_addrs().items():
        addresses = []
        for addr in interface_info:
            if addr.family == socket.AF_INET:
                addresses.append(addr.address)
        interfaces[interface_name] = addresses
    return interfaces

def get_active_connections():
    return [
        {
            "Протокол": "TCP" if conn.type == socket.SOCK_STREAM else "UDP",
            "Локальный адрес": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A",
            "Удалённый адрес": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
            "Статус": conn.status
        }
        for conn in psutil.net_connections(kind="inet")
    ]

def get_network_traffic():
    net_io = psutil.net_io_counters()
    return {
        "Отправлено байтов": net_io.bytes_sent,
        "Получено байтов": net_io.bytes_recv
    }

def get_routing_table():
    command = "route print" if platform.system() == "Windows" else "ip route"
    try:
        # Используем cp1251 для Windows
        result = subprocess.getoutput(command)
        if platform.system() == "Windows":
            result = result.encode("cp1251").decode("utf-8", errors="ignore")
        return result
    except Exception as e:
        return f"Ошибка: {e}"


def get_all_network_info():
    return {
        "Имя хоста": get_hostname(),
        "Локальный IP": get_local_ip(),
        "MAC-адрес": get_mac_address(),
        "Сетевые интерфейсы": get_network_interfaces(),
        "Активные соединения": get_active_connections(),
        "Сетевой трафик": get_network_traffic(),
        "Таблица маршрутизации": get_routing_table()
    }

# Анализ активных соединений с помощью netstat

def analyze_netstat_connections():
    # Выполнение команды для получения информации о сетевых соединениях
    result = subprocess.run("netstat -a -n -o -p tcp,udp", capture_output=True, text=True, shell=True)

    # Проверка на ошибки выполнения команды
    if result.returncode != 0:
        return None, None, None, f"Ошибка выполнения команды netstat: {result.stderr}"

    # Разбор вывода на строки
    lines = result.stdout.splitlines()

    # Извлекаем заголовки
    headers = ["Протокол", "Локальный адрес", "Удалённый адрес", "Статус"]

    # Список для хранения данных
    data = []

    # Проход по каждой строке и извлечение нужной информации
    for line in lines:
        if line.startswith('  '):  # Пропускаем строки, которые не содержат нужной информации
            continue
        parts = line.split()

        # Пропускаем строки, которые не содержат нужных данных
        if len(parts) < 5:
            continue

        protocol = parts[0]
        local_address = parts[1]
        remote_address = parts[2]
        status = parts[3] if protocol == "TCP" else "N/A"

        # Добавляем данные в список
        data.append([protocol, local_address, remote_address, status])

    # Создаем DataFrame с помощью pandas
    df = pd.DataFrame(data, columns=headers)

    # Дополнительный анализ
    status_counts = df["Статус"].value_counts()
    protocol_counts = df["Протокол"].value_counts()

    return df, status_counts, protocol_counts, None

if __name__ == "__main__":
    # Получаем общую информацию о сети
    network_info = get_all_network_info()
    print("Информация о сети:")
    print(json.dumps(network_info, indent=4, ensure_ascii=False))

    # Выполняем анализ активных соединений
    df, status_counts, protocol_counts, error = analyze_netstat_connections()

    if error:
        print("\nОшибка при анализе соединений:", error)
    else:
        # Выводим таблицу активных соединений
        print("\nТаблица активных соединений:")
        print(df)

        # Выводим анализ по статусу соединений
        print("\nАнализ соединений по статусу:")
        print(status_counts)

        # Выводим анализ по протоколам
        print("\nАнализ соединений по протоколу:")
        print(protocol_counts)
