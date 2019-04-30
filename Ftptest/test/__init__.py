import struct
from functools import reduce
class Screen(object):

    @property
    def width(self):
        return self._width
    @width.setter
    def width(self,width):
        self._width = width

    @property
    def height(self):
        return self._width

    @height.setter
    def height(self, height):
        self._height = height

    @property
    def area(self):
        return self._width*self._height

if __name__ == '__main__':
    screen = Screen()
    screen.width=10
    screen.height = 20
    # print screen.width
    # print screen.height
    # print screen.area

    a = 12.34
    bytes = struct.pack('i', a)
    a= struct.unpack('i',bytes)
    # print bytes
    # print a
    


