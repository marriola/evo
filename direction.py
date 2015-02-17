###############################################################################
# CONSTANTS
###############################################################################

UP = 1
UPRIGHT = 2
RIGHT = 3
DOWNRIGHT = 4
DOWN = 5
DOWNLEFT = 6
LEFT = 7
UPLEFT = 8

names = { UP: "U",
          UPRIGHT: "UR",
          RIGHT: "R",
          DOWNRIGHT: "DR",
          DOWN: "D",
          DOWNLEFT: "DL",
          LEFT: "L",
          UPLEFT: "UL" }
		 
			   
###############################################################################

def project(row, col, dir, distance, MAZE_HEIGHT, MAZE_WIDTH):
	if dir in (UP, UPLEFT, UPRIGHT):
		row -= distance

	if dir in (DOWN, DOWNLEFT, DOWNRIGHT):
		row += distance

	if dir in (UPLEFT, LEFT, DOWNLEFT):
		col -= distance

	if dir in (UPRIGHT, RIGHT, DOWNRIGHT):
		col += distance

	return (row, col)

	
