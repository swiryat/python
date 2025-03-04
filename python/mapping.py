# Словарь соответствий между английской и русской раскладкой клавиатуры
layout_map = {
    'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з', '[': 'х', ']': 'ъ',
    'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д', ';': 'ж', "'": 'э',
    'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь', ',': 'б', '.': 'ю', '/': '.',
    
    # Заглавные буквы
    'Q': 'Й', 'W': 'Ц', 'E': 'У', 'R': 'К', 'T': 'Е', 'Y': 'Н', 'U': 'Г', 'I': 'Ш', 'O': 'Щ', 'P': 'З', '{': 'Х', '}': 'Ъ',
    'A': 'Ф', 'S': 'Ы', 'D': 'В', 'F': 'А', 'G': 'П', 'H': 'Р', 'J': 'О', 'K': 'Л', 'L': 'Д', ':': 'Ж', '"': 'Э',
    'Z': 'Я', 'X': 'Ч', 'C': 'С', 'V': 'М', 'B': 'И', 'N': 'Т', 'M': 'Ь', '<': 'Б', '>': 'Ю', '?': ','
}

def convert_layout(text):
    """Функция перевода текста, набранного в английской раскладке, в русский"""
    return ''.join(layout_map.get(char, char) for char in text)

# Тестируем
text = "yfgbib bv? xnj z rehcsa b[ybt ghjitk yt yflj pfybvfnmcz rktdtnjq  gecnm kexit levf.n j cdjb[ htiybz[ b cdjtq jndtncxdtyyjcnb z yt gjkexbk jn yb[ jndtnf j cjke;t,yjq ytj,[jlbvjcnb gjlrk.xtybz r dcnytxfv nfr;t afrn vjtuj"
converted_text = convert_layout(text)
print(converted_text)  # Ожидаемый вывод: "наш мир"
