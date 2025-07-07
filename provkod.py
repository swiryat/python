import ast
import astor
import autopep8
import black
import subprocess
import logging
import pylint.lint
from pylint.reporters.text import TextReporter
from io import StringIO  # Добавляем импорт для StringIO

# Настройка логирования
logging.basicConfig(filename='code_formatter.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_code(code):
    # Используем инструмент pycodestyle (также известный как pep8) для проверки соответствия PEP 8
    process = subprocess.Popen(['pycodestyle', '--first', '--ignore=E,W', '--max-line-length=88', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate(code.encode())
    return process.returncode, stdout, stderr

def check_with_pyflakes(code):
    try:
        # Попытка анализа кода
        parsed_code = ast.parse(code)
    except SyntaxError as e:
        error_message = f"Ошибка синтаксиса: {e}"
        logging.error(error_message)
        return error_message

    return None

def check_and_fix_code(code):
    try:
        # Попытка анализа кода
        parsed_code = ast.parse(code)
    except SyntaxError as e:
        error_message = f"Ошибка синтаксиса: {e}"
        logging.error(error_message)
        return error_message

    # Преобразование обратно в строку (может изменить форматирование)
    formatted_code = astor.to_source(parsed_code)

    # Валидация кода перед форматированием (проверка PEP 8)
    validation_result, validation_output, _ = validate_code(formatted_code)

    if validation_result != 0:
        warning_message = f"Предупреждение: Код не соответствует PEP 8:\n{validation_output.decode()}"
        logging.warning(warning_message)

    # Проверка кода с использованием pyflakes
    pyflakes_result = check_with_pyflakes(code)

    if pyflakes_result:
        return pyflakes_result

    # Форматирование кода с использованием autopep8
    formatted_code = autopep8.fix_code(formatted_code)

    # Форматирование кода с использованием black с дополнительными опциями
    try:
        black_mode = black.FileMode(
            line_length=88,  # Максимальная длина строки
            target_versions={black.TargetVersion.PY37},  # Версия Python, совместимая с кодом
            is_pyi=False,  # True, если это файл pyi (типовой аннотации)
            string_normalization=True,  # Нормализация строковых литералов
        )
        formatted_code = black.format_str(formatted_code, mode=black_mode)
    except black.InvalidInput:
        info_message = "Black не может применить форматирование. Хотите продолжить с autopep8? (да/нет): "
        logging.info(info_message)
        return info_message

    return formatted_code

def main():
    # Введите код для проверки и исправления
    user_input = input("Введите код для проверки и исправления:\n")
    logging.info(f"Введенный код:\n{user_input}")

    # Сохраните оригинальный код
    original_code = user_input

    # Примените форматирование
    fixed_code = check_and_fix_code(user_input)

    if isinstance(fixed_code, str):
        print("Исправленный код:")
        print(fixed_code)
        logging.info("Исправленный код:\n" + fixed_code)
    else:
        choice = input(fixed_code)
        if choice.strip().lower() == "да":
            # Продолжить с autopep8
            fixed_code_autopep8 = autopep8.fix_code(original_code)
            print("Исправленный код с использованием autopep8:")
            print(fixed_code_autopep8)
            logging.info("Исправленный код с использованием autopep8:\n" + fixed_code_autopep8)
        else:
            print("Код без изменений:")
            print(original_code)
            logging.info("Код без изменений:\n" + original_code)

if __name__ == "__main__":
    main()
