import threading

def dummy_function():
    while True:
        pass  # Поток выполняет бесконечный цикл

threads = []
count = 0

try:
    while True:
        t = threading.Thread(target=dummy_function)
        t.start()
        threads.append(t)
        count += 100
        print(f"Потоков запущено: {count}")
except RuntimeError as e:
    print(f"Ошибка! Достигнуто {count} потоков. {e}")
