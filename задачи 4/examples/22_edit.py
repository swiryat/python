# coding: utf-8
"""
Использование графического модуля graph.py.
GR_EDIT - редактор текста
  (C) К. Поляков, 2017-2021
  e-mail: kpolyakov@mail.ru
  web: http://kpolyakov.spb.ru
"""
from graph import *

def update():
  lbl['text'] = edt.text.get()

def keyPressed(event):
  if event.keycode == VK_ESCAPE:
    close()

brushColor("blue")
rectangle(0, 0, 400, 400)
x = 100
y = 100
lbl = label( "???", x, y )

xe = 50
ye = 370
lblEdt = label( "Имя", 10, ye, fg="white", bg="blue",
                font=("Arial", 12)  )
edt = edit( "Вася", xe, ye, font=("Arial", 12)  )
print( edt.text )

onKey(keyPressed)
onTimer(update, 50)

run()