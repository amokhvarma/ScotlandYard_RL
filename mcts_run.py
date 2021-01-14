import copy
import random
import math
import sys
import game
from utilities import mcts

try:
	c = sys.argv[1]
except:
	c = 2
try:	
	playouts = sys.argv[2]
except:
	playouts = 10
	
G = game.game()
p = mcts.mcts(G, c, playouts)
print(p.planning())
print(G.list_of_action_x())