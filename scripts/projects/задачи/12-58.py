while True:
    num = int(input('введите целое трёхзначное число: '))

    if 100 < num < 999:
        str_num = str(num)

        str_one = str_num[0]
        str_two = str_num[1]
        str_three = str_num[2]

        one = int(str_one)
        two = int(str_two)
        three = int(str_three)

        if one == two or two == three or one == three:
             print('да')
        else:
            print('нет')
