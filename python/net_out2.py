from scapy.all import *
import time
from threading import Thread

# Функция для отправки пакета
def send_broadcast():
    # Создаём Ethernet-кадр с широковещательным MAC-адресом
    packet = Ether(dst="FF:FF:FF:FF:FF:FF") / IP(dst="192.168.0.255") / ICMP()

    print("Отправка широковещательного пакета...")
    # Отправляем пакет в локальную сеть
    sendp(packet)

# Функция для прослушивания ответов с помощью AsyncSniff
def sniff_packets():
    print("Ожидание ответов...")
    # Прослушиваем сеть, фильтруем по протоколу ICMP, чтобы получать только ответы на пинги
    sniff(filter="icmp", prn=process_packet, store=0, timeout=5)

# Функция обработки полученных пакетов
def process_packet(packet):
    # Если пакет ICMP (пинг), выводим информацию о пакете
    if packet.haslayer(ICMP):
        print(f"Получен ответ от {packet[IP].src} с MAC-адресом {packet[Ether].src}")

# Основной блок программы
if __name__ == "__main__":
    # Запускаем асинхронное прослушивание в отдельном потоке
    sniff_thread = Thread(target=sniff_packets)
    sniff_thread.start()

    # Отправляем широковещательный пакет
    send_broadcast()

    # Ждем, пока завершится поток с прослушиванием
    sniff_thread.join()
