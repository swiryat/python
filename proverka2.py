import torch

# Проверка доступности CUDA
print("CUDA доступен:", torch.cuda.is_available())

# Получение имени GPU (если доступен)
if torch.cuda.is_available():
    print("Имя GPU:", torch.cuda.get_device_name(0))
