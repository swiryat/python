<<<<<<< HEAD
def full_name(name):
    f, i, o = map(str, name.split(' '))
    return i[0] + '. ' + o[0] + '. ' + f

=======
def full_name(name):
    f, i, o = map(str, name.split(' '))
    return i[0] + '. ' + o[0] + '. ' + f

>>>>>>> origin/master
print(full_name(input('Введите ФИО: ')))