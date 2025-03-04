# Автор: А. Харченко

from graph import *
from random import randint

"""
  Игра "Ходом коня": заполнить всю шахматную доску
  ходом коня
"""

w=40 # размер клетки
a=[] #pole  igry
N=8 # row   razmer polya
M=8 # columns
hod=1
hodM=[]

def proverka(xx,yy):
    global hod,N,M,hodM
    w=len(hodM)-1
    if hod==1: otv= True
    else:
        otv=((abs(hodM[w][0]-xx)==1 and abs(hodM[w][1]-yy)==2) or
        (abs(hodM[w][0]-xx)==2 and abs(hodM[w][1]-yy)==1)) and (xx>0)and(yy>0)and(xx<=M)and(yy<=N)
    return otv
def pole(n,m):# risuem pole
    for i in range(n+1):
        line(50,50+i*w,50+w*m,50+i*w)
    for i in range(m+1):
        line(50+i*w,50,50+i*w,50+w*n)

def mouseClick(event): # Click left mouse
    global hod,stx,sty,hodM,kk,N,M
    i2=(event.y-50)//w+1# nomer row
    j2=(event.x-50)//w+1# nomer column
    x2=(j2-1)*w+55  # rovnyi x
    y2=(i2-1)*w+55  # rovnyi y

    if a[i2][j2]==0 and proverka(i2,j2):
        a[i2][j2]=hod
        hodM.append([i2,j2])
        stx=i2 # staryi x
        sty=j2 # staryi y
        lb1["text"]="Счет: "+str(hod)
        if hod==N*M:
            lb1["text"]="Счет: "+str(hod)+" Победа!!!"
        hod+=1

    if 0<i2<11 and 0<j2<11: # vnutri polya?
        if a[i2][j2]>=0: # no mines
            label(str(a[i2][j2])+" ",x2,y2,font=("Arial Bold", 14))


def mouseClick2(event): # Click right mouse
    global kol,hodM,hod,stx,sty
    nn=len(hodM)
    #print(nn)
    if hod > 0:
        i2,j2=hodM[nn-1]
        a[i2][j2]=0
        stx,sty=hodM[nn-2]
        sty=j2
        x2=(j2-1)*w+60
        y2=(i2-1)*w+55

        hodM.pop(nn-1)
        hod-=1
        lb1["text"]="Счет: "+str(hod-1)
        label("   ",x2-1,y2,font=("Arial Bold", 14))

def start(n,m):
    global a
    a=[[0]*m for i in range(n)] # zanulyaem Matrix
    mins=0

print("Game  Step Horse 8*8. AVaHar(c) ")


start(N+2,M+2)
pole(N,M) # risuem pole
# gdem sobytiy
onMouseClick(mouseClick, 1)
onMouseClick(mouseClick2,3)
lb1=label("Счет: 0",400,50,
          font=("Arial Bold", 16))
AV=label("AVaHar (c) StepHorse",30,5,
         font=("Arial Bold", 8))
tx=label("Ходом коня, надо побывать в каждой клетке поля",
         170,5,font=("Arial Bold", 10))
tz=label("Старт в любой клетке",200,25,
         font=("Arial Bold", 10))
run()
