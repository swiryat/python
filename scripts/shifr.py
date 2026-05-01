from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES


# Генерация случайного ключа и IV
key = get_random_bytes(16)  # 128-битный ключ для AES
iv = get_random_bytes(16)  # 128-битный IV

# Данные для шифрования
data = "Это секретные данные, которые нужно зашифровать.".encode('utf-8')  # Перекодируем в байты

# Шифрование
cipher = AES.new(key, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(pad(data, AES.block_size))

# Дешифрование
decipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = unpad(decipher.decrypt(ciphertext), AES.block_size)

# Вывод результатов
print(f"Зашифрованные данные: {ciphertext.hex()}")
print(f"Расшифрованные данные: {plaintext.decode('utf-8')}")
