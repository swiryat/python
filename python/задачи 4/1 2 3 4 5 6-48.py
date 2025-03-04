from graph import *
from random import randint
import math

screen_width = 600
screen_height = 400
fps = 20
update_period = round(1000 / fps)

class TGameObject:
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        if not hasattr(self, "update"):
            raise NotImplementedError(
                "Нельзя создать такой объект!")

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        self._x = value
    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        self._y = value
    @property
    def width(self):
        return self._width
    @property
    def height(self):
        return self._height
    @height.setter
    def height(self, value):
        self._height = value

class TMovingObject(TGameObject):
    def __init__(self, x, y, width, height,
                 v, course):
        TGameObject.__init__(self, x, y, width, height)
        self.v = v
        self.course = course
    def move(self):
        dx = self.v*math.cos(self.course)
        dy = -self.v*math.sin(self.course)
        self.x += dx
        self.y += dy
        moveObjectBy(self.image, dx, dy)

class TBlackHole(TGameObject):
    def __init__(self, xCenter, yCenter, radius):
        TGameObject.__init__(self, xCenter, yCenter,
                             2*radius, 2*radius)
        self.brushColor = ("black")
        self.image = circle(xCenter, yCenter, radius)
    def update(self):
        pass

class TPulsar(TBlackHole):
    def __init__(self, xCenter, yCenter, radius):
        TBlackHole.__init__(self, xCenter, yCenter, radius)
        changeFillColor(self.image, "brown")
    def update(self):
        self.__changeRadius(randint(5, 20))
    def __changeRadius(self, newRadius):
        self._width = 2*newRadius
        self.height = 2*newRadius
        changeCoords(self.image,
                    [(self._x - newRadius, self._y - newRadius),
                     (self._x + newRadius, self._y + newRadius)])

class TSpaceShip(TMovingObject):
    def __init__(self, xCenter, yCenter, radius, v, course):
        TMovingObject.__init__(self, xCenter, yCenter, 2*radius, 2*radius, v, course)
        self.image = circle(xCenter, yCenter, radius)
        self.brushColor = "blue"

    def update(self):
        self.move()
        if self.check_collision():
            self.destroy()
            self.create_new_ship()
        else:
            self.bounce()

    def check_collision(self):
        for obj in all_obj:
            if isinstance(obj, TBlackHole) or isinstance(obj, TPulsar):
                x1, y1, x2, y2 = coords(self.image)
                x3, y3, x4, y4 = coords(obj.image)
                if x1 < x4 and x2 > x3 and y1 < y4 and y2 > y3:
                    return True
        return False

    def destroy(self):
        deleteObject(self.image)
        all_obj.remove(self)

    def create_new_ship(self):
        all_obj.append(TSpaceShip(
            randint(0, screen_width),
            randint(0, screen_height),
            spaceship_size,
            randint(1, 5),
            randint(0, 359) * math.pi / 180)
        )
    def update(self):
        self.move()
        self.bounce()
    def bounce(self):
        x1, y1, x2, y2 = coords(self.image)
        if x1 <= 0 or x2 >= screen_width:
            self.course = math.pi - self.course
        if y1 <= 0 or y2 >= screen_height:
            self.course = -self.course

class TRanger(TSpaceShip):
    def __init__(self, xCenter, yCenter,
                 radius, v, course):
        TSpaceShip.__init__(self, xCenter, yCenter,
                 radius, v, course)
        changeFillColor(self.image, "yellow")
    def update(self):
        if randint(1, 20) == 1:
            self.course = randint(0, 359)*math.pi/180
        super().update()

windowSize(screen_width, screen_height)
canvasSize(screen_width, screen_height)

bh_number = randint(1, 5)
all_obj = []
for i in range(bh_number):
    all_obj.append(TBlackHole(
        randint(0, screen_width),
        randint(0, screen_height),
        randint(10, 20)
    ))
        
ps_number = randint(1, 3)
for i in range(ps_number):
    all_obj.append(TPulsar(
        randint(0, screen_width),
        randint(0, screen_height),
        randint(10, 20)
    ))

def update():
    for obj in all_obj:
        obj.update()
onTimer(update, update_period)

spaceships_number = randint(5, 9)
spaceship_size = 5
for i in range(spaceships_number):
    all_obj.append(TSpaceShip(
        randint(0, screen_width),
        randint(0, screen_height),
        spaceship_size,
        randint(1, 5),
        randint(0, 359)*math.pi/180)
    )
        

run()