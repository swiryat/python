from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import socket

# Настройка сокета для получения данных
server_address = ('localhost', 12346)  # Адрес и порт получателя
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(server_address)  # Привязываем сокет к порту для прослушивания входящих данных

# Ожидаем, что данные будут приходить частями
print("Ожидание зашифрованного сообщения...")

# Чтение данных по частям
data_received = b""

# Получение IV (первые 16 байт)
iv, address = sock.recvfrom(16)  # Получаем 16 байт для IV
data_received += iv

# Получение зашифрованных данных (остаток сообщения)
ciphertext, address = sock.recvfrom(4096)  # Получаем зашифрованные данные, можно увеличить размер
data_received += ciphertext

# Разделение данных
iv = data_received[:16]
ciphertext = data_received[16:]

# Получение ключа
key = b'This is a key123'  # Ключ должен быть таким же, как у отправителя

# Дешифрование
cipher = AES.new(key, AES.MODE_CBC, iv)

try:
    # Расшифровка данных
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    print(f"Расшифрованное сообщение: {plaintext.decode()}")
except ValueError:
    print("Ошибка при расшифровке: некорректное дополнение")

sock.close()
