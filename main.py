import curses, traceback, sys, signal
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

def signal_handler(signal, frame):
        curses.endwin
        sys.exit(0)


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
        signal.signal(signal.SIGINT, signal_handler)
        Game()
    except:
        end()
        traceback.print_exc()
