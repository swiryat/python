a = [[1, 2, 3], 
     [4, 5, 6], 
     [7, 8, 9]]

def printMatrix(a):
    for i in range(len(a)):
        for j in range(len(a[i])):
            print('{:4d}'.format(a[i][j]), end='')
    print()

printMatrix(a)