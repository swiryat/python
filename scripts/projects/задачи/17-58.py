month = int(input('введите номер месяца (1-12): '))

if 1 <= month <= 12:
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    days = days_in_month[month - 1]

    print(f'в месяце {month} {days} дней')
else:
    print('введите число от 1 до 12')
