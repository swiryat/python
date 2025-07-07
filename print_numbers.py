def print_numbers(last_number):
    i = 1
    while i >= last_number:
        print(i)
        i = i - 1
    print('finished!')

print_numbers(4)

def print_numbers(last_number):
    i = last_number
    while i >= 1:
        print(i)
        i -= 1
    print('finished!')

print_numbers(4)
