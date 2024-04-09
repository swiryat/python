from cs50 import get_int

x = int(input("x: "))
y = int(input("y: "))

if x < y:
    print ("x is less than y")
elif x > y:
    print ("x is greater than y")
else:
    print("x is equal to y")

s = input('Do you agree?')

if s == 'Y' or s == 'y':
    print ('Agreat.')
elif s == 'N' or s == 'n':
    print ('Not agreed.')

s = input('Do you agree?')

if s in ['Y','y']:
    print ('Agreat.')
elif s in ['N','n']:
    print ('Not agreed.')    