import copy
import random
import math
import sys
import game
from utilities import mcts

try:
	c = int(sys.argv[1])
except:
	c = 2
try:	
	playouts = int(sys.argv[2])
except:
	playouts = 10
	
G = game.game()
p = mcts.mcts(G, c, playouts)
print(p.planning())
print(G.list_of_action_x())
