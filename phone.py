import csv

#file = open("phone.csv", "a")
with open('phone.csv', 'a') as file:

    name = input("Name: ")
    number = input("Number: ")

    #writer = csv.writer(file)
    writer = csv.DictWriter(file, fieldnames=['name','number'])
    #writer.writerow([name, number])
    writer.writerow({"name":name, "number": number})


file.close()
