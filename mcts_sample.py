import game
from utilities import mcts
#
G = game.game()
p = mcts.mcts(G)
print(p.planning())
print(G.list_of_action_x())
