from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import socket

# Настройка ключа и генерация случайного IV
key = b'This is a key123'  # Должен быть 16, 24 или 32 байта для AES
iv = get_random_bytes(AES.block_size)  # Генерация случайного вектора инициализации

# Создание шифратора с ключом и IV
cipher = AES.new(key, AES.MODE_CBC, iv)

# Преобразование сообщения в байты с использованием UTF-8
data = "Привет, любишь ли ты мороженное? Если да, то какое тебе купить?".encode('utf-8')

# Дополнение данных до подходящего размера для AES (например, 16 байт)
padded_data = pad(data, AES.block_size)

# Шифрование данных
encrypted_data = cipher.encrypt(padded_data)

# Отправка зашифрованных данных через сокет
server_address = ('localhost', 12346)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Отправляем сначала IV, затем зашифрованные данные
sock.sendto(iv, server_address)  # Отправляем IV как байты
sock.sendto(encrypted_data, server_address)  # Отправляем зашифрованные данные как байты
sock.close()

print("Зашифрованные данные отправлены.")
