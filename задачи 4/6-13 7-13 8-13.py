from graph import *

class TShip:
    def __init__(self, x0, y0, fileName):
        self.x = x0 if x0 >= 0 else 0
        self.y = 0
        self.v = y0
        self.image = image(self.x, 150, fileName)
    def move(self):
        moveObjectBy(self.image, self.v, 0)
    def update():
        ship.move()
        
    fps = 20
    updatePeriod = round(1000 / fps)
    onTimer(update, updatePeriod)

class Torp_app:
    def __init__(self) -> None:
        pass

ship = TShip(30, 3, "ship.gif")
run()