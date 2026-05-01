# Импортируем библиотеки
import socket
import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict
from datetime import datetime
import argparse
import ipaddress
import json
import csv
from tqdm import tqdm


# Проверка доступности IP (ping)
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


# Проверка TCP-порта с баннерграббингом
def scan_port(ip: str, port: int, timeout: float = 0.5) -> Dict:
    result = {"port": port, "open": False, "banner": ""}
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            result["open"] = True
            try:
                s.sendall(b"\r\n")
                banner = s.recv(1024)
                result["banner"] = banner.decode(errors="ignore").strip()
            except:
                result["banner"] = ""
    except:
        pass
    return result


# Сканирование всех портов на одном хосте
def scan_host(ip: str, ports: List[int], timeout: float = 0.5, max_workers: int = 100) -> List[Dict]:
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(scan_port, ip, port, timeout) for port in ports]
        for future in tqdm(as_completed(futures), total=len(futures), desc=f"Сканирование портов {ip}"):
            result = future.result()
            if result["open"]:
                results.append(result)
    return results


# Обработка диапазона портов
def parse_ports(port_str: str) -> List[int]:
    ports = []
    for part in port_str.split(","):
        if "-" in part:
            start, end = map(int, part.split("-"))
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))
    return ports


# Аргументы командной строки
def parse_args():
    parser = argparse.ArgumentParser(description="Сканер TCP-портов с CIDR, баннером и экспортом")
    parser.add_argument("--subnet", required=True, help="CIDR-подсеть, например 192.168.1.0/24")
    parser.add_argument("--ports", default="22,80,443", help="Список портов или диапазон (напр. 20-80)")
    parser.add_argument("--timeout", type=float, default=0.5, help="Таймаут в секундах")
    parser.add_argument("--workers", type=int, default=100, help="Число потоков")
    parser.add_argument("--output", choices=["csv", "json"], default="json", help="Формат вывода")
    parser.add_argument("--outfile", default="scan_results", help="Имя выходного файла без расширения")
    return parser.parse_args()


# Сохранение в CSV
def save_csv(filename: str, data: List[Dict]):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["ip", "port", "banner"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)


# Сохранение в JSON
def save_json(filename: str, data: List[Dict]):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# Основной запуск
def main():
    args = parse_args()
    ports = parse_ports(args.ports)
    all_ips = [str(ip) for ip in ipaddress.ip_network(args.subnet, strict=False)]

    print(f"[{datetime.now()}] Поиск активных IP в {args.subnet}...")

    active_ips = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [executor.submit(ping_ip, ip, args.timeout) for ip in all_ips]
        for i, future in enumerate(tqdm(as_completed(futures), total=len(futures), desc="Проверка доступности IP")):
            ip = all_ips[i]
            if future.result():
                active_ips.append(ip)

    print(f"\nНайдено активных IP: {len(active_ips)}\n")

    full_results = []
    for ip in active_ips:
        print(f" → Сканирование {ip}")
        open_ports = scan_host(ip, ports, args.timeout, args.workers)
        for res in open_ports:
            full_results.append({"ip": ip, **res})

    # Сохранение
    out_file = f"{args.outfile}.{args.output}"
    if args.output == "csv":
        save_csv(out_file, full_results)
    else:
        save_json(out_file, full_results)

    print(f"\n✅ Результаты сохранены в: {out_file}")


if __name__ == "__main__":
    main()

