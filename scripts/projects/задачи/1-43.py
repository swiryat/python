import random

a = int(input('a = '))
b = int(input('b (b > a) = '))

for i in range(5):
    random_number = random.randint(a, b)
    print(random_number)
    
