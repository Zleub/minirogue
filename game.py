import curses, random
from character import Character
from room import Room

class Game:
    def __init__(self):
        try:
            stdscr = curses.initscr()
            curses.noecho()
            curses.cbreak()
            curses.curs_set(0)
            stdscr.keypad(1)
        except:
            end() # FAIL

        max_width, max_height = stdscr.getmaxyx()
        self.screen = stdscr.subwin(max_width, max_height, 0, 0)

        self.character = Character(self.screen, self)

        self.stack = [
            Room(self.screen,
                int(max_width / 2) - 10, int(max_height / 2) - 10,
                20, 20),
        ]
        while len(self.stack) != 10:
            self.randomRoom()
            pass

        self.offset = [ 0, 0 ]
        self.logger = [
            'Hello World'
        ]

        while 1:
            max_width, max_height = stdscr.getmaxyx()

            self.screen.clear()
            self.draw()
            self.character.draw()
            self.screen.hline(max_width - 8, 0, curses.ACS_HLINE, 77)
            i = 7
            for v in self.logger:
                self.screen.addstr(max_width - i, 0, v)
                i -= 1

            self.screen.refresh()

            c = stdscr.getch()
            if (c == curses.KEY_UP
            and self.character.collides([-1, 0]) ):
                self.offset[0] += 1
            if (c == curses.KEY_DOWN
            and self.character.collides([1, 0]) ):
                self.offset[0] -= 1
            if (c == curses.KEY_LEFT
            and self.character.collides([0, -1]) ):
                self.offset[1] += 1
            if (c == curses.KEY_RIGHT
            and self.character.collides([0, 1]) ):
                self.offset[1] -= 1

            if int(random.random() * 100) == 0:
                self.randomNotify()

            pass

    def draw(self):
        for v in self.stack:
            v.draw(self.offset)

    def notify(self, str):
        self.logger.append(str)
        if len(self.logger) == 8:
            self.logger = self.logger[1:]

    def randomNotify(self):
        strs = [
            'You feel quite alone ...',
            'Amazing how stone can be fascinating while nothing else to stare about'
        ]

        self.notify( strs[int(random.random() * len(strs))] )

    def randomRoom(self):
        x, y, w, h = int(random.random() * 30), int(random.random() * 30), int(random.random() * 30), int(random.random() * 30)
        b = 1
        for v in self.stack:
            if ( (v.x < x and v.x + v.width < x)
            or (v.y < y and v.y + v.height < y)
            or v.x > x + w or v.y > y + h ):
                b = 0

        if b:
            self.stack.append( Room(self.screen, x, y, w, h) )
