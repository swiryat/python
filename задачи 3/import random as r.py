import random as r

a = []

for i in range(r.randint(1, 20)):
    a.append(r.randint(1, 25))

print('массив: ', a)

n = len(a)
for i in range(n - 1):
    for j in range(n-2, i-1, -1):
        if a[j] > a[j+1]:
            a[j], a[j+1] = a[j+1], a[j]     # меняем местами

print('отсортированный массив: ', a)

unique_numbers = set(a)
count_unique_numbers = len(unique_numbers)

print('количество различных чисел: ', len(unique_numbers))