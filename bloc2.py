import pydivert
import re

def load_blacklist():
    # Загрузить черный список сайтов
    return ["vk.com", "ok.ru", "t.me"]
def is_blocked_site(host, blacklist):
    # Проверить, является ли хост (имя сайта) в черном списке
    for blocked_site in blacklist:
        if re.search(blocked_site, host, re.IGNORECASE):
            return True
    return False

def main():
    blacklist = load_blacklist()
    
    with pydivert.WinDivert("outbound and udp.DstPort == 53") as w:
        print("Программа брандмауэра запущена.")
        
        try:
            for packet in w:
                if packet.is_outbound and packet.is_dns_request:
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
