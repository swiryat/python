import pydivert
import ipaddress

def load_whitelist():
    # Загрузить белый список IP-адресов из файла или другого источника
    return [ipaddress.ip_network("192.168.1.0/24")]

def load_blacklist():
    # Загрузить черный список IP-адресов из файла или другого источника
    return [ipaddress.ip_network("10.0.0.0/8")]

def is_allowed_ip(ip, whitelist, blacklist):
    # Проверить, является ли IP-адрес разрешенным
    for allowed_net in whitelist:
        if ip in allowed_net:
            return True
    
    # Проверить, не является ли IP-адрес запрещенным
    for blocked_net in blacklist:
        if ip in blocked_net:
            return False
    
    # Если IP-адрес не входит ни в белый, ни в черный список, разрешить его
    return True

def main():
    whitelist = load_whitelist()
    blacklist = load_blacklist()
    
    # Создать объект перехвата сетевого трафика
    with pydivert.WinDivert("ip") as w:
        print("Программа брандмауэра запущена.")
        
        try:
            for packet in w:
                ip = ipaddress.ip_address(packet.src_addr)
                
                if is_allowed_ip(ip, whitelist, blacklist):
                    # Пропустить разрешенный трафик
                    w.send(packet)
                else:
                    # Заблокировать запрещенный трафик
                    print(f"Заблокирован трафик от {ip}")
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()
