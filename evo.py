import curses
from curses import wrapper

from rat import rat

MAZE_WIDTH = 40
MAZE_HEIGHT = 25

STABLE_WIDTH = 80
STABLE_HEIGHT = 25

def draw_maze(mazewin):
    mazewin.addstr(0, 0, "+" + "-" * MAZE_WIDTH + "+");
    for n in range(0, MAZE_HEIGHT):
        mazewin.addstr(n + 1, 0, "|" + " " * MAZE_WIDTH + "|")
    mazewin.addstr(MAZE_HEIGHT, 0, "+" + "-" * MAZE_WIDTH + "+")

def draw_stable(stablewin, stable):
    categories = [("#", 2), ("NAME", 16)]
    category_column = 0

    for category in categories:
        stablewin.addstr(0, category_column, category[0], curses.A_REVERSE)
        category_column += category[1]

    for (n, dude) in enumerate(stable):
        stablewin.addstr(n + 1, 0, str(n + 1))
        stablewin.addstr(n + 1, 3, dude.name)

    stablewin.refresh()

def main(stdscr):
    stable = [rat("clyde", rat.DEFAULT_MAX_HEALTH)]
    stablewin = curses.newwin(STABLE_HEIGHT + 1, STABLE_WIDTH, 0, MAZE_WIDTH + 3)
    draw_stable(stablewin, stable)

    mazewin = curses.newwin(MAZE_HEIGHT + 2, MAZE_WIDTH + 2, 0, 0)
    draw_maze(mazewin)

    mazewin.refresh()
    mazewin.getkey()

###############################################################################

wrapper(main)
