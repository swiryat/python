import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
import time  # Для измерения времени на CPU

# Параметры
batch_size = 64
learning_rate = 0.3
epochs = 5

# Загрузка данных
train_loader = torch.utils.data.DataLoader(
    datasets.MNIST('.', train=True, download=True, transform=transforms.ToTensor()),
    batch_size=batch_size, shuffle=True
)

# Определение простой модели
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(28 * 28, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = x.view(-1, 28 * 28)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Инициализация модели
model = SimpleNN()

# Перемещение на GPU
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model.to(device)

# Оптимизатор и функция потерь
optimizer = optim.SGD(model.parameters(), lr=learning_rate)
criterion = nn.CrossEntropyLoss()

# Для измерения времени на CPU
start_time_cpu = time.time()

# Для измерения времени на GPU (если доступен)
if device == 'cuda':
    start_event = torch.cuda.Event(enable_timing=True)
    end_event = torch.cuda.Event(enable_timing=True)
    start_event.record()  # Записываем начало на GPU

# Обучение
model.train()
for epoch in range(epochs):
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)

        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        if batch_idx % 100 == 0:
            print(f"Epoch {epoch} [{batch_idx * len(data)}/{len(train_loader.dataset)}] Loss: {loss.item():.6f}")

# Для измерения времени на CPU
end_time_cpu = time.time()
elapsed_time_cpu = end_time_cpu - start_time_cpu
print(f"Total training time on {device} (CPU measurement): {elapsed_time_cpu:.2f} seconds")

# Для измерения времени на GPU
if device == 'cuda':
    end_event.record()  # Записываем окончание на GPU
    # Синхронизируем и вычисляем время
    torch.cuda.synchronize()
    elapsed_time_gpu = start_event.elapsed_time(end_event) / 1000  # Время в секундах
    print(f"Total training time on GPU (GPU measurement): {elapsed_time_gpu:.2f} seconds")
