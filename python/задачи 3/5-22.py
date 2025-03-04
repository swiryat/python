import random as r

player_reply = int(input('введите число: '))


def game(num):
    while player_reply != num:
        if player_reply > num:
            print('меньше!')
        elif player_reply < num:
            print('больше!')
        else:
            print('*динь-динь-динь* ВЕРНО!!!')
            break

game(r.randint(1, 101))