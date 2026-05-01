import socket
import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict
from datetime import datetime
import argparse

# Шаг 1. Проверка доступности IP (пинг)
def ping_ip(ip: str, timeout: float = 0.5) -> bool:
    try:
        param = "-n" if platform.system().lower() == "windows" else "-c"
        result = subprocess.run(
            ["ping", param, "1", "-w", str(int(timeout * 1000)), ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except:
        return False

# Шаг 2. Проверка порта
def scan_port(ip: str, port: int, timeout: float = 0.5) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            return True
    except:
        return False

# Шаг 3. Сканирование портов на одном IP
def scan_host(ip: str, ports: List[int], timeout: float = 0.5, max_workers: int = 100) -> Dict[int, bool]:
    open_ports = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_port = {executor.submit(scan_port, ip, port, timeout): port for port in ports}
        for future in as_completed(future_to_port):
            port = future_to_port[future]
            try:
                open_ports[port] = future.result()
            except:
                open_ports[port] = False
    return open_ports

# Шаг 4. Генерация IP по маске
def generate_ips(subnet_base: str, start: int = 1, end: int = 254) -> List[str]:
    return [f"{subnet_base}.{i}" for i in range(start, end + 1)]

# Шаг 5. Парсинг диапазонов портов
def parse_ports(port_str: str) -> List[int]:
    ports = []
    for part in port_str.split(","):
        if "-" in part:
            start, end = map(int, part.split("-"))
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))
    return ports

# Шаг 6. Обработка аргументов
def parse_args():
    parser = argparse.ArgumentParser(description="Поиск активных IP и сканирование их портов")
    parser.add_argument("--subnet", required=True, help="Базовая часть подсети, например 192.168.1")
    parser.add_argument("--ports", default="22,80,443", help="Порты: список или диапазон")
    parser.add_argument("--timeout", type=float, default=0.5, help="Таймаут в секундах")
    parser.add_argument("--workers", type=int, default=100, help="Параллельных потоков")
    return parser.parse_args()

# Шаг 7. Главная логика
def main():
    args = parse_args()
    all_ips = generate_ips(args.subnet)
    ports = parse_ports(args.ports)

    print(f"[{datetime.now()}] Поиск активных IP в {args.subnet}.0/24...")
    active_ips = []

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_to_ip = {executor.submit(ping_ip, ip, args.timeout): ip for ip in all_ips}
        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            if future.result():
                active_ips.append(ip)
    
    print(f"Найдено активных хостов: {len(active_ips)}\n")
    
    for ip in active_ips:
        print(f" → Сканирование портов {ip}:")
        result = scan_host(ip, ports, args.timeout, args.workers)
        for port, is_open in result.items():
            if is_open:
                print(f"    [+] Порт {port} открыт")
        print()

if __name__ == "__main__":
    main()
