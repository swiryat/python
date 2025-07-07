"""
# Считываем имя пользователя
username = input()
# Выводим приветствие
print("Hello, " + username)



name = input()
print(f'Hello, {name}')


city = input ()
time = input ()
print(f"Current location is {city} and time is {time}")

fruits = {'apple', 'banana', 'cherry'}
fruits.add('orange') 
print(fruits)
"""

"""
from re import I


a = 4
b = 8
flag = True
flag2 = False

print(flag)

c = a > b
print(c)

print(a == 4)
print(a != 4)
print(a < b)
print(a <= b)
print(a > b)
print(a >= b)
print(flag == flag2)

print(not flag)
print(not flag2)
print(flag and flag2)
print(flag or flag2)
print(not flag and flag2)
print(not (a < b))
print(a > b and a < b)
print(a < b or a > b)
print(a < b and a > 2)
print(not (a < b and a > 2))
print(not (a < b) or a > 2)
print(a < b and not (a > 2))
print(a < b or not (a > 2))
print(not (a < b) and not (a > 2))
print(not (a < b) or not (a > 2))
print(a < b and not (a > 2) and a < b)
print(a < b or not (a > 2) or a < b)
print(a < b and a > 2)
print(a < b or a > 2)
print(a < b and a > 2 and a < b)
print(a < b or a > 2 or a < b)
print(a < b and a > 2 or a < b)
print(a < b or a > 2 and a < b)
print(a < b and a > 2 and a < b and a > 2)
print(a < b or a > 2 or a < b or a > 2)
print(a < b and a > 2 or a < b and a > 2)
print(a < b or a > 2 and a < b or a > 2)
print(a < b and a > 2 and a < b and a > 2 or a < b or a > 2)
print(a < b or a > 2 or a < b and a > 2 or a < b or a > 2)
print(a < b and a > 2 and a < b or a > 2 and a < b or a > 2)
print(a < b or a > 2 or a < b and a > 2 or a < b or a > 2)
print(a != b or a < 2)
print(a != b and a < 2)
print(a != b or a < 2 or a > 2)
print(a != b and a < 2 and a > 2)
print(a != b or a < 2 and a > 2)
print(a != b and a < 2 or a > 2)
print(a != b or a < 2 or a > 2 and a < b)
print(a == b or a < b)
print(a < b or a == b)
print(a == b and a < b)
print(a < b and a == b)
print(a < b or ((not (a == b)) and a > 0))

# Вариант исправления сравнения:
c = a > 0 or b > 10
c = a > 0 and b > 10
c = not (a > 0) and b > 10
c = not (a > 0) or b > 10
c = a > 0 and not (b > 10)
c = a > 0 or not (b > 10)
c = not (a > 0) and not (b > 10)
c = a < 0 and b != 1

# Исправленные условные выражения:
if a < 20 and b > -1:
    print('a < 20 and b > -1')

if a < 20 or b > -1:
    print('a < 20 or b > -1')

if 0 <= a < 20:
    print("0 <= a < 20")
    c = a if a > b else b
    print(c)
else:
    print("0 <= a < 20 or b > -1")

if a < 20:
    if b > -1:
        print("a < 20 and b > -1")
    else:
        print("a < 20 and b < -1")



for i in range(1, 10, 2):
    print(i)
    #print(i * i)
    #print(i * i - i)
    #print(i * i / i % i)
print('end')  

for i in 'abc123':
    print(i)
    #print(i * i)
    #print(i * i - i)
    #print(i * i / i % i)
print('end')        

for i in range(10):
    if i == 4:
        continue
    print(i)
print('end')  

for i in range(10):
    if i == 4:
        break
    print(i)
print('end')  



a = 0
while a < 10:
    print(a)
    a += 1
    if a > 4:
        break
    print('end')
print('end2')  

print(bool(""), bool("0"), bool("0.0"), bool("0.00"), bool("0.000"), bool("0.0000"), bool("0.00000"))
print(bool(""), bool("ABC"), bool("123"), bool("123.456"), bool("123.456789"))

data = input()
while data!= 'exit':
    print(data)
    data = input()

data = input()
while data:
    print("Enterend" , data)
    data = input()   
    
"""




while data := input():
    print("Enterend:", data)
    
data = input()
while data:
    print("Entered:", data)
    data = input()
    