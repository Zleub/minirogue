class Room:
    def __init__(self, screen, x, y, width, height):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, offset):
        max_width, max_height = self.screen.getmaxyx()
        for _x in range(self.x, self.x + self.width):
            for _y in range(self.y, self.y + self.height):
                if (_x + offset[0] >= 0 and _y + offset[1] >= 0
                and _x + offset[0] < max_width - 8 and _y + offset[1] < max_height):
                    if (_x == self.x
                    or _y == self.y
                    or _x == self.x + self.width - 1
                    or _y == self.y + self.height - 1):
                        self.screen.addch(_x + offset[0], _y + offset[1], ord('O'))
                    else:
                        self.screen.addch(_x + offset[0], _y + offset[1], ord('.'))
        self.screen.refresh()
