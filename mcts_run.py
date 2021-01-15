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
	playouts = str(sys.argv[2])
except:
	playouts = 10
try:	
	runs = int(sys.argv[3])
except:
	runs = 500

def trans(test):
	if(test[0][0]==4):
		return [test[0][0],test[0][1],test[1][0]]
	else:
		return [test[0][0],test[1][0]]

colors = ['b','g','r','y','k','m']
playouts = list(playouts.split(","))
for i in range(0,len(playouts)):
	playouts[i] = int(playouts[i])
	surv = []
	win_rate = []
	rew_list = []
	total_steps = 0
	for itr in range(0,runs+2):
		G = game()
		step_rew,rew = 0,0
		while(not G.finish()):
			print("Move no:", G.move, "\n")
			p = mcts.mcts(G, c, int(playouts[i]))
			act = trans(p.planning())
			print(act)
			state_act = G.f_x_action(act)
			if(act[0] == 4):
				mode = [act[0],act[1]]
				target = [act[2]]
			else:
				mode = [act[0]]
				target = [act[1]]
			G.take_action(target,"x",mode,0)
			total_steps+=1
			print("\n")
			for j in range(G.no_of_players):
				G.take_action(None,"detective",[],j,"random")
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
		rew_list.append(rew/float(len(surv)))
		if(itr//runs == 1):
			plot1 = plt.figure(1)
			plt.title("Win rate vs Episodes")
			plt.xlabel("Episode")
			plt.ylabel("Win rate for X")
			plt.ylim(-0.2,1.4)
			plt.plot(win_rate, colors[i], label=str(playouts[i]))
			plt.legend(loc="upper right")
			plt.savefig("Result/mcts_win_rate_x.png")

			plot1 = plt.figure(2)
			plt.title("Dynamic Average Reward vs Episodes")
			plt.xlabel("Episode")
			plt.ylabel("Dynamic Average Reward for X")
			plt.plot(rew_list, colors[i], label=str(playouts[i]))
			plt.legend(loc="upper right")
			plt.savefig("Result/mcts_dynamic_rew_avg_x.png")			

		G.print_pos()