#!/usr/bin/env python3
"""
Шаг 1: Импорт и настройка
Шаг 2: Определение функций сканирования
Шаг 3: Параллельное выполнение и сбор результатов
Шаг 4: Профилировщик и отчёт
"""

import socket                      # Шаг 1.1: для TCP-соединений
from concurrent.futures import ThreadPoolExecutor  # Шаг 1.2: для параллельности
import cProfile                    # Шаг 1.3: для профилирования
from memory_profiler import profile  # Шаг 1.4: для оценки памяти

# Шаг 2: Функция сканирования одного порта
@profile
def scan_port(ip: str, port: int, timeout: float = 0.5) -> bool:
    """
    Вход: ip, порт
    Цель: проверить доступность TCP-порта
    Выход: True если открыт, иначе False
    """
    s = socket.socket()
    s.settimeout(timeout)
    try:
        s.connect((ip, port))       # попытка установить соединение
        s.close()
        return True
    except Exception:
        return False

# Шаг 3: Параллельный скан для одного IP
def scan_host(ip: str, ports: list[int]) -> dict[int, bool]:
    """
    Вход: ip, список портов
    Цель: параллельный запуск scan_port
    Выход: словарь {порт: статус}
    """
    results = {}
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(scan_port, ip, p): p for p in ports}
        for fut in futures:
            port = futures[fut]
            results[port] = fut.result()
    return results

# Шаг 4: Точка входа и профилирование
if __name__ == "__main__":
    target_ips = ["192.168.0.10", "192.168.0.50"]  # Пример адресов
    ports_to_scan = [22, 80, 443, 3389, 8080]      # Пример портов
    profiler = cProfile.Profile()
    profiler.enable()
    for ip in target_ips:
        print(f"Сканирование {ip}: {scan_host(ip, ports_to_scan)}")
    profiler.disable()
    profiler.print_stats(sort="time")