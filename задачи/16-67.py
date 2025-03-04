num = int(input('введите число: '))

num_str = str(num)

if all(char == num_str[0] for char in num_str):
    print('да')
else:
    print('нет')
