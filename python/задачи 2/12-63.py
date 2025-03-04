import random

array_size = 15
a = [random.randint(1, 100) for _ in range(array_size)]
sr_ar = []
sr_ar_50 = []

for i in a:
    if i < 50:
        sr_ar_50.append(i)
    elif i >= 50:
        sr_ar.append(i)

total_sum_one = sum(sr_ar)
length_one = len(sr_ar)
average1 = total_sum_one / length_one

total_sum_two = sum(sr_ar_50)
length_two = len(sr_ar_50)
average2 = total_sum_two / length_two

print(f'средние арифметические: {average1} (больше/равно нуля) и {average2} (меньше нуля)')