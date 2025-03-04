from scapy.all import *
import time

# Функция для отправки ICMP-запроса на конкретный IP
def send_broadcast():
    packet = Ether(dst="FF:FF:FF:FF:FF:FF") / IP(dst="192.168.0.100") / ICMP()
    print("Отправка ICMP-запроса на 192.168.0.100...")
    sendp(packet)

# Функция для прослушивания ответов
def listen_for_responses():
    print("Ожидание ответов...")
    ans, unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF") / IP(dst="192.168.0.100") / ICMP(), timeout=5)

    if ans:
        for s, r in ans:
            print(f"Получен ответ от {r[IP].src} с MAC-адресом {r[Ether].src}")
    else:
        print("Ответов не получено.")

# Основной блок программы
if __name__ == "__main__":
    send_broadcast()    # Отправляем ICMP-запрос
    time.sleep(1)       # Даем время на отправку
    listen_for_responses()  # Прослушиваем ответы
