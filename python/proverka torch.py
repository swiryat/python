import torch

# Проверка версии PyTorch
print("PyTorch version:", torch.__version__)

# Проверка доступности CUDA
cuda_available = torch.cuda.is_available()
print("CUDA available:", cuda_available)

# Если CUDA доступен, выведите информацию о GPU
if cuda_available:
    print("GPU Name:", torch.cuda.get_device_name(0))

# Простая проверка работы на GPU или CPU
device = torch.device("cuda" if cuda_available else "cpu")
tensor = torch.tensor([1.0, 2.0, 3.0], device=device)
print("Tensor on device:", tensor)
