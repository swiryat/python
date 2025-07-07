for y in range(15, -15, -1):
    line = ""
    for x in range(-30, 30):
        x_scaled = x * 0.05
        y_scaled = y * 0.1
        eq = (x_scaled**2 + y_scaled**2 - 1)**3 - x_scaled**2 * y_scaled**3
        line += "\u2665" if eq <= 0 else " "
    print(line)