"""
def hanoi(n, k, m):             # n - кол-во дисков
    if n <= 0: return
    p = 6 - k - m
    hanoi(n-1, k, p)
    print(k, '->', m)
    hanoi(n-1, p, m)

hanoi(5, 15, 1)
"""


def allwords(word, abc, K):
    if K < 1:
        print(word)
        return 1
    count = 0
    for c in abc:
        count += allwords(word + c, abc, K-1)
        return count

count = allwords('', 'АБВГДЕЁЖ', 3)
print(count)
