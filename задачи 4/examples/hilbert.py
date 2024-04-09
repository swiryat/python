# Автор: А. Харченко

from graph import *

"""
  Кривая Гильберта
"""

u = 10 # шаг
# эта программа в цвете показывает
# последовательность рекурсивных вызовов

def a(i):
    global penX, penY
    if i > 0:
        d(i - 1)
        penX += u
        penColor("red")
        lineTo(penX, penY)
        a(i - 1)
        penY += u
        penColor("red")
        lineTo(penX, penY)
        a(i - 1)
        penX -= u
        penColor("red")
        lineTo(penX, penY)
        c(i - 1)
def b(i):
    global penX, penY
    if i>0:
        c(i-1)
        penX -= u
        penColor("blue")
        lineTo(penX, penY)
        b(i - 1)
        penY -= u
        penColor("blue")
        lineTo(penX, penY)
        b(i - 1)
        penX += u
        penColor("blue")
        lineTo(penX, penY)
        d(i - 1)
def c(i):
    global penX, penY
    if i > 0:
        b(i - 1)
        penY -= u
        penColor("green")
        lineTo(penX, penY)
        c(i - 1)
        penX -= u
        penColor("green")
        lineTo(penX, penY)
        c(i - 1)
        penY += u
        penColor("green")
        lineTo(penX, penY)
        a(i - 1)
def d(i):
    global penX, penY
    if i > 0:
        a(i - 1)
        penY += u
        penColor("purple")
        lineTo(penX, penY)
        d(i - 1)
        penX += u
        penColor("purple")
        lineTo(penX, penY)
        d(i - 1)
        penY -= u
        penColor("purple")
        lineTo(penX, penY)
        b(i - 1)


moveTo(40, 40)
penX = 50
penY = 40
moveTo(penX, penY)

a(1)
tx = label("Кривая 1 порядка", 80, 30,
         font=("Arial Bold", 10))

penY += 30
moveTo(penX, penY)
a(2)
tx = label("Кривая 2 порядка", 100, 70,
         font=("Arial Bold", 10))

penY += 30
moveTo(penX, penY)
a(3)
tx = label("Кривая 3 порядка",140,130,
           font=("Arial Bold", 10))

penY += 40
moveTo(penX, penY)
a(5)
tx=label("Кривая 5 порядка", 90, 220,
         font=("Arial Bold", 10))

penY -= 500
penX += 240
moveTo(penX, penY)
a(4)
tx=label("Кривая 4 порядка",300,30,
         font=("Arial Bold", 10))

run()