def squard(w, h):
    print('.' * w)
    for _ in range(h - 2):
        print("." + " " * (w - 2) + ".")
    if h > 1:
        print('.' * w)

squard(10, 10)