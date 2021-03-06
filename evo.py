###############################################################################
# GLOBAL IMPORTS
###############################################################################

import curses
import math
import random
import sys
from time import sleep


###############################################################################
# LOCAL IMPORTS
###############################################################################

from rat import Rat
import direction


###############################################################################
# CONSTANTS
###############################################################################

FOOD_COLOR = 32
FOOD_VALUE = 15

MAZE_WIDTH = 40
MAZE_HEIGHT = 25

STABLE_WIDTH = 80
STABLE_HEIGHT = 25

STABLE_UPDATE_INTERVAL = 5
FEEDING_INTERVAL = 20
HEALTH_SUBTRACT_INTERVAL = 10

NUM_INITIAL_RATS = 5

OFFSET_TO_DIRECTION = { (-1, -1): direction.UPLEFT,
                        (-1, 0): direction.UP,
                        (-1, 1): direction.UPRIGHT,
                        (1, 1): direction.DOWNRIGHT,
                        (1, 0): direction.DOWN,
                        (1, -1): direction.DOWNLEFT,
                        (0, 1): direction.RIGHT,
                        (0, -1): direction.LEFT }

###############################################################################
# GAME STATE
###############################################################################

step_delay = 0.1
step = 0

stable = []
maze = []
food_locations = []

stablewin = None

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
        maze.append(" " * 40) #line[1:-1])
    maze_file.close()


###############################################################################

def draw_maze():
    mazewin.addstr(0, 0, "+" + "-" * MAZE_WIDTH + "+");
    for n in range(0, MAZE_HEIGHT):
        mazewin.addstr(n + 1, 0, "|" + maze[n] + "|")
    mazewin.addstr(MAZE_HEIGHT + 1, 0, "+" + "-" * MAZE_WIDTH + "+")

    for dude in stable:
        mazewin.addch(dude.row + 1, dude.col + 1, dude.name[0], curses.color_pair(dude.color))

    for food_row, food_col in food_locations:
        mazewin.addch(food_row + 1, food_col + 1, "&", curses.color_pair(FOOD_COLOR) + curses.A_BOLD)

    mazewin.refresh()


###############################################################################

def draw_stable():
    categories = [("#", 2), ("GEN", 4), ("NAME", 10), ("HEALTH", 7), ("SNIFF", 6), ("DIR", 3)]
    category_columns = [0]

    stablewin.addstr(0, 0, " " * STABLE_WIDTH, curses.A_REVERSE)

    for (n, category) in enumerate(categories):
        stablewin.addstr(0, category_columns[n], category[0], curses.A_REVERSE)
        category_columns.append(category_columns[n] + category[1] + 1)

    for (n, dude) in enumerate(stable):
        stablewin.addstr(n + 1, 0, " " * STABLE_WIDTH)
        stablewin.addstr(n + 1, category_columns[0], str(n + 1), curses.color_pair(dude.color))
        stablewin.addstr(n + 1, category_columns[1], str(dude.generation))
        stablewin.addstr(n + 1, category_columns[2], dude.name)
        stablewin.addstr(n + 1, category_columns[3], str(dude.health) + "/" + str(dude.max_health))
        stablewin.addstr(n + 1, category_columns[4], str(dude.sniff_distance))
        stablewin.addstr(n + 1, category_columns[5], direction.names[dude.direction])

    stablewin.refresh()


###############################################################################

def setup_stable():
    # initialize stable

    for n in range(NUM_INITIAL_RATS):
        row, col = random_coordinate()
        stable.append(Rat(n, row, col, Rat.NAMES[n], mutate(Rat.DEFAULT_MAX_HEALTH, 20), 1, mutate(Rat.DEFAULT_SNIFF_DISTANCE, 2)))
        while occupied(row, col):
            row, col = random_coordinate()
            stable[len(stable) - 1].row = row
            stable[len(stable) - 1].col = col


###############################################################################

