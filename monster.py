import curses, math, random, unicodedata
from colors import *

names = [
    'Goblin',
    'Orc',
    'Troll'
]


class Monster:
    id = 0

    def __init__(self, screen, game, x, y):
        self.id = Monster.id
        Monster.id += 1

        self.screen = screen
        self.game = game
        self.x, self.y = x, y
        self._life = int(random.random() * 5) + 3
        self.life = self._life
        self.name = names[int(random.random() * len(names))]

        self.level = self.game.level

        self.atk = int(random.random() * 4) + self.level
        self.dfs = int(random.random() * 3) + self.level

    def update(self, offset):
        self.dst = math.sqrt(
            math.pow(self.game.character.y - self.y, 2) +
            math.pow(self.game.character.x - self.x, 2)
        )
        x, y = self.game.character.x - self.x, self.game.character.y - self.y
        move = [0, 0]
        if (self.dst < 20):
            # err([self.id, x, y])
            if (abs(self.game.character.y - self.y) >= abs(self.game.character.x - self.x)
              and self.game.character.y - self.y < 0):
                if (self.collides([0 + offset[0], -1 + offset[1]])):
                    move[1] -= 1
                elif (self.game.character.x - self.x < 0 and self.collides([-1 + offset[0], 0 + offset[1]])):
                    move[0] -= 1
                elif (self.game.character.x - self.x > 0 and self.collides([1 + offset[0], 0 + offset[1]])):
                    move[0] += 1

            if (abs(self.game.character.y - self.y) >= abs(self.game.character.x - self.x)
              and self.game.character.y - self.y > 0):
                if (self.collides([0 + offset[0], 1 + offset[1]])):
                    move[1] += 1
                elif (self.game.character.x - self.x < 0 and self.collides([-1 + offset[0], 0 + offset[1]])):
                    move[0] -= 1
                elif (self.game.character.x - self.x > 0 and self.collides([1 + offset[0], 0 + offset[1]])):
                    move[0] += 1

            if (abs(self.game.character.y - self.y) < abs(self.game.character.x - self.x)
              and self.game.character.x - self.x < 0):
                if (self.collides([-1 + offset[0], 0 + offset[1]])):
                    move[0] -= 1
                elif (self.game.character.y - self.y < 0 and self.collides([0 + offset[0], 1 + offset[1]])):
                    move[1] -= 1
                elif (self.game.character.y - self.y > 0 and self.collides([0 + offset[0], -1 + offset[1]])):
                    move[1] += 1

            if (abs(self.game.character.y - self.y) < abs(self.game.character.x - self.x)
              and self.game.character.x - self.x > 0):
                if (self.collides([1 + offset[0], 0 + offset[1]])):
                    move[0] += 1
                elif (self.game.character.y - self.y < 0 and self.collides([0 + offset[0], 1 + offset[1]])):
                    move[1] -= 1
                elif (self.game.character.y - self.y > 0 and self.collides([0 + offset[0], -1 + offset[1]])):
                    move[1] += 1

            self.x += move[0]
            self.y += move[1]
            self.game.draw()

    def draw(self, offset):
        max_width, max_height = self.screen.getmaxyx()

        _x = self.x + offset[0]
        _y = self.y + offset[1]
        if (_x >= 0 and _y >= 0
            and _x < max_width - 8 and _y < max_height):
                self.screen.addstr(_x, _y, '!', curses.color_pair(MONSTER_COLOR))

    def collides(self, offset):
        max_width, max_height = self.screen.getmaxyx()
        _x = self.x + offset[0]
        _y = self.y + offset[1]
        if (_x >= 0 and _y >= 0
          and _x < max_width - 8 and _y < max_height):
            self.oldch = chr(self.screen.inch(_x, _y))
            test = self.oldch.encode()
            for value in test:
                # err(value)
                pass
            if (self.oldch == '祐' or self.oldch == ' ' or self.oldch == 'ȡ'):
                return 0
            elif (self.oldch == 'ീ'):
                _d = (self.atk - self.game.character.agi if self.atk - self.game.character.agi > 0 else 1)
                self.game.notify('An ennemy %s hit you for %d' % (self.name, _d))
                self.game.character.life -= _d
                if self.game.character.life <= 0:
                    self.game.notify('Game over ! Press any key to continue ...')
                    c = self.game.stdscr.getch()
                    self.game.menu = 1
                return 0
            return 1
        return 0
