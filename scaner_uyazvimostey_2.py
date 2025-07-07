# scaner_uyazvimostey_optimized.py

import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict
import argparse
from datetime import datetime

# Шаг 1. Проверка одного порта
def scan_port(ip: str, port: int, timeout: float = 0.5) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            return True
    except:
        return False

# Шаг 2. Сканирование всех портов
def scan_host(ip: str, ports: List[int], max_workers: int = 100) -> Dict[int, bool]:
    open_ports = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_port = {executor.submit(scan_port, ip, port): port for port in ports}
        for future in as_completed(future_to_port):
            port = future_to_port[future]
            try:
                open_ports[port] = future.result()
            except Exception:
                open_ports[port] = False
    return open_ports

# Шаг 3. Парсинг диапазонов и отдельных портов
def parse_ports(ports_str: str) -> List[int]:
    ports = set()
    for part in ports_str.split(','):
        part = part.strip()
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                ports.update(range(start, end + 1))
            except ValueError:
                raise argparse.ArgumentTypeError(f"Неверный диапазон портов: {part}")
        else:
            try:
                ports.add(int(part))
            except ValueError:
                raise argparse.ArgumentTypeError(f"Неверный порт: {part}")
    return sorted(ports)

# Шаг 4. Аргументы командной строки
def parse_args():
    parser = argparse.ArgumentParser(description="Сканер TCP-портов")
    parser.add_argument("--ip", required=True, help="IP-адрес")
    parser.add_argument("--ports", default="22,80,443,3389,8080", help="Список портов через запятую и/или диапазоны")
    parser.add_argument("--timeout", type=float, default=0.5, help="Таймаут в секундах")
    return parser.parse_args()

# Шаг 5. Главный запуск
def main():
    args = parse_args()
    ports = parse_ports(args.ports)

    if len(ports) > 65535:
        print("⚠️ Слишком много портов. Проверь аргумент --ports.")
        return

    print(f"[{datetime.now()}] Сканирование IP {args.ip}...")
    results = scan_host(args.ip, ports)
    print(f"\nРезультаты сканирования:")
    for port, is_open in results.items():
        status = "ОТКРЫТ" if is_open else "закрыт"
        print(f" → Порт {port}: {status}")

if __name__ == "__main__":
    main()
