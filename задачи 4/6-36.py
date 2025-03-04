# классы: корабль, подводная лодка, самолёт, вертолёт, гидросамолёт, мотоцикл, трактор

class Transport:
    def __init__(self, v, width, length, height):
        self.__v = v
        self.__width = width
        self.__length = length
        self.__height = height
    @property
    def v(self): return self.__v
    @property
    def width(self): return self.__width
    @property
    def length(self): return self.__length
    @property
    def height(self): return self.__height
    
class Water_Transport(Transport):
    