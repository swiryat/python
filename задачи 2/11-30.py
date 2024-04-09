def isEven(a):
    return (a % 2 == 0)

a = 63

while isEven(a) and a > 5:
    a = a // 2
    print(a)
