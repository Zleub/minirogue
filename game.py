import sys, curses, random
from character import Character
from monster import Monster
from room import Room
from colors import *

class Game:
    def __init__(self):
        try:
            self.stdscr = curses.initscr()
            curses.noecho()
            curses.cbreak()
            curses.curs_set(0)
            curses.start_color()
            curses.use_default_colors()
            for i in range(0, curses.COLORS):
                curses.init_pair(i + 1, i, -1)
            self.stdscr.keypad(1)
        except:
            end() # FAIL

        self.min_room_size = 10
        self.max_room_size = 30 - self.min_room_size
        max_width, max_height = self.stdscr.getmaxyx()
        self.screen = self.stdscr.subwin(max_width, max_height, 0, 0)
        max_width, max_height = self.screen.getmaxyx()

        self.character = Character(self.screen, self)

        self.golds = []
        self.paths = []
        self.monsters = []
        self.stack = [
            Room(self.screen, -7, -5, 10, 20),
        ]

        while len(self.stack) != 10:
            self.randomRoom()
            pass

        self.selected = 0
        self.max_selected = 3
        self.panel = 0
        self.menu = 1
        self.offset = [ int(max_width/ 2), int(max_height/ 2) ]
        self.logger = [
            'Hello World'
        ]

        self.loop()

    def game_control(self, c):
        if (c == curses.KEY_UP
          and self.character.collides([-1, 0]) ):
            self.offset[0] += 1
            self.character.x -= 1
        if (c == curses.KEY_DOWN
          and self.character.collides([1, 0]) ):
            self.offset[0] -= 1
            self.character.x += 1
        if (c == curses.KEY_LEFT
          and self.character.collides([0, -1]) ):
            self.offset[1] += 1
            self.character.y -= 1
        if (c == curses.KEY_RIGHT
          and self.character.collides([0, 1]) ):
            self.offset[1] -= 1
            self.character.y += 1
        if (c == 46):
            self.panel = 1
            return 0
        return 1

    def menu_control(self, c):
        if (c == curses.KEY_UP):
            self.selected = (self.selected - 1 if self.selected - 1 >= 0 else self.max_selected )
        if (c == curses.KEY_DOWN):
            self.selected = (self.selected + 1 if self.selected + 1 <= self.max_selected else 0 )
        if (c == 10 and self.selected == 0):
            self.menu = 0
            self.game = 1
        if (c == 10 and self.selected == 3):
            end()

    def loop(self):

        while 1:
            max_width, max_height = self.stdscr.getmaxyx()

            if (self.menu):
                self.draw_menu()
                c = self.stdscr.getch()
                self.menu_control(c)
            elif (self.game):
                self.draw()
                c = self.stdscr.getch()
                t = self.game_control(c)
                self.draw()
                if (t):
                    for v in self.monsters:
                        v.update(self.offset)
                    if int(random.random() * 100) == 0:
                        self.randomNotify()
            pass

    def draw_menu(self):
        max_width, max_height = self.screen.getmaxyx()

        self.screen.clear()
        self.screen.addstr(0, int(max_height / 2) - 23, '  __  __ _       _                            ')
        self.screen.addstr(1, int(max_height / 2) - 23, ' |  \/  (_)     (_)                           ')
        self.screen.addstr(2, int(max_height / 2) - 23, ' | \  / |_ _ __  _ _ __ ___   __ _ _   _  ___ ')
        self.screen.addstr(3, int(max_height / 2) - 23, ' | |\/| | | \'_ \| | \'__/ _ \ / _` | | | |/ _ \\')
        self.screen.addstr(4, int(max_height / 2) - 23, ' | |  | | | | | | | | | (_) | (_| | |_| |  __/')
        self.screen.addstr(5, int(max_height / 2) - 23, ' |_|  |_|_|_| |_|_|_|  \___/ \__, |\__,_|\___|')
        self.screen.addstr(6, int(max_height / 2) - 23, '                              __/ |           ')
        self.screen.addstr(7, int(max_height / 2) - 23, '                             |___/            ')

        self.screen.addstr(12, int(max_height / 2) - 4, 'New Game')
        self.screen.addstr(13, int(max_height / 2) - 4, 'Load Game')
        self.screen.addstr(14, int(max_height / 2) - 4, 'Options')
        self.screen.addstr(15, int(max_height / 2) - 4, 'Exit')

        self.screen.addstr( 12 + self.selected, int(max_height / 2) - 6, '>')

        self.screen.refresh()


    def draw(self):
        max_width, max_height = self.stdscr.getmaxyx()
        self.screen.clear()

        for v in self.stack:
            v.draw(self.offset)

        for v in self.paths:
            _x = v[0] + self.offset[0]
            _y = v[1] + self.offset[1]
            if (_x >= 0 and _y >= 0
                and _x < max_width - 8 and _y < max_height):
                # self.screen.addch(_x, _y, ord('\''))
                self.screen.addstr(_x, _y, '.', curses.color_pair(FLOOR_COLOR))

        for v in self.golds:
            _x = v[0] + self.offset[0]
            _y = v[1] + self.offset[1]
            if (_x >= 0 and _y >= 0
                and _x < max_width - 8 and _y < max_height):
                # self.screen.addch(_x, _y, ord('\''))
                self.screen.addstr(_x, _y, '*', curses.color_pair(GOLD_COLOR))

        for v in self.monsters:
            v.draw(self.offset)

        self.character.draw()
        self.screen.hline(max_width - 8, 0, curses.ACS_HLINE, max_height)
        i = 7
        for v in self.logger:
            self.screen.addstr(max_width - i, 0, v)
            i -= 1

        self.screen.addstr(0, 0, self.character.toString())
        self.screen.refresh()


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
        max_width, max_height = self.stdscr.getmaxyx()

        i = -1
        while i == -1:
            r = int(random.random() * len(self.stack))
            if ( self.stack[r].up == -1
                or self.stack[r].down == -1
                or self.stack[r].left == -1
                or self.stack[r].right == -1):
                i = r
            pass

        room = self.stack[i]

        _ = -1
        while _ == -1:
            _r = int(random.random() * 4)
            if _r == 0 and room.up == -1:
                _ = 0
            if _r == 1 and room.down == -1:
                _ = 1
            if _r == 2 and room.left == -1:
                _ = 2
            if _r == 3 and room.right == -1:
                _ = 3
            pass

        def f(x, y, w, h):
            nr = Room(self.screen, x, y, w, h)
            self.stack.append(nr)
            return nr

        def gen_door(room, size):
            if size == 0:
                r = [ room.x, int(random.random() * (room.height - 2)) + room.y + 1 ]
            if size == 1:
                r = [ room.width + room.x - 1, int(random.random() * (room.height - 2)) + room.y + 1 ]
            if size == 2:
                r = [ int(random.random() * (room.width - 2)) + room.x + 1, room.y ]
            if size == 3:
                r = [ int(random.random() * (room.width - 2)) + room.x + 1, room.y + room.height - 1 ]

            room.doors.append(r)
            return r

        _w, _h = (int(random.random() * self.max_room_size) + self.min_room_size,
            int(random.random() * self.max_room_size) + self.min_room_size)
        if _ == 0:
            nr = f(room.x - _w - self.max_room_size, room.y, _w, _h)
            r1 = gen_door(room, _)
            r2 = gen_door(nr, 1)
            room.up = nr
            nr.down = room

            __ = range( min(r1[0], r2[0]) + 1, max(r1[0], r2[0]) )
            mid = __[int(len(__) / 2)]
            t = r2[1]
            for i in __:
                if (r1[1] - r2[1] and i == mid):
                    if (r1[1] - r2[1] + 1 < 0):
                        for j in range(r1[1] - r2[1], 0):
                            self.paths.append([int(i), r1[1] - j])
                    else:
                        for j in range(0, r1[1] - r2[1] + 1):
                            self.paths.append([int(i), r1[1] - j])
                    t = r1[1]

                self.paths.append([int(i), t])

        elif _ == 1:
            nr = f(room.x + _w + self.max_room_size, room.y, _w, _h)
            r2 = gen_door(room, _)
            r1 = gen_door(nr, 0)
            room.down = nr
            nr.up = room

            __ = range( min(r1[0], r2[0]) + 1, max(r1[0], r2[0]) )
            mid = __[int(len(__) / 2)]
            t = r2[1]
            for i in __:
                if (r1[1] - r2[1] and i == mid):
                    if (r1[1] - r2[1] + 1 < 0):
                        for j in range(r1[1] - r2[1], 0):
                            self.paths.append([int(i), r1[1] - j])
                    else:
                        for j in range(0, r1[1] - r2[1] + 1):
                            self.paths.append([int(i), r1[1] - j])
                    t = r1[1]

                self.paths.append([int(i), t])


        elif _ == 2:
            nr = f(room.x, room.y - _h - self.max_room_size, _w, _h)
            r1 = gen_door(room, _)
            r2 = gen_door(nr, 3)
            room.left = nr
            nr.right = room

            __ = range( min(r1[1], r2[1]) + 1, max(r1[1], r2[1]) )
            mid = __[int(len(__) / 2)]
            t = r2[0]
            for i in __:
                if (r1[0] - r2[0] and i == mid):
                    if (r1[0] - r2[0] < 0):
                        for j in range(r1[0] - r2[0], 0):
                            self.paths.append([r1[0] - j, int(i)])
                    else:
                        for j in range(0, r1[0] - r2[0] + 1):
                            self.paths.append([r1[0] - j, int(i)])
                    t = r1[0]

                self.paths.append([t, int(i)])


        elif _ == 3:
            nr = f(room.x, room.y + self.max_room_size + _h, _w, _h)
            r2 = gen_door(room, _)
            r1 = gen_door(nr, 2)
            room.right = nr
            nr.left = room

            __ = range( min(r1[1], r2[1]) + 1, max(r1[1], r2[1]) )
            mid = __[int(len(__) / 2)]
            t = r2[0]
            for i in __:
                if (r1[0] - r2[0] and i == mid):
                    if (r1[0] - r2[0] < 0):
                        for j in range(r1[0] - r2[0], 0):
                            self.paths.append([r1[0] - j, int(i)])
                    else:
                        for j in range(0, r1[0] - r2[0] + 1):
                            self.paths.append([r1[0] - j, int(i)])
                    t = r1[0]

                self.paths.append([t, int(i)])

        self.gen_gold(nr)
        self.gen_monster(nr)

    def gen_gold(self, room):
        nbr = int(random.random() * 3)
        if (nbr == 0):
            nbr = int(random.random() * 4)
            while nbr > -1:
                x, y = (int(random.random() * (room.width - 2)) + room.x + 1,
                    int(random.random() * (room.height - 2)) + room.y + 1)
                self.golds.append([x, y])
                nbr -= 1

    def gen_monster(self, room):
        nbr = int(random.random() )
        if (nbr == 0):
            nbr = int(random.random() * 6)
            while nbr > -1:
                x, y = (int(random.random() * (room.width - 2)) + room.x + 1,
                    int(random.random() * (room.height - 2)) + room.y + 1)
                self.monsters.append(Monster(self.screen, self, x, y))
                nbr -= 1
