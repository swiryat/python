import pydivert
import re
import subprocess
import ipaddress

def add_ip_range_to_blacklist(ip_range_start, ip_range_end, blacklist):
    # Очистить существующий список IP-адресов
    blacklist["ip_addresses"] = []

    # Добавить диапазон IP-адресов в черный список
    ip_range = ipaddress.IPv4Network(f"{ip_range_start} - {ip_range_end}", strict=False)
    blacklist["ip_addresses"].extend([str(ip) for ip in ip_range])

def clear_dns_cache():
    # Очистить DNS-кеш в системе Windows
    subprocess.run(["ipconfig", "/flushdns"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def load_blacklist():
    # Загрузить черный список сайтов и IP-адресов
    return {
        "sites": ["vk.com"],
        "ip_addresses": ["93.186.228.130", "93.186.229.2", "93.186.229.3", "93.186.224.233", "93.186.224.234",
                         "93.186.224.235", "93.186.224.236", "93.186.224.238", "93.186.224.239", "93.186.225.6",
                         "93.186.225.211", "93.186.226.4", "93.186.226.5", "93.186.226.129", "93.186.226.130",
                         "93.186.227.123", "93.186.227.124", "93.186.227.125", "93.186.227.126", "93.186.227.129",
                         "93.186.227.130", "93.186.228.129"]
    }

def is_blocked_site(host, blacklist):
    # Проверить, является ли хост (имя сайта или IP-адрес) в черном списке
    for blocked_site in blacklist["sites"]:
        if re.search(blocked_site, host, re.IGNORECASE):
            return True
    return False

def is_blocked_ip(ip, blacklist):
    # Проверить, является ли IP-адрес в черном списке
    return ip in blacklist["ip_addresses"]

def main():
    clear_dns_cache()  # Очистить DNS-кеш при каждом запуске программы
    blacklist = load_blacklist()
    
    with pydivert.WinDivert("udp.DstPort == 53 or outbound") as w:
        print("Программа брандмауэра запущена.")
        
        try:
            for packet in w:
                if packet.is_dns_request:
                    # Заблокировать все DNS-запросы
                    print("Заблокирован DNS-запрос")
                    continue

                if packet.is_outbound:
                    ip_header = packet.ipv4 if packet.ipv4 else packet.ipv6
                    if is_blocked_ip(ip_header.src_addr, blacklist) or is_blocked_ip(ip_header.dst_addr, blacklist):
                        # Заблокировать сетевой трафик к/от запрещенного IP-адреса
                        print(f"Заблокирован сетевой трафик: {ip_header.src_addr} -> {ip_header.dst_addr}")
                        continue
                    else:
                        # Пропустить разрешенный сетевой трафик
                        w.send(packet)
                else:
                    # Пропустить все другие пакеты
                    w.send(packet)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()
