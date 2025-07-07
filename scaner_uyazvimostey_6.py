import socket
import argparse
import ipaddress
import json
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from typing import List, Optional

# --- Проверка открытости порта ---
def scan_port(ip: str, port: int, timeout: float) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
        return True
    except:
        return False

# --- Получение баннера (баннерграббинг) ---
def grab_banner(ip: str, port: int, timeout: float) -> Optional[str]:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            banner = s.recv(1024)
            return banner.decode(errors='ignore').strip()
    except:
        return None

# --- Расширенная проверка уязвимостей по баннеру ---
def check_vulnerabilities(port: int, banner: Optional[str]) -> List[str]:
    vulns = []
    if not banner:
        return vulns

    import re

    # SSH (порт 22)
    if port == 22 and "SSH" in banner:
        match = re.search(r'SSH-.*?([\d\.]+)', banner)
        if match:
            version = match.group(1)
            major_version = int(version.split('.')[0])
            if major_version < 7:
                vulns.append(f"SSH version {version} < 7.0 - уязвимая версия")

    # HTTP (обычно 80, 8080, 8000, 443)
    elif port in (80, 8080, 8000, 443) and ("Apache" in banner or "nginx" in banner.lower()):
        # Apache
        match = re.search(r'Apache/([\d\.]+)', banner)
        if match:
            version = match.group(1)
            major, minor, *rest = map(int, version.split('.'))
            if (major, minor) < (2, 4):
                vulns.append(f"Apache version {version} < 2.4 - уязвимая версия")

        # nginx
        match_nginx = re.search(r'nginx/([\d\.]+)', banner.lower())
        if match_nginx:
            version = match_nginx.group(1)
            major, minor, *rest = map(int, version.split('.'))
            if (major, minor) < (1, 14):
                vulns.append(f"nginx version {version} < 1.14 - потенциально уязвимая версия")

    # FTP (порт 21)
    elif port == 21 and "vsFTPd" in banner:
        match = re.search(r'vsFTPd\s*([\d\.]+)', banner)
        if match:
            version = match.group(1)
            major, minor, *rest = map(int, version.split('.'))
            if (major, minor) < (3, 0):
                vulns.append(f"vsFTPd version {version} < 3.0 - уязвимая версия")

    # Можно добавить свои проверки для других сервисов

    return vulns

# --- Сканирование IP (проверка "живости") ---
def scan_ip(ip: str, timeout: float) -> bool:
    # Проверяем доступность хоста через порт 80 (можно изменить)
    return scan_port(ip, 80, timeout)

# --- Загрузка IP из файла ---
def load_ips_from_file(filename: str) -> List[str]:
    ips = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                ips.append(line)
    return ips

# --- Парсинг портов (поддержка диапазонов) ---
def parse_ports(port_str: str) -> List[int]:
    ports = []
    parts = port_str.split(',')
    for part in parts:
        if '-' in part:
            start, end = part.split('-')
            ports.extend(range(int(start), int(end) + 1))
        else:
            ports.append(int(part))
    return sorted(set(ports))

# --- Основной запуск ---
def main():
    parser = argparse.ArgumentParser(description="Сканер IP и TCP портов с баннерграббингом и проверкой уязвимостей")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--subnet", help="Подсеть в формате CIDR, например 192.168.1.0/24")
    group.add_argument("--ipfile", help="Файл с IP-адресами, по одному на строку")
    parser.add_argument("--ports", default="22,80,443,3389,8080", help="Порты через запятую, поддерживается диапазон через '-'")
    parser.add_argument("--timeout", type=float, default=1.0, help="Таймаут соединения в секундах")
    parser.add_argument("--max_workers_ip", type=int, default=100, help="Потоков для сканирования IP")
    parser.add_argument("--max_workers_port", type=int, default=200, help="Потоков для сканирования портов")
    parser.add_argument("--output", choices=['json', 'csv'], default='json', help="Формат вывода")
    parser.add_argument("--outfile", default="scan_results", help="Имя выходного файла без расширения")
    args = parser.parse_args()

    if args.subnet:
        network = ipaddress.ip_network(args.subnet, strict=False)
        ip_list = [str(ip) for ip in network.hosts()]
    else:
        ip_list = load_ips_from_file(args.ipfile)

    print(f"Сканирование живых хостов среди {len(ip_list)} IP...")
    live_ips = []
    with ThreadPoolExecutor(max_workers=args.max_workers_ip) as executor:
        futures = {executor.submit(scan_ip, ip, args.timeout): ip for ip in ip_list}
        for future in tqdm(as_completed(futures), total=len(futures), desc="IP сканирование"):
            ip = futures[future]
            try:
                if future.result():
                    live_ips.append(ip)
            except:
                pass

    print(f"Найдено живых хостов: {len(live_ips)}")

    ports = parse_ports(args.ports)

    print(f"Сканирование портов {ports} на живых хостах...")
    results = []
    with ThreadPoolExecutor(max_workers=args.max_workers_port) as executor:
        futures = {}
        for ip in live_ips:
            for port in ports:
                futures[executor.submit(scan_port, ip, port, args.timeout)] = (ip, port)

        for future in tqdm(as_completed(futures), total=len(futures), desc="Порт сканирование"):
            ip, port = futures[future]
            try:
                if future.result():
                    banner = grab_banner(ip, port, args.timeout)
                    vulns = check_vulnerabilities(port, banner)
                    results.append({
                        "ip": ip,
                        "port": port,
                        "banner": banner,
                        "vulnerabilities": vulns
                    })
            except:
                pass

    print(f"Найдено открытых портов: {len(results)}")

    outfile = f"{args.outfile}.{args.output}"
    print(f"Сохраняем результаты в файл: {outfile}")
    if args.output == "json":
        with open(outfile, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    else:
        with open(outfile, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["ip", "port", "banner", "vulnerabilities"])
            writer.writeheader()
            for row in results:
                row_copy = row.copy()
                row_copy["vulnerabilities"] = "; ".join(row_copy["vulnerabilities"]) if row_copy["vulnerabilities"] else ""
                writer.writerow(row_copy)

    print("Готово.")

if __name__ == "__main__":
    main()
