import xml.etree.ElementTree as ET
import pandas as pd

# Загрузка XML (например, из файла или как строка)
xml_data = '''<root>
    <Devices>
        <Device>
            <Measurements>
                <Measurement>
                    <Signals>
                        <Signal id="ref-1">
                            <XValue>-409|-408|-407|-406|-405|7779|7780|7781|7782</XValue>
                            <YValue>-10|-10|-10|-10|-10|-10|-10|-10</YValue>
                        </Signal>
                    </Signals>
                </Measurement>
            </Measurements>
        </Device>
    </Devices>
</root>'''

# Парсинг XML
root = ET.fromstring(xml_data)

# Извлечение сигналов
signals = []
for signal in root.findall('.//Signal'):
    # Извлечение XValue и YValue
    x_values_str = signal.find('XValue').text
    y_values_str = signal.find('YValue').text
    
    # Вывод значений для отладки
    print(f"XValue: '{x_values_str}', YValue: '{y_values_str}'")
    
    # Обработка значений X
    x_values = [int(val) for val in x_values_str.split('|')]
    
    # Обработка значений Y
    y_values = []
    for val in y_values_str.split('|'):
        try:
            y_values.append(int(val))  # Пробуем преобразовать все значения в int
        except ValueError:
            print(f"Не удалось преобразовать значение Y: '{val}'")
    
    # Проверка на совпадение длин
    if len(x_values) != len(y_values):
        print(f"Несоответствие в длине списков: X ({len(x_values)}) и Y ({len(y_values)})")
        continue  # Пропускаем эту запись, если длины не совпадают

    # Вывод значений для отладки
    print(f"X Values: {x_values}, Y Values: {y_values}")
    
    # Добавление в signals
    for x, y in zip(x_values, y_values):
        signals.append({'X': x, 'Y': y})

# Создание DataFrame, если есть собранные данные
if signals:
    df = pd.DataFrame(signals)
    print(df)
else:
    print("Нет доступных сигналов для анализа.")
