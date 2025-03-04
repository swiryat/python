import random

# Создайте список возможных направлений
directions = ["вверх", "вниз", "влево", "вправо"]

while True:
    random_direction = random.choice(directions)
    print("Метеорит движется", random_direction)
    input()
