import sys, curses
from colors import *

class Room:
    def __init__(self, screen, x, y, width, height):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.doors = []

        self.up = -1
        self.down = -1
        self.left = -1
        self.right = -1

    def draw(self, offset):
        max_width, max_height = self.screen.getmaxyx()

        for _x in range(self.x, self.x + self.width):
            for _y in range(self.y, self.y + self.height):
                __x = _x + offset[0]
                __y = _y + offset[1]

                # print('%d: %d' % (_x, _y), file=sys.stderr)
                # print([x for x in self.doors if x[0] == _x and x[1] == _y], file=sys.stderr)

                if (__x >= 0 and __y >= 0
                and __x < max_width - 8 and __y < max_height):
                    if len([x for x in self.doors if x[0] == _x and x[1] == _y]) != 0:
                        self.screen.addstr(__x, __y, '/')
                    elif (_x == self.x
                      or _y == self.y
                      or _x == self.x + self.width - 1
                      or _y == self.y + self.height - 1):
                        self.screen.addstr(__x, __y, 'O')
                    else:
                        self.screen.addstr(__x, __y, '.')
        self.screen.refresh()
