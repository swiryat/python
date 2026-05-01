import pydivert
import re
import subprocess

def load_blacklist():
    # Загрузить черный список сайтов
    return ["example.com", "malicious-site.com", "blocked-site.com", "another-blocked-site.com"]

def clear_dns_cache():
    # Очистить DNS-кеш в системе Windows
    subprocess.run(["ipconfig", "/flushdns"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def is_blocked_site(host, blacklist):
    # Проверить, является ли хост (имя сайта) в черном списке
    for blocked_site in blacklist:
        if re.search(blocked_site, host, re.IGNORECASE):
            return True
    return False

def main():
    clear_dns_cache()  # Очистить DNS-кеш при каждом запуске программы
    blacklist = load_blacklist()
    
    with pydivert.WinDivert("udp.DstPort == 53") as w:
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
                else:
                    # Пропустить все другие пакеты
                    w.send(packet)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()
