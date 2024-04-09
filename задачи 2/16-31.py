def numberOfDivisors():
    n = int(input())
    nums = []
    for i in range(1, n + 1):
        if n % i == 0:
            nums.append(i)
    print(len(nums))

numberOfDivisors()