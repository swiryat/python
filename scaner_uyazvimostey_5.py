import socket
import argparse
import ipaddress
import json
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from typing import List, Dict, Optional, Union

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
            # Пробуем получить баннер - часто сервер что-то шлёт после подключения
            banner = s.recv(1024)
            return banner.decode(errors='ignore').strip()
    except:
        return None

# --- Проверка уязвимостей по баннеру ---
def check_vulnerabilities(port: int, banner: Optional[str]) -> List[str]:
    vulns = []
    if banner:
        # Пример проверки SSH версии < 7.0
        if port == 22 and "SSH" in banner:
            import re
            match = re.search(r'SSH-.*?([\d\.]+)', banner)
            if match:
                version = match.group(1)
                major_version = int(version.split('.')[0])
                if major_version < 7:
                    vulns.append(f"SSH version {version} < 7.0 - уязвимая версия")
    return vulns

# --- Сканирование IP ---
def scan_ip(ip: str, timeout: float) -> bool:
    # Попытка подключиться на популярный порт (например 80), чтобы проверить "жив ли" хост
    # Можно расширить или сделать ping (но ping требует дополнительных привилегий)
    # Здесь делаем попытку порта 80 для проверки хоста
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

# --- Основной скан ---
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

    # Получаем список IP для сканирования
    if args.subnet:
        network = ipaddress.ip_network(args.subnet, strict=False)
        ip_list = [str(ip) for ip in network.hosts()]
    else:
        ip_list = load_ips_from_file(args.ipfile)

    # Сканируем IP (проверка «живой» хост)
    print(f"Сканирование живых хостов среди {len(ip_list)} IP...")
    live_ips = []
    with ThreadPoolExecutor(max_workers=args.max_workers_ip) as executor:
        futures = {executor.submit(scan_ip, ip, args.timeout): ip for ip in ip_list}
        for future in tqdm(as_completed(futures), total=len(futures), desc="IP сканирование"):
            ip = futures[future]
            try:
                if future.result():
                    live_ips.append(ip)
            except Exception:
                pass

    print(f"Найдено живых хостов: {len(live_ips)}")

    ports = parse_ports(args.ports)

    # Сканируем порты на живых IP и собираем баннеры и уязвимости
    results = []
    print(f"Сканирование портов {ports} на живых хостах...")
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
            except Exception:
                pass

    print(f"Найдено открытых портов: {len(results)}")

    # Сохраняем результаты
    outfile = f"{args.outfile}.{args.output}"
    print(f"Сохраняем результаты в файл: {outfile}")
    if args.output == "json":
        with open(outfile, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    else:  # csv
        with open(outfile, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["ip", "port", "banner", "vulnerabilities"])
            writer.writeheader()
            for row in results:
                # vulnerabilities — список, конвертируем в строку
                row_copy = row.copy()
                row_copy["vulnerabilities"] = "; ".join(row_copy["vulnerabilities"]) if row_copy["vulnerabilities"] else ""
                writer.writerow(row_copy)

    print("Готово.")

if __name__ == "__main__":
    main()
