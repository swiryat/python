from sys import argv

#if len(argv) == 2:
    #print(f"helo, {argv[1]}")
#else:
    #print("helo, world")   
#for i in range(len(argv)):
for arg in argv[1:]:
    print(arg) 