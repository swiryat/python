def digit(num):
    for i in range(1, num + 1):
        if num % i == 0:
            print(i)

digit(228)