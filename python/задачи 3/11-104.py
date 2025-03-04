def count_ways_to_make_change(total, coins):
    ways = [0] * (total + 1)
    ways[0] = 1  # Нулевая сдача можно получить одним способом - не выдавать никакие монеты.

    for coin in coins:
        for amount in range(coin, total + 1):
            ways[amount] += ways[amount - coin]

    return ways[total]

def main():
    # Предполагаем, что в наборе есть монета достоинством 1 рубль
    p1 = 1

    total_amount = int(input("Введите сумму сдачи в рублях: "))
    num_coin_values = int(input("Введите количество различных монет в наборе: "))

    coin_values = []
    for i in range(1, num_coin_values + 1):
        coin_value = int(input(f"Введите достоинство монеты {i} в рублях: "))
        coin_values.append(coin_value)

    coin_values.insert(0, p1)  # Добавляем монету достоинством 1 рубль в начало списка

    ways_count = count_ways_to_make_change(total_amount, coin_values)

    print(f"Способы размена суммы {total_amount} рублей: {ways_count}")

if __name__ == "__main__":
    main()
