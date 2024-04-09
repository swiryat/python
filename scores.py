#scores = [2,3,4,5]

#average = sum(scores) / len(scores)
#print(f'Average: {average}')

"""
from cs50 import get_int
scores = []
for i in range (3):
    score = get_int('Score:')
    #scores.append(score)
    score += [score]
average = sum(scores) / len(scores)
print(f'Average: {average}')    
""" 

from cs50 import get_string

answer = get_string('What`s youre name?')
print(f'hello,{answer}')   