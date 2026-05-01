import socket
import argparse
import ipaddress
import re
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional
from tqdm import tqdm
from datetime import datetime
import csv

# === Шаг 1. Считывание правил ===
def load_rules(rule_path: str):
    with open(rule_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# === Шаг 2. Сравнение версий (семантическое) ===
def compare_versions(vuln_ver: str, safe_ver: str) -> bool:
    def parse(ver): return list(map(int, re.findall(r'\d+', ver)))
    return parse(vuln_ver) < parse(safe_ver)

# === Шаг 3. Баннерграббинг и проверка на уязвимость ===
def grab_banner(ip: str, port: int, timeout: float = 1.0) -> str:
    try:
        with socket.create_connection((ip, port), timeout=timeout) as s:
            s.settimeout(timeout)
            return s.recv(1024).decode(errors="ignore")
    except:
        return ""

def analyze_banner(banner: str, port: int, rules: List[dict]) -> List[str]:
    findings = []
    for rule in rules:
        ports = rule["ports"]
        if port in ports or "*" in str(ports):
            match = re.search(rule["banner_regex"], banner, re.IGNORECASE)
            if match:
                found_ver = match.group(1)
                if compare_versions(found_ver, rule["min_safe_version"]):
                    findings.append(f"[!] Уязвимость: {rule['name']} (порт {port}) — версия {found_ver} < {rule['min_safe_version']}: {rule['description']}")
    return findings

# === Шаг 4. Сканирование порта ===
def scan_port(ip: str, port: int, timeout: float = 0.5) -> Optional[Dict]:
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            banner = grab_banner(ip, port, timeout)
            return {"port": port, "status": "open", "banner": banner}
    except:
        return None

# === Шаг 5. Сканирование IP ===
def scan_ip(ip: str, ports: List[int], rules: List[dict], timeout: float, max_workers: int) -> Dict:
    result = {"ip": ip, "open_ports": [], "vulnerabilities": []}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scan_port, ip, port, timeout): port for port in ports}
        for future in as_completed(futures):
            res = future.result()
            if res:
                result["open_ports"].append(res["port"])
                findings = analyze_banner(res["banner"], res["port"], rules)
                result["vulnerabilities"].extend(findings)
    return result

# === Шаг 6. Поддержка CIDR и/или файла IP ===
def expand_targets(ip_range: Optional[str], ip_file: Optional[str]) -> List[str]:
    if ip_file:
        with open(ip_file, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    elif ip_range:
        return [str(ip) for ip in ipaddress.IPv4Network(ip_range, strict=False)]
    else:
        return []

# === Шаг 7. Главная точка входа ===
def main():
    parser = argparse.ArgumentParser(description="Расширенный TCP-сканер с проверкой уязвимостей")
    parser.add_argument("--ip", help="CIDR-диапазон (например, 192.168.0.0/24)")
    parser.add_argument("--ip_file", help="Файл со списком IP-адресов")
    parser.add_argument("--ports", default="22,80,443,8080", help="Список портов через запятую или диапазон (например, 20-100)")
    parser.add_argument("--timeout", type=float, default=0.5, help="Таймаут в секундах")
    parser.add_argument("--max_workers_ip", type=int, default=50, help="Количество потоков на IP")
    parser.add_argument("--max_workers_port", type=int, default=100, help="Количество потоков на порты")
    parser.add_argument("--rules", required=True, help="Файл с описанием уязвимостей (JSON)")
    parser.add_argument("--output", help="Файл для вывода результатов (JSON или CSV)")

    args = parser.parse_args()

    # Разбор портов
    if "-" in args.ports:
        start, end = map(int, args.ports.split("-"))
        ports = list(range(start, end + 1))
    else:
        ports = list(map(int, args.ports.split(",")))

    targets = expand_targets(args.ip, args.ip_file)
    if not targets:
        print("❌ Не указаны IP-адреса ни через --ip, ни через --ip_file")
        return

    rules = load_rules(args.rules)
    all_results = []

    print(f"[{datetime.now()}] Начало сканирования {len(targets)} IP-адресов...")

    with ThreadPoolExecutor(max_workers=args.max_workers_ip) as ip_executor:
        future_to_ip = {
            ip_executor.submit(scan_ip, ip, ports, rules, args.timeout, args.max_workers_port): ip
            for ip in targets
        }
        for future in tqdm(as_completed(future_to_ip), total=len(targets), desc="Сканирование IP"):
            result = future.result()
            all_results.append(result)
            if result["open_ports"]:
                print(f"[+] {result['ip']}: Открытые порты: {result['open_ports']}")
                for vuln in result["vulnerabilities"]:
                    print(f"    {vuln}")

    if args.output:
        if args.output.endswith(".json"):
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(all_results, f, indent=4, ensure_ascii=False)
        elif args.output.endswith(".csv"):
            with open(args.output, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["IP", "Открытые порты", "Уязвимости"])
                for res in all_results:
                    writer.writerow([
                        res["ip"],
                        ";".join(map(str, res["open_ports"])),
                        " | ".join(res["vulnerabilities"])
                    ])

if __name__ == "__main__":
    main()
