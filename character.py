import curses, random
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

        self._life = 10 #max hp
        self.life = 10
        self.recup = 0

        self.level = 1
        self.exp = 0
        self.next_lvl = 100

        self.gold = 0

        self.str = 4
        self.agi = 4
        self.int = 4

    def addLife(self, v):
        if (self.life + v >= self._life):
            self.life = self._life
        else:
            self.life += v

    def draw(self):
        self.recup += 1
        if (self.recup == 100):
            self.recup = 0
            self.addLife(1)
        self.screen.addstr(self._x, self._y, '@', curses.color_pair(PLAYER_COLOR))

    def collides(self, offset):
        self.oldch = chr(self.screen.inch(self._x + offset[0], self._y + offset[1]))
        # err('Character: %s' % self.oldch)
        if (self.oldch == 'ཏ' or self.oldch == ' '):
            self.game.notify('You knock yourself back')
            return 0
        elif (self.oldch == 'ȡ'):
            monsters  = [a for a in self.game.monsters if a.x == self.x + offset[0] and a.y == self.y + offset[1]]
            self.game.notify('You hit a %s' % (monsters[0].name))
            monsters[0].life -= (self.str - monsters[0].dfs if self.str - monsters[0].dfs > 0 else 1)
            if (monsters[0].life <= 0):
                _t = monsters[0].level * 5 + random.randrange(0, monsters[0].level * 5)
                self.exp += _t
                self.game.notify('You gain %d exp!' % _t)
                self.game.monsters  = [a for a in self.game.monsters if a not in monsters]
				#choose a bonus.
            return 0
        elif (self.oldch == '휪'):
            g = int(random.random() * 10) + 2
            self.gold += g
            self.game.notify('You pick up %d golds' % g)
            self.game.golds  = [a for a in self.game.golds if a not in [[self.x + offset[0], self.y + offset[1]]]]
            self.oldch = 'Į'
        return 1

    def toString(self):
        return 'Life: %d / %d\tGold: %d\t\tSTR: %d\tAGI: %d\tINT: %d \tEXP: %d%c' % (
            self.life, self._life, self.gold, self.str, self.agi, self.int, self.exp / self.next_lvl * 100, '%'
        )
