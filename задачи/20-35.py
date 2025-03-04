rub, cop = map(int, input('Введите цену одного пирожка (рубли, копейки): ').split())
count = int(input('Введите количество пирожков: '))

total_price_cop = (rub * 100 + cop) * count

total_rub = total_price_cop // 100
total_cop = total_price_cop % 100

print(f'Общая стоимость: {total_rub} рублей и {total_cop} копеек')
