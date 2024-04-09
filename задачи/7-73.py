k = 1
for i in range(5):
    print(i, end='')
    
k = 1
for i in range(5):
    print(i+k, end='')

k = 1
for i in range(5):
    print(k*k, end='')

k = 8
for i in range(5):
    print(i, end='')
    k -= 2

k = 8
for i in range(5, 0, -1):
    print(2*i-k, end='')
    k -= 2