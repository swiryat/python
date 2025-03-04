def replace_word(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            text = file.read()

        replaced_text = text.replace("паровоз", "поезд")

        with open(output_file, 'w') as file:
            file.write(replaced_text)

        print("Текст успешно изменен и записан в файл:", output_file)

    except FileNotFoundError:
        print("Файл не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Пример использования
input_filename = "parovoz.txt"
output_filename = "poezd.txt"
replace_word(input_filename, output_filename)
