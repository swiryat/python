import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import time
import matplotlib.pyplot as plt
import torch.nn.functional as F

# Параметры
num_epochs = 5
batch_size = 64
learning_rate = 0.001
weight_decay = 1e-4  # L2 регуляризация

# Загрузка данных с аугментацией
transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),  # Случайное горизонтальное отражение
    transforms.RandomRotation(10),  # Случайный поворот
    transforms.ToTensor(),
])

train_dataset = datasets.MNIST(root='./data', train=True, transform=transform, download=True)
train_loader = data.DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)

val_dataset = datasets.MNIST(root='./data', train=False, transform=transform, download=True)
val_loader = data.DataLoader(dataset=val_dataset, batch_size=batch_size, shuffle=False)

# Определение модели
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)
        self.dropout = nn.Dropout(0.25)  # Dropout для регуляризации

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 64 * 7 * 7)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

# Инициализация модели, функции потерь и оптимизатора
model = SimpleCNN().cuda()  # Переносим модель на GPU
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)

# Обучение модели
train_losses = []
val_losses = []
val_accuracies = []

# Определение событий для замера времени на GPU
start_event = torch.cuda.Event(enable_timing=True)
end_event = torch.cuda.Event(enable_timing=True)

for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0

    # Начало замера времени
    torch.cuda.synchronize()  # Синхронизация перед началом замера времени
    start_event.record()      # Запись начала события на GPU

    for i, (images, labels) in enumerate(train_loader):
        images, labels = images.cuda(), labels.cuda()  # Переносим данные на GPU

        optimizer.zero_grad()  # Обнуляем градиенты
        outputs = model(images)  # Прямой проход
        loss = criterion(outputs, labels)  # Вычисляем потерю
        loss.backward()  # Обратный проход
        optimizer.step()  # Обновление параметров

        running_loss += loss.item()

    # Конец замера времени
    end_event.record()        # Запись конца события на GPU
    torch.cuda.synchronize()  # Синхронизация для завершения всех операций

    # Вычисление потерь и точности на валидационном наборе
    model.eval()
    val_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.cuda(), labels.cuda()
            outputs = model(images)
            loss = criterion(outputs, labels)
            val_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    train_loss = running_loss / len(train_loader)
    val_loss /= len(val_loader)
    val_accuracy = 100 * correct / total

    train_losses.append(train_loss)
    val_losses.append(val_loss)
    val_accuracies.append(val_accuracy)

    # Вывод информации
    elapsed_time_ms = start_event.elapsed_time(end_event)
    elapsed_time_sec = elapsed_time_ms / 1000  # Перевод в секунды
    print(f'Epoch {epoch} - Train Loss: {train_loss:.6f}, Val Loss: {val_loss:.6f}, Val Accuracy: {val_accuracy:.2f}%')
    print(f'Total training time on GPU (measured with torch.cuda.Event): {elapsed_time_sec:.2f} seconds')

# Визуализация потерь и точности
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(train_losses, label='Train Loss')
plt.plot(val_losses, label='Validation Loss')
plt.title('Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(val_accuracies, label='Validation Accuracy')
plt.title('Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy (%)')
plt.legend()

plt.tight_layout()
plt.show()

# Сохранение модели
torch.save(model.state_dict(), 'model.pth')

# Загрузка модели
model = SimpleCNN()  # Создание новой модели
model.load_state_dict(torch.load('model.pth'))  # Загрузка параметров
model.eval()  # Переводим модель в режим оценки


