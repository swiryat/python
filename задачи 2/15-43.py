def full_name(name):
    parts = name.split(' ')
    
    if len(parts) != 3:
        return "Ошибка: Введите три слова (Фамилия Имя Отчество)"
    
    f, i, o = map(str, parts)
    return i[0] + '. ' + o[0] + '. ' + f

user_input = input('Введите ФИО: ')
print(full_name(user_input))
