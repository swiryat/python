from scapy.all import *
import time

# Функция для отправки пакета
def send_broadcast():
    # Создаём Ethernet-кадр с широковещательным MAC-адресом
    packet = Ether(dst="FF:FF:FF:FF:FF:FF") / IP(dst="192.168.0.255") / ICMP()

    print("Отправка широковещательного пакета...")
    # Отправляем пакет в локальную сеть
    sendp(packet)

# Функция для прослушивания ответов
def listen_for_responses():
    print("Ожидание ответов...")
    # Слушаем ответы на широковещательный адрес в течение 5 секунд
    ans, unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF") / IP(dst="192.168.0.255") / ICMP(), timeout=5)

    if ans:
        for s, r in ans:
            print(f"Получен ответ от {r[IP].src} с MAC-адресом {r[Ether].src}")
    else:
        print("Ответов не получено.")

# Основной блок программы
if __name__ == "__main__":
    send_broadcast()    # Отправляем широковещательный пакет
    time.sleep(1)       # Даем время на отправку
    listen_for_responses()  # Прослушиваем ответы
