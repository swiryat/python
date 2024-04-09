num = int(input('введите 4хзначное число: '))
num_str = str(num)

sum_first = num_str[0] + num_str[1]
sum_middle = num_str[1] + num_str[2]
sum_end = num_str[2] + num_str[3]

result = int(sum_first) * int(sum_middle) * int(sum_end)

print('Результат работы автомата: ', result)
