from utilities import MrX,detective,observation,graph_utils,mcts
import numpy as np
import copy
import random
import math
import sys
from game import game
import time
import matplotlib.pyplot as plt

try:
	c = int(sys.argv[1])
except:
	c = 2
try:	
	playouts = int(sys.argv[2])
except:
	playouts = 10
try:	
	runs = int(sys.argv[3])
except:
	runs = 100

surv = []
win_rate = []
total_steps = 0
for itr in range(0,runs):
	G = game()
	step_rew,rew = 0,0
	while(not G.finish()):
		print("Move no:", G.move, "\n")
		p = mcts.mcts(G, c, playouts)
		act = p.planning()
		state_act = G.f_x_action(act)
		if(act[0] == 4):
			mode = [act[0],act[1]]
			target = [act[2]]
		else:
			mode = [act[0]]
			target = [act[1]]
		print(act)
		G.take_action(target,"x",mode,0)
		total_steps+=1
		print("\n")
		for i in range(G.no_of_players):
			G.take_action(None,"detective",[],i,"random")
			print("\n")
		G.update_fv()
		step_rew = G.X_reward-rew
		rew = G.X_reward
		# G = copy.deepcopy(G)
		print(rew, step_rew)
	if (G.move>=20):
		surv.append(1)
	else:
		surv.append(0)
	win_rate.append(sum(surv)/float(len(surv)))
	if(itr%1000 == 0):
		plot1 = plt.figure(1)
		plt.title("Win rate vs Episodes")
		plt.xlabel("Episode")
		plt.ylabel("Win rate ")
		plt.plot(win_rate)
		plt.savefig("Result/mcts_win_rate.png")

	G.print_pos()