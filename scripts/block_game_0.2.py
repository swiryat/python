# Шаг 1: Импорты и конфигурация
import psutil                    # Работа с процессами
import subprocess                # Вызов netsh
import threading                 # Для таймера
from datetime import datetime    # Время

# Шаг 2: Настройки
BLOCK_LIST = ["GenshinImpact.exe"]  # Названия процессов (можно добавить свои)
EXE_PATH = r"E:\HoYoPlay\games\Genshin Impact game\GenshinImpact.exe"  # Полный путь к .exe
CHECK_INTERVAL = 5  # интервал в секундах
SCHEDULE = [("22:00", "23:59"), ("00:00", "07:00")]  # Время, когда блокировка активна

# Шаг 3: Функции блокировки сети — только для этой игры
def block_network():
    for direction in ["in", "out"]:
        subprocess.run([
            "netsh", "advfirewall", "firewall", "add", "rule",
            f"name=Block_Genshin_{direction}",
            f"dir={direction}",
            "action=block",
            f"program={EXE_PATH}",
            "enable=yes"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Интернет для Genshin заблокирован.")

def unblock_network():
    for direction in ["in", "out"]:
        subprocess.run([
            "netsh", "advfirewall", "firewall", "delete", "rule",
            f"name=Block_Genshin_{direction}"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Блокировка Genshin снята.")

# Шаг 4: Проверка времени
def is_within_schedule():
    now = datetime.now().strftime("%H:%M")
    for start, end in SCHEDULE:
        if start <= now <= end:
            return True
    return False

# Шаг 5: Основная логика
def monitor_and_block():
    if is_within_schedule():
        block_network()
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] in BLOCK_LIST:
                    proc.kill()
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Завершён процесс: {proc.info['name']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    else:
        unblock_network()

    # Повторить через CHECK_INTERVAL секунд
    threading.Timer(CHECK_INTERVAL, monitor_and_block).start()

# Шаг 6: Запуск
if __name__ == "__main__":
    print("[INFO] Мониторинг запущен. Нажмите Ctrl+C для выхода.")
    monitor_and_block()
