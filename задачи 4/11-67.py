def convert_nautical_miles_to_kilometers(nautical_miles):
    # 1 морская миля = 1.852 километра
    kilometers = nautical_miles * 1.852
    return kilometers

def main():
    print("Программа для перевода морских миль в километры.")
    
    try:
        # Ввод количества морских миль
        nautical_miles = float(input("Введите количество морских миль: "))
        
        # Перевод в километры
        kilometers = convert_nautical_miles_to_kilometers(nautical_miles)
        
        # Вывод результата
        print(f"{nautical_miles} морских миль равно {kilometers:.2f} километров.")
    
    except ValueError:
        print("Ошибка: Введите числовое значение для морских миль.")

if __name__ == "__main__":
    main()
