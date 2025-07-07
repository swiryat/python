# Настройки
width, height = 80, 24
re_start, re_end = -2.0, 1.0
im_start, im_end = -1.0, 1.0

# Рисуем фрактал
for iy in range(height):
    line = ""
    c_im = im_start + (iy / (height - 1)) * (im_end - im_start)
    for ix in range(width):
        c_re = re_start + (ix / (width - 1)) * (re_end - re_start)
        z_re, z_im = 0.0, 0.0
        is_inside = True
        for _ in range(30):
            z_re, z_im = z_re*z_re - z_im*z_im + c_re, 2*z_re*z_im + c_im
            if z_re*z_re + z_im*z_im > 4.0:
                is_inside = False
                break
        line += "\u2665" if is_inside else " "
    print(line)
