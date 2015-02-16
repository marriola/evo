###############################################################################
# GLOBAL IMPORTS
###############################################################################

import curses
from curses import wrapper
import random

###############################################################################
# LOCAL IMPORTS
###############################################################################

from rat import rat


###############################################################################
# CONSTANTS
###############################################################################

MAZE_WIDTH = 40
MAZE_HEIGHT = 25

STABLE_WIDTH = 80
STABLE_HEIGHT = 25

RAT_NAMES = ["Bonnie", "Clyde", "Zeke", "Biff", "Randy", "Jax", "Walter", "Gale", "Nova", "Boof", "Sam", "Huell"]


###############################################################################
# GAME STATE
###############################################################################

stable = []
maze = []


###############################################################################

def mutate(value, range):
    return value + random.randint(-range, range)    


###############################################################################

def occupied(row, col):
    return maze[row][col] != ' '


###############################################################################

def load_maze():
    maze_file = open("maze", "r")
    for line in maze_file:
        maze.append(line[1:-1])
    maze_file.close()


###############################################################################

def draw_maze(mazewin):
    mazewin.addstr(0, 0, "+" + "-" * (MAZE_WIDTH - 1) + "+");
    for n in range(0, MAZE_HEIGHT):
        mazewin.addstr(n + 1, 0, "|" + maze[n] + "|")
    mazewin.addstr(MAZE_HEIGHT + 1, 0, "+" + "-" * (MAZE_WIDTH - 1) + "+")

    for dude in stable:
        mazewin.addch(dude.row + 1, dude.col + 1, dude.name[0], curses.color_pair(dude.color))


###############################################################################

def draw_stable(stablewin, stable):
    categories = [("#", 2), ("NAME", 10), ("HEALTH", 7), ("MAX HEALTH", 11), ("SNIFF", 6)]
    category_columns = [0]

    stablewin.addstr(0, 0, " " * STABLE_WIDTH, curses.A_REVERSE)

    for (n, category) in enumerate(categories):
        stablewin.addstr(0, category_columns[n], category[0], curses.A_REVERSE)
        category_columns.append(category_columns[n] + category[1] + 1)

    for (n, dude) in enumerate(stable):
        stablewin.addstr(n + 1, category_columns[0], str(n + 1), curses.color_pair(dude.color))
        stablewin.addstr(n + 1, category_columns[1], dude.name)
        stablewin.addstr(n + 1, category_columns[2], str(dude.health))
        stablewin.addstr(n + 1, category_columns[3], str(dude.max_health))
        stablewin.addstr(n + 1, category_columns[4], str(dude.sniff_distance))

    stablewin.refresh()


###############################################################################

def setup_stable():
    # initialize stable
    for (color, name) in enumerate(RAT_NAMES):
        row = random.randint(0, MAZE_HEIGHT)
        col = random.randint(0, MAZE_WIDTH)
        stable.append(rat(color, row, col, name, mutate(rat.DEFAULT_MAX_HEALTH, 20), mutate(rat.DEFAULT_SNIFF_DISTANCE, 2)))
        # don't really know why this doesn't work
        # while occupied(row, col):
        #     stable[len(stable) - 1].row = random.randint(0, MAZE_HEIGHT)
        #     stable[len(stable) - 1].col = random.randint(0, MAZE_WIDTH)


###############################################################################

def setup_game():
    for n in range(0, 16):
        curses.init_pair(n + 1,
                         7 if (n + 1) % 8 == 0 else 0,
                         (n + 1) % 8)

    load_maze()
    setup_stable()


###############################################################################

def main(stdscr):
    setup_game()

    stablewin = curses.newwin(STABLE_HEIGHT + 1, STABLE_WIDTH, 0, MAZE_WIDTH + 3)
    draw_stable(stablewin, stable)

    mazewin = curses.newwin(MAZE_HEIGHT + 3, MAZE_WIDTH + 2, 0, 0)
    draw_maze(mazewin)

    mazewin.refresh()
    mazewin.getkey()


###############################################################################

wrapper(main)
