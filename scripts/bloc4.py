import pydivert
import re
import subprocess

def load_blacklist():
    # Загрузить черный список сайтов и IP-адресов
    return {
        "sites": ["example.com", "malicious-site.com", "blocked-site.com", "another-blocked-site.com"],
        "ip_addresses": ["10.0.0.1", "192.168.1.2"]
    }

def clear_dns_cache():
    # Очистить DNS-кеш в системе Windows
    subprocess.run(["ipconfig", "/flushdns"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
                    dns_request = packet.dns
                    host = dns_request.qry_name.decode("utf-8")
                    
                    if is_blocked_site(host, blacklist):
                        # Заблокировать DNS-запрос к запрещенному сайту
                        print(f"DNS-запрос к запрещенному сайту: {host}")
                        packet.dns.qry_name = b"blocked-site.com"
                        w.send(packet)
                    else:
                        # Пропустить разрешенный DNS-запрос
                        w.send(packet)
                elif packet.is_outbound:
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
