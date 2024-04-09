def find_min_max_even_numbers(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            numbers = [int(line.strip()) for line in file]

        even_numbers = [num for num in numbers if num % 2 == 0 and num > 0]

        if not even_numbers:
            result = "В файле нет положительных чётных чисел."
        else:
            min_even = min(even_numbers)
            max_even = max(even_numbers)
            result = f"Минимальное чётное положительное число: {min_even}\nМаксимальное чётное положительное число: {max_even}"

        with open(output_file, 'w') as file:
            file.write(result)

        print("Результат записан в файл:", output_file)

    except FileNotFoundError:
        print("Файл не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Пример использования
input_filename = "input_numbers.txt"
output_filename = "output_result.txt"
find_min_max_even_numbers(input_filename, output_filename)