def setup_game():
    for n in range(0, 16):
        curses.init_pair(n + 1,
                         7 if (n + 1) % 8 == 0 or (n + 1) % 8 == 4 else 0,
                         (n + 1) % 8)

    curses.init_pair(FOOD_COLOR, curses.COLOR_WHITE, curses.COLOR_GREEN)

    load_maze()
    setup_stable()


###############################################################################

def sense_food(dude):
    def sign(num):
        return 0 if num == 0 else num / abs(num)

    # define area to sniff for food
    row_start = dude.row - dude.sniff_distance
    col_start = dude.col - dude.sniff_distance
    row_end = dude.row + dude.sniff_distance
    col_end = dude.col + dude.sniff_distance

    if row_start < 0:
        row_start = 0
    if row_end >= MAZE_HEIGHT:
        row_end = MAZE_HEIGHT - 1
    if col_start < 0:
        col_start = 0
    if col_end >= MAZE_WIDTH:
        col_end = MAZE_WIDTH - 1

    # scan immediate vicinity for food, keeping track of the nearest piece of food
    food_in_range = []
    closest = (sys.maxint, -1, -1)

    for row in range(row_start, row_end + 1):
        for col in range(col_start, col_end + 1):
            if (row, col) in food_locations:
                distance = math.sqrt(math.pow(dude.row - row, 2) + math.pow(dude.col - col, 2))
                if distance < closest[0]:
                    closest = (distance, row, col)

    # return the direction to go to get to the nearest food
    if closest[0] < sys.maxint:
        food_offset = (sign(closest[1] - dude.row), sign(closest[2] - dude.col))
        return None if food_offset == (0, 0) else OFFSET_TO_DIRECTION[food_offset]
    else:
        return None


###############################################################################

def move_rat(dude):
    newrow, newcol = direction.project(dude.row, dude.col, dude.direction, 1, MAZE_HEIGHT, MAZE_WIDTH)
    if occupied(newrow, newcol):
        dude.direction = random.randint(1, 8)
    else:
        dude.row, dude.col = newrow, newcol

    food_direction = sense_food(dude)
    if food_direction != None:
        dude.direction = food_direction

    for food_row, food_col in food_locations:
        if dude.row == food_row and dude.col == food_col:
            food_locations.remove((food_row, food_col))
            dude.health += FOOD_VALUE
            if dude.health >= dude.max_health:
                stable.append(dude.reproduce())


###############################################################################

def game_step():
    global step

    for dude in stable:
        move_rat(dude)

    step += 1

    if step % HEALTH_SUBTRACT_INTERVAL == 0:
        subtract_health()

    if step % STABLE_UPDATE_INTERVAL == 0:
        draw_stable()

    if step % FEEDING_INTERVAL == 0:
        feed()

        
###############################################################################

def poll_keyboard():
    ch = mazewin.getch()
    if ch == 27:
        return False

    return True


###############################################################################

def subtract_health():
    for dude in stable:
        dude.health -= dude.health_decay
        if dude.health < 0:
            stablewin.addstr(len(stable), 0, " " * STABLE_WIDTH)
            stable.remove(dude)

        
###############################################################################

def feed():
    row, col = random_coordinate()
    while (occupied(row, col)):
        row, col = random_coordinate()
    
    food_locations.append((row, col))


###############################################################################

def game_loop():

    while poll_keyboard():
        sleep(step_delay)
        game_step()
        draw_maze()

        
###############################################################################

def main(stdscr):
    global stablewin
    global mazewin

    setup_game()

    stablewin = curses.newwin(STABLE_HEIGHT + 1, STABLE_WIDTH, 0, MAZE_WIDTH + 3)
    mazewin = curses.newwin(MAZE_HEIGHT + 3, MAZE_WIDTH + 2, 0, 0)

    mazewin.nodelay(True)
    draw_stable()
    game_loop()

    
###############################################################################

curses.wrapper(main)
