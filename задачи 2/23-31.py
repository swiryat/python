def isByte(num):
    if 0 <= num <= 255:
        return True
    else:
        return False

print(isByte(int(input())))