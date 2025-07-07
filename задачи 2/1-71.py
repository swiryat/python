<<<<<<< HEAD
import random

x = int(input('введите значение x (от 0 до 4) '))
a = []

array_size = 25
a = [random.randint(0, 5) for _ in range(array_size)]

for index, value in enumerate(a):
    if value == x:
=======
import random

x = int(input('введите значение x (от 0 до 4) '))
a = []

array_size = 25
a = [random.randint(0, 5) for _ in range(array_size)]

for index, value in enumerate(a):
    if value == x:
>>>>>>> origin/master
        print(f"Элемент {x} найден на позиции {index}")