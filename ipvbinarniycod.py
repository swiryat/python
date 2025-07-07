def ip_to_binary(ip_address):
    # Разбиваем IP-адрес на отдельные октеты
    octets = ip_address.split('.')
    # Преобразуем каждый октет в бинарное представление и объединяем их
    binary_ip = '.'.join([bin(int(octet))[2:].zfill(8) for octet in octets])
    return binary_ip

ip_address = input("Введите IP-адрес: ")
binary_ip = ip_to_binary(ip_address)
print("Бинарное представление IP-адреса:", binary_ip)

