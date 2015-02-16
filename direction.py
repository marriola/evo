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

names= { UP: "U",
         UPRIGHT: "UR",
         RIGHT: "R",
         DOWNRIGHT: "DR",
         DOWN: "D",
         DOWNLEFT: "DL",
         LEFT: "L",
         UPLEFT: "UL" }
		 
			   
###############################################################################

def project(coord, dir, distance):
	if dir in (UP, UPLEFT, UPRIGHT):
		coord[0] -= distance

	if dir in (DOWN, DOWNLEFT, DOWNRIGHT):
		coord[0] += distance

	if dir in (UPLEFT, LEFT, DOWNLEFT):
		coord[1] -= distance

	if dir in (UPRIGHT, RIGHT, DOWNRIGHT):
		coord[1] += distance

	return coord

	
