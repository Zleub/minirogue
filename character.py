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

        self._life = 16 #max hp
        self.life = self._life
        self.recup = 0

        self.level = 1
        self.exp = 0
        self.next_lvl = 100

        self.gold = 0

        self.str = 4
        self.agi = 4
        self.int = 4

        self.lvl_up_str = 1
        self.lvl_up_agi = 1
        self.lvl_up_int = 1

    def addLife(self, v):
        if (self.life + v >= self._life):
            self.life = self._life
        else:
            self.life += v

    def update(self):
        self.recup += 1
        if (self.recup == 100):
            self.recup = 0
            self.addLife(1)

        if (self.life <= 0):
            self.game.death = 1

    def draw(self):
        self._x, self._y = self.screen.getmaxyx()
        self._x, self._y = (int(self._x / 2), int(self._y / 2))
        self.screen.addstr(self._x, self._y, '@', curses.color_pair(PLAYER_COLOR))

    def collides(self, offset):
        self.oldch = chr(self.screen.inch(self._x + offset[0], self._y + offset[1]))
        # err('Character')
        # err(self.screen.inch(self._x + offset[0], self._y + offset[1]))
        # err(self.oldch)
        # err((ord(self.oldch) >> 8) & 0xff)
        # err([
        #     ((ord(self.oldch) >> 8) & 0xff),
        #     ((ord(self.oldch) >> 8) & 0xff << 8),
        #     ((ord(self.oldch) >> 8) & 0xff << 16),
        #     ((ord(self.oldch) >> 8) & 0xff << 24),
        # ])
        # test = self.oldch.encode()
        # for value in test:
        #     err([
        #         (value),
        #         (value << 8),
        #         (value << 16),
        #         (value << 24),
        #     ])
        #     pass
        if (self.oldch == '祐' or self.oldch == ' '):
            self.game.notify('You knock yourself back')
            return 0
        elif (self.oldch == 'ȡ'):
            monsters  = [a for a in self.game.monsters if a.x == self.x + offset[0] and a.y == self.y + offset[1]]
            _hit = (self.str - monsters[0].dfs if self.str - monsters[0].dfs > 0 else 1)
            self.game.notify('You hit an ennemy %s for %d damage' % (monsters[0].name, _hit))
            monsters[0].life -= _hit
            if (monsters[0].life <= 0):
                self.game.notify('You killed the ennemy %s' % (monsters[0].name))
                _t = monsters[0].level * 2 + random.randrange(0, monsters[0].level * 10)
                _g = random.randrange(0, monsters[0].level * 3)
                self.exp += _t + 50
                self.gold += _g
                if _g == 0:
                    self.game.notify('You gain %d exp!' % (_t))
                elif _g == 1:
                    self.game.notify('You gain %d exp! The monster had %d gold coin!' % (_t, _g))
                else :
                    self.game.notify('You gain %d exp! The monster had %d gold coins!' % (_t, _g))
                if self.exp >= self.next_lvl:
                    self.level += 1
                    self.exp -= self.next_lvl
                    self.next_lvl = self.level * 100
                    self._life += random.randrange(3 + (self.str / 2), 3 + self.str)
                    self.life = self._life
                    # #self.game.level_up_screen = 1
                    # self.game.notify('Level up !')
                    # self.str += self.lvl_up_str
                    # self.int += self.lvl_up_int
                    # self.agi += self.lvl_up_agi
                    self.game.notify('Level up ! Choose an upgrade !(type : a -> agi | i -> int | s -> strengh)')
                    while 1:
                        c = chr(self.game.stdscr.getch())
                        if c == 'a' or c == 's' or c == 'i':
                            if c == 's':
                                self.str + 1
                                self.game.notify('You\'re str increased')
                            if c == 'i':
                                self.int + 1
                                self.game.notify('You\'re int increased')
                            if c == 'a':
                                self.agi + 1
                                self.game.notify('You\'re agi increased')
                            break
                        else:
                            self.game.notify('You need to press a or s or i to level up.. Retry again !')
                            self.game.draw()
                self.game.monsters  = [a for a in self.game.monsters if a not in monsters]
				#choose a bonus.
            return 0
        elif (self.oldch == '쭆'):
            if self.life == self._life:
                self.game.notify('You found some food on the floor! But you\'re already full, come back later !')
            else :
                self.game.notify('You found some food on the floor! You eat it and restore your life !')
                self.addLife(random.randrange(1, int(self._life / 20 + self.game.level * 3)))
                self.game.food = [a for a in self.game.food if a not in [[self.x + offset[0], self.y + offset[1]]]]
                self.oldch = 'Į'
        elif (self.oldch == '㕔'):
            self.game.notify('You stepped on a trap.. Are you blind ?')
            if (random.randrange(0, 20)== 0):
                self._life -= random.randrange(1, 5)
                if self.life > self._life :
                    self.life = self._life
            else:
                self.life -= random.randrange(5, 20)
            # if self.life <= 0:
            #     self.game.notify('Game over !')
            #     c = self.game.stdscr.getch()
            #     self.game.menu = 1
            # self.life
        elif (self.oldch == '휪'):
            g = int(random.random() * 10) + 2
            self.gold += g
            self.game.notify('You pick up %d golds' % g)
            self.game.golds  = [a for a in self.game.golds if a not in [[self.x + offset[0], self.y + offset[1]]]]
            self.oldch = 'Į'
        return 1

    def toString(self):
        return 'Floor: %d\t\tLevel: %d \tLife: %d / %d\tGold: %d\t\tSTR: %d\tAGI: %d\tINT: %d \tEXP: %d%c' % (
            self.game.level, self.level, self.life, self._life, self.gold, self.str, self.agi, self.int, self.exp / self.next_lvl * 100, '%'
        )
