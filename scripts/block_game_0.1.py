# Шаг 1: Импорты и конфигурация
import psutil                    # Работа с процессами
import subprocess                # Вызов консольных команд
import threading                 # Таймер
import time                      # Ожидание
from datetime import datetime    # Работа с датой и временем

BLOCK_LIST = ["GenshinImpact.exe", "another_game.exe"]
CHECK_INTERVAL = 5               # секунд
SCHEDULE = [("22:00", "23:59"), ("00:00", "07:00")]

# Шаг 2: Функции для блокировки/разблокировки сети
def block_network():
    """Добавление правила в Windows Firewall для блокировки всех входящих/исходящих."""
    subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "state", "off"])
    # cProfile можно подключить здесь

def unblock_network():
    """Восстановление доступа."""
    subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "state", "on"])

# Шаг 3: Проверка и завершение процессов
def monitor_and_block():
    now = datetime.now().strftime("%H:%M")
    should_block = any(start <= now <= end for start, end in SCHEDULE)
    if should_block:
        block_network()
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] in BLOCK_LIST:
                proc.kill()
    else:
        unblock_network()
    threading.Timer(CHECK_INTERVAL, monitor_and_block).start()

# Шаг 4: Запуск мониторинга
if __name__ == "__main__":
    monitor_and_block()
