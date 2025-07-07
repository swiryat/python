A = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

B = A[:]

print(*A)
print(*B)

A[0] = 0

print(*A)
print(*B)

X = 12       # искомый в массиве элемент
N = 13       # размер массива

i = 0
while A[i] != X:
    i += 1
if i < N:
    print('A[{}] = {}'.format(i, X))
else:
    print('Не нашли!')

