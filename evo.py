###############################################################################
# GLOBAL IMPORTS
###############################################################################

import curses
from curses import wrapper
import random
from time import sleep


###############################################################################
# LOCAL IMPORTS
###############################################################################

from rat import rat
import direction


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

step_delay = 0.1
stable = []
maze = []


###############################################################################

def mutate(value, range):
    return value + random.randint(-range, range)    


###############################################################################

def random_coordinate():
    return (random.randint(0, MAZE_HEIGHT - 1), random.randint(0, MAZE_WIDTH))

	
###############################################################################

def occupied(row, col):
    return row < 0 or row >= MAZE_HEIGHT - 1 or col < 0 or col >= MAZE_WIDTH - 1 or maze[row][col] != ' '

	
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

    mazewin.refresh()


###############################################################################

def draw_stable(stablewin, stable):
    categories = [("#", 2), ("NAME", 10), ("HEALTH", 7), ("MAX HEALTH", 11), ("SNIFF", 6), ("DIR", 3)]
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
        stablewin.addstr(n + 1, category_columns[5], direction.names[dude.direction])

    stablewin.refresh()


###############################################################################

def setup_stable():
    # initialize stable

    for (color, name) in enumerate(RAT_NAMES):
        row, col = random_coordinate()
        stable.append(rat(color, row, col, name, mutate(rat.DEFAULT_MAX_HEALTH, 20), mutate(rat.DEFAULT_SNIFF_DISTANCE, 2)))
        while occupied(row, col):
            row, col = random_coordinate()
            stable[len(stable) - 1].row = row
            stable[len(stable) - 1].col = col


###############################################################################

def setup_game():
    for n in range(0, 16):
        curses.init_pair(n + 1,
                         7 if (n + 1) % 8 == 0 else 0,
                         (n + 1) % 8)

    load_maze()
    setup_stable()


###############################################################################

def game_step():
    for dude in stable:
        newrow, newcol = direction.project(dude.row, dude.col, dude.direction, 1, MAZE_HEIGHT, MAZE_WIDTH)
        if occupied(newrow, newcol):
            dude.direction = random.randint(1, 8)
        else:
            dude.row, dude.col = newrow, newcol

        
###############################################################################

def poll_keyboard(mazewin):
    ch = mazewin.getch()
    if ch == 27:
        return False

    return True

        
###############################################################################

def game_loop(mazewin, stablewin):
	while poll_keyboard(mazewin):
		sleep(step_delay)
		game_step()
		draw_stable(stablewin, stable)
		draw_maze(mazewin)

        
###############################################################################

def main(stdscr):
    setup_game()

    stablewin = curses.newwin(STABLE_HEIGHT + 1, STABLE_WIDTH, 0, MAZE_WIDTH + 3)
    mazewin = curses.newwin(MAZE_HEIGHT + 3, MAZE_WIDTH + 2, 0, 0)

    mazewin.nodelay(True)
    game_loop(mazewin, stablewin)

    
###############################################################################

wrapper(main)
