a = [30, 5, 16, 87, 45, 0, 48, -1466]
n = len(a)

for i in range(n-1):
    for j in range(n-2, i-1, -1):
        if a[j] > a[j+1]:
            a[j], a[j+1] = a[j+1], a[j]

print(*a)