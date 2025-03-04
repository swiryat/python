"""Консольная утилита для конвертации валют.

Author: Andrei Karelin.

Программа является домашним заданием по курсу "Подготовительный курс по Python" от Хекслет.

Алгоритм работы программы:
1. Вывод приветствия.
2. Вывод правила использования.
3. Вывод списка валют.
4. Выбор имеющейся валюты.
5. Количество имеющейся валюты.
6. Выбор валюты конвертации.
7. Вывод результата.
"""

import logging
import re
import requests
from os import environ
from requests.structures import CaseInsensitiveDict


class CurrencyConverter:
    """Класс для конвертации валют."""

    # TODO: Вынести во внешний источник.
    config = {
        'log_level': logging.INFO,
        'currency_api_url': 'https://api.freecurrencyapi.com/v1/latest',
        'supported_currencies': ['CNY', 'EUR', 'GBP', 'JPY', 'USD'],
        'base_currency': 'USD',
        'lang': 'ru'
    }

    # TODO: Вынести во внешний источник, добавить другие языки.
    messages = {
        'ru': {
            'hello': 'Добро пожаловать в конвертор валют!',
            'rules': '\n'.join([
                'Данная программа поможет вам конвертировать вашу валюту в желаемую.',
                '- выбор исходной валюты;',
                '- ввод количества этой валюты;',
                '- выбор валюты конвертации.'
            ]),
            'current_currency': 'Введите имеющийся валюту (цифру или название)',
            'current_amount': 'Введите имеющуюся сумму',
            'conversion_currency': 'Выберите валюту для конвертации',
            'result': 'ИТОГО',
            'error_values': 'ОШИБКА: Введены неправильные параметры.',
            'error_unrealized': 'Непредвиденная ошибка в программе. Пожалуйста, сообщите о ней разработчикам.'
        }
    }

    def __init__(self):
        logging.basicConfig(
            level=self.config['log_level'],
            filename='app.log',
            filemode='w',
            format='%(asctime)s %(levelname)s %(message)s'
        )
        self.CURRENCIES = self.get_online_currencies()
        logging.info(self.CURRENCIES)

    def run(self) -> None:
        """Точка входа в программу."""
        print('=' * 20)
        # 1. Вывод приветствия.
        self.print_message('hello')
        # 2. Вывод правила использования.
        self.print_message('rules')
        # 3. Вывод списка валют.
        print()
        for i in self.CURRENCIES:
            print(f'{i["id"]}) {i["name"]} ({i["exchange_rates"]:.2f})')
        print()
        try:
            # 4. Выбор имеющейся валюты.
            current_currency = self.normalize_currency(
                self.input_message('current_currency')
            )
            # 5. Количество имеющейся валюты.
            current_amount = self.input_message('current_amount', 'float')
            # 6. Выбор валюты конвертации.
            conversion_currency = self.normalize_currency(
                self.input_message('conversion_currency')
            )
            # 7. Вывод результата.
            result = self.do_conversion(current_currency, conversion_currency, current_amount)
            self.print_message('result', ': ', round(result, 2), '.')
        except ValueError as err:
            self.print_message('error_values')
        except Exception as err:
            logging.error(err)
            self.print_message('error_unrealized')

    def do_conversion(self, current_currency: str,
                conversion_currency: str, current_amount: int
            ) -> float:
        """Производит конвертацию между валютами.

        Args:
            current_currency (str): Текущая выбранная валюта.
            conversion_currency (str): Текущая валюта конвертации.
            current_amount (int): Количество имеющейся валюты.

        Returns:
            float: Результат конвертации валют.
        """
        if current_currency['exchange_rates'] == conversion_currency['exchange_rates']:
            return current_amount
        result = 0
        # Если текущая валюта не является базовой, то делаем конвертацию через нее.
        if current_currency['name'] != self.config['base_currency']:
            for i in self.CURRENCIES:
                if i['name'] == self.config['base_currency']:
                    base_currency = i
                    break
            count_base_currency = (base_currency['exchange_rates'] / current_currency['exchange_rates'])
        else:
            count_base_currency = current_currency['exchange_rates']
        return count_base_currency * conversion_currency['exchange_rates'] * current_amount

    def normalize_currency(self, currency: int|str) -> dict:
        """Возвращает нормализованный идентификатор валюты.

        Args:
            currency (int | str): Идентификатор или название валюты.

        Returns:
            dict: Объект настроек для выбранной валюты.
        """
        normalized_currency = re.sub(r'[^\d\w]+', '', currency)
        normalized_currency = normalized_currency.upper()
        key = 'id' if normalized_currency.isdigit() else 'name'
        for i in self.CURRENCIES:
            if str(i[key]) == normalized_currency:
                return i
        self.clear_and_abort(ValueError, 'Currency error: {currency}.')

    def print_message(self, message_name: str, *strings: str|None) -> None:
        """Печатает в консоль сообщение на языке пользователя.

        Args:
            message_name (str): Имя сообщения в объекте языковых настроек пользователя.
        """
        message = self.messages[self.config['lang']][message_name]
        if strings is not None:
            for i in strings:
                message += str(i)
        print(message)

    def input_message(self, message_name: str, type_name: str='str') -> int|float|str:
        """Читает ввод из консоли, приводит его к нужному типу
            и выводит в консоль сообщение на языке пользователя.

        Args:
            message_name (str): Имя сообщения в объекте языковых настроек пользователя.
            type_name (str, optional): Ожидаемый тип возвращаемых данных. По умолчанию 'str'.

        Returns:
            int|float|str: Данные, введенные пользователем.
        """
        result = input(self.messages[self.config['lang']][message_name] + ': ')
        if type_name == 'int':
            return int(result)
        elif type_name == 'float':
            return float(result)
        return result

    def get_online_currencies(self) -> list:
        """Получает актуальные курсы валют из API вендора.

        Returns:
            list: Список с настройками валют.
        """
        url = self.config['currency_api_url']
        headers = CaseInsensitiveDict()
        headers["apikey"] = environ['CURRENCY_API_TOKEN']
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            currencies = response.json().get('data')
            result = []
            index = 2
            for currency in currencies.keys():
                if currency == self.config['base_currency']:
                    result.insert(0, {
                        'id': 1,
                        'name': currency,
                        'exchange_rates': currencies[currency]
                    })
                elif currency in self.config['supported_currencies']:
                    result.append({
                        'id': index,
                        'name': currency,
                        'exchange_rates': currencies[currency]
                    })
                    index += 1
            return result
        response.raise_for_status()

    def clear_and_abort(self, exception_object: Exception, message: str|None=None) -> None:
        """Завершает программу с ошибкой.

        Args:
            exception_object (Exception): Объект исключения Python.
            message (str | None, optional): Описание ошибки. По умолчанию None.

        Raises:
            exception_object: Выбрасывает исключение переданного типа.
        """
        logging.error(message)
        raise exception_object(message or None)


if __name__ == "__main__":
    CurrencyConverter().run()
