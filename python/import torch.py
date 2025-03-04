import torch

# Проверяем, доступна ли CUDA
if torch.cuda.is_available():
    print("CUDA is available")
    print(f"Number of GPU(s): {torch.cuda.device_count()}")
    print(f"Device Name: {torch.cuda.get_device_name(0)}")
else:
    print("CUDA is not available")

# Проверяем работу с тензорами
x = torch.rand(5, 3)
print(f"Torch Tensor: \n{x}")
