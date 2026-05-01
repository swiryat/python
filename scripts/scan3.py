import subprocess

def get_network_interfaces():
    result = subprocess.run(['ipconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='cp1251')  # Вывод результата
    print(result.stdout)
    
    # Разбиваем вывод команды на строки
    output = result.stdout.splitlines()
    
    print("Вывод команды ipconfig:")
    print(result.stdout)  # Покажем весь вывод для отладки
    
    interfaces = []  # Инициализируем список для хранения интерфейсов
    current_interface = None  # Сначала интерфейс не выбран
    
    for line in output:
        print(f"Обрабатываем строку: {line}")  # Покажем текущую строку для отладки
        
        # Ищем название интерфейса
        if "adapter" in line:
            # Если был создан предыдущий интерфейс, добавляем его в список
            if current_interface:
                interfaces.append(current_interface)
            current_interface = {'name': line.strip()}  # Начинаем новый интерфейс
        
        # Ищем строку с IPv4-адресом
        elif "IPv4" in line and current_interface is not None:
            current_interface['IPv4'] = line.split(":")[1].strip()
        
        # Ищем строку с IPv6-адресом
        elif "IPv6" in line and current_interface is not None:
            ipv6_address = line.split(":")[1].strip()
            if ipv6_address:
                current_interface['IPv6'] = ipv6_address
    
    # Добавляем последний интерфейс, если он есть
    if current_interface:
        interfaces.append(current_interface)
    
    return interfaces

def main():
    # Получаем список сетевых интерфейсов
    interfaces = get_network_interfaces()
    
    if not interfaces:
        print("Интерфейсы не найдены.")  # Выводим сообщение, если нет интерфейсов
    
    # Выводим информацию о каждом интерфейсе
    for interface in interfaces:
        print(f"Интерфейс: {interface['name']}")
        if 'IPv4' in interface:
            print(f"  IPv4: {interface['IPv4']}")
        if 'IPv6' in interface:
            print(f"  IPv6: {interface['IPv6']}")
        print('-' * 40)

if __name__ == "__main__":
    main()
