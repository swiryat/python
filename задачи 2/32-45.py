def file (file_name, file_end):
    the_file = file_name.split('.')
    the_file[1] = file_end
    return '.'.join(the_file)

print(file(input('имя файла - '), input('расширение - ')))