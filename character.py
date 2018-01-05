import curses
class Character:
    def __init__(self, screen, game):
        # print('Character init')
        self.screen = screen
        self.game = game
        self.x, self.y = screen.getmaxyx()
        self.x = int(self.x / 2)
        self.y = int(self.y / 2)

    def draw(self):
        self.screen.addch(self.x, self.y, ord('@'))

    def collides(self, offset):
        self.oldch = chr(self.screen.inch(self.x + offset[0], self.y + offset[1]))
        if (self.oldch == 'O'):
            self.game.notify('You knock yourself back')
            return 0
        return 1
