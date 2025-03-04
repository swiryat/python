import torch

# Создаем тензор на CPU
x_cpu = torch.randn(3, 3)

# Перемещаем тензор на GPU
if torch.cuda.is_available():
    x_gpu = x_cpu.to('cuda')
    print("Tensor on GPU:", x_gpu)
