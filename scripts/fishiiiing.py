import random as r
import time

def fishing(total_catch):
    rain = bool(r.randint(0, 1))
    answer = input('забросить удочку? (да/нет) ')
    while answer != 'да' and answer != 'нет':
        print('пожалуйста, введите либо "да", либо "нет".')
        answer = input('забросить удочку? (да/нет) ')
    
    if answer == 'нет':
        print('может быть, в следующий раз!')
        input()
    elif answer == 'да':
        if rain == True:
            time.sleep(1)
            print('пошёл дождь. шансы на хороший улов увеличены!')
            catch = r.randrange(2, 4)
            fishing_range = r.randrange(-5, 5)
            if -2 < fishing_range < 2:
               catch = r.randrange(2, 5)
               time.sleep(1)
               print(f'вы забросили удочку на дальность {fishing_range}...')
               time.sleep(r.randint(2, 6))
               print(f'вы поймали {catch} рыб(ы)!')
               total_catch += catch
            else:
               time.sleep(1)
               print(f'вы забросили удочку на дальность {fishing_range}...')
               time.sleep(r.randint(2, 6))
               print(f'вы поймали {catch} рыб(ы)!')
               total_catch += catch
        else:
            time.sleep(1)
            print('дождя нет. шансы на хороший улов снижены...')
            catch = r.randrange(0, 3)
            fishing_range = r.randrange(-5, 5)
            if -1 < fishing_range < 1:
                catch = r.randrange(1, 3)
                time.sleep(1)
                print(f'вы забросили удочку на дальность {fishing_range}...')
                time.sleep(r.randint(2, 6))
                print(f'вы поймали {catch} рыб(ы)!')
                total_catch += catch
            else:
                time.sleep(1)
                print(f'вы забросили удочку на дальность {fishing_range}...')
                time.sleep(r.randint(2, 6))
                print(f'вы поймали {catch} рыб(ы)!')
                total_catch += catch
    
        another_try = input('вы хотите попробовать снова? (да/нет) ' )
        while another_try != 'да' and another_try != 'нет':
            print('пожалуйста, введите либо "да", либо "нет".')
            another_try = input('вы хотите попробовать снова? (да/нет) ' )
    
        if another_try == 'нет':
            print(f'ваш итоговый улов: {total_catch}')
            input()
        elif another_try == 'да':
            fishing(total_catch)

fishing(0)
