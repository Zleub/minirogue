import curses, traceback, sys
from game import Game

# Notes
#    a point is a array like [x, y]

# Todo
# monsters
# items( gold > consommable > equipable)
# main menu (new game, load game, options)
# load game, save Game
# config file (.roguerc)
# better room generation(doors, paths)
# races, classes

def end():
    curses.echo()
    curses.nocbreak()
    curses.endwin()
    curses.curs_set(1)

if __name__=='__main__':
    import sys
    if sys.version_info[0] < 3:
        print("Must be using Python 3")
        sys.exit()
    try:
        sys.path.append('.')
        Game()
    except:
        end()
        traceback.print_exc()
