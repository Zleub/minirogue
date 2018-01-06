import curses, math, random
from colors import *

names = [
    'Goblin',
    'Orc',
    'Troll'
]

class Monster:
    def __init__(self, screen, game, x, y):
        # print('Character init')
        self.screen = screen
        self.game = game
        self.x, self.y = x, y
        self._life = int(random.random() * 5) + 3
        self.life = self._life
        self.name = names[int(random.random() * len(names))]

    def update(self, offset):
        dst = math.sqrt(
            math.pow(self.game.character.y - self.y, 2) +
            math.pow(self.game.character.x - self.x, 2)
        )
        x, y = self.game.character.x - self.x, self.game.character.y - self.y
        move = [0, 0]
        if (dst < 20):
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


    def draw(self, offset):
        max_width, max_height = self.screen.getmaxyx()

        _x = self.x + offset[0]
        _y = self.y + offset[1]
        if (_x >= 0 and _y >= 0
            and _x < max_width - 8 and _y < max_height):
                self.screen.addstr(_x, _y, '!')

    def collides(self, offset):
        err(self.x)
        err(offset)
        self.oldch = chr(self.screen.inch(self.x + offset[0], self.y + offset[1]))
        err(self.oldch)
        if (self.oldch == 'O' or self.oldch == ' ' or self.oldch == '!'):
            return 0
        elif (self.oldch == '@'):
            self.game.notify('A %s hit you' % self.name)
            return 0
        return 1
