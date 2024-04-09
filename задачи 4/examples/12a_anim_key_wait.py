# coding: utf-8
"""
Использование графического модуля graph.py.
GR_ANIM_KEY_WAIT - анимация с управлением клавишами-стрелками
      (с ожиданием нажатия на клавишу)
      когда желтый квадрат соприкасается с красным, красный исчезает
  (C) К. Поляков, 2017-2022
  e-mail: kpolyakov@mail.ru
  web: http://kpolyakov.spb.ru
"""
from graph import *

def keyPressed(event):
  if event.keycode == VK_LEFT:
    moveObjectBy(obj, -5, 0)
  elif event.keycode == VK_RIGHT:
    moveObjectBy(obj, 5, 0)
  elif event.keycode == VK_UP:
    moveObjectBy(obj, 0, -5)
  elif event.keycode == VK_DOWN:
    moveObjectBy(obj, 0, 5)
  elif event.keycode == VK_ESCAPE:
    close()
  for t in targets:
    if overlap(obj, t):
       deleteObject( t )
       targets.remove( t )
  if overlapRect(obj, 200, 200, 400, 400):
    changeFillColor(obj, "maroon")
  else:
    changeFillColor(obj, "yellow")

brushColor("blue")
rectangle(0, 0, 400, 400)
brushColor("green")
rectangle(200, 200, 400, 400)

from random import randint
penColor("red")
brushColor("red")
targets = []
for i in range(10):
  x = randint(5, 375)
  y = randint(5, 375)
  targets.append( rectangle(x, y, x+20, y+20) )

x = 100
y = 100
penColor("yellow")
brushColor("yellow")
obj = rectangle(x, y, x+20, y+20)

onKey(keyPressed)

run()