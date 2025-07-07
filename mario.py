""" 
from cs50 import get_int

def main():
    height = get_height()
    for i in range(height):
        print('#')
def get_height():
    while True:
        try:
        n = get_int('Height:')
        if n > 0:
            return n
        exept ValueError:
    print('Not an integer')            
main() 
"""

#while True:
    #n = get_int("Height: ")
    #if n >0:
        #break
#for i in range(n):
    #print("#")


"""
from cs50 import get_int
def main():
    height = get_height()
    for i in range(1, height + 1):
        # Печатаем пробелы перед символами '#'
        print(' ' * (height - i) + '#' * i)

def get_height():
    while True:
        n = get_int('Высота: ')
        if n > 0 and n <= 8:  # Вы можете настроить максимальную высоту по вашему усмотрению
            return n

if __name__ == "__main__":
    main()
"""
"""
for i in range(3):
    print ('?', end='')
    print ('?', end='!')    
print()
print('?'*5)
print('!'*5)
"""
for i in range(3):
    #for j in range(3):
        #print('#')
        #print('#', end='')
    print('#'*3)    
