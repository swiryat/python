inf = 'информатика'

word1 = inf[7:10]  # "тика"
word2 = inf[3:7] + inf[7:10]  # "форматика"
word3 = inf[7] + inf[3] + inf[0] + inf[7:10]  # "тинтика"
word4 = inf[7:10] + inf[3] + inf[7]  # "тикаинт"
word5 = inf[7:10] + inf[3:5] + inf[7:10]  # "тиканика"

print(word1)
print(word2)
print(word3)
print(word4)
print(word5)
