import curses
from colors import *

class Character:
    def __init__(self, screen, game):
        # print('Character init')
        self.screen = screen
        self.game = game
        self.x, self.y = 0, 0
        self._x, self._y = screen.getmaxyx()
        self._x = int(self._x / 2)
        self._y = int(self._y / 2)
        self._life = 10
        self.life = 10

        self.gold = 0

    def draw(self):
        self.screen.addstr(self._x, self._y, '@')

    def collides(self, offset):
        self.oldch = chr(self.screen.inch(self._x + offset[0], self._y + offset[1]))
        if (self.oldch == 'O' or self.oldch == ' ' or self.oldch == '!'):
            self.game.notify('You knock yourself back')
            return 0
        return 1

    def toString(self):
        return 'Life: ' + str(self.life) + ' / ' + str(self._life) + '\t' + ('Gold: %d' % self.gold)
