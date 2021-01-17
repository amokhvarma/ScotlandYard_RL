import torch
from copy import deepcopy
import sys
import os
from utilities.DQN_Det import DQN_Det
from utilities.DQN_Agent import DQN_Agent
from game import game
import time
import matplotlib.pyplot as plt
playouts = int(sys.argv[1])
model_name = str(sys.argv[3])
lr = float(sys.argv[2])
surv = []
win_rate_X = []
iter = 1
D_agent = DQN_Det()
D_agent.load_model("/content/ScotLandYard_RL/Model/DQNN_Det")
X_agent = DQN_Agent(lr)
total_steps = 0
while(iter<=playouts):
	G = game()
	step_rew,rew=0,0
	step_rew_X,rew_X=0,0
	while(not G.finish()):
		#print("Move No ", G.move ,iter)
		#print(G.list_of_action_x())
		act = D_agent.train_action(G)
		state_action = G.f_d_action(act)
		act_X = X_agent.train_action(G)
		# print(act_X)
		state_action_X = G.f_x_action(act_X)
		if(act_X[0] == 4):
			mode = [act_X[0],act_X[1]]
			target = [act_X[2]]
		else:
			mode = [act_X[0]]
			target = [act_X[1]]
		# print(act)
		G.take_action(target,"x",mode,0)
		for i in range(4):
			if act[0][i]!=None:
				G.take_action([act[1][i]],"detective",[act[0][i]],i)
		total_steps+=1
		G.update_fv()
		step_rew = G.D_reward-rew
		rew = G.D_reward
		step_rew_X = G.X_reward-rew_X
		rew_X = G.X_reward
		next_state = deepcopy(G)

		D_agent.add_to_memory(state_action,next_state,step_rew)
		X_agent.add_to_memory(state_action_X,next_state,step_rew_X)
		#print(rew,step_rew)
		'''if(total_steps%D_agent.batch_size == 0):
			print("Replaying ... ")
			D_agent.replay()'''
		if(total_steps%X_agent.batch_size == 0):
			print("Replaying ... ")
			X_agent.replay()
	print(iter)
	iter+=1
	if(G.move>=20):
		surv.append(1)
	else:
		surv.append(0)
	win_rate_X.append(sum(surv)/len(surv))
	if(iter%100 == 0):
		#D_agent.save_model("Model/"+model_name+"_det")
		X_agent.save_model("/content/drive/MyDrive/ScotLand_Yard/"+model_name)

		plot1 = plt.figure(1)
		#print(D_agent.loss)
		plt.plot(X_agent.loss)
		plt.title("X Loss vs Episodes")
		plt.xlabel("Episode")
		plt.ylabel("MSE Loss for X in Q value")
		plt.savefig("/content/drive/MyDrive/ScotLand_Yard/loss_X_adv.png")

		plot2 = plt.figure(2)
		plt.title("Win rate of X vs Episodes")
		plt.xlabel("Episode")
		plt.ylabel("Win rate of X")
		plt.plot(win_rate_X)
		plt.savefig("/content/drive/MyDrive/ScotLand_Yard/win_rate_X_adv.png")

		plot3 = plt.figure(3)
		plt.plot(D_agent.loss)
		plt.title("Det Loss vs Episodes")
		plt.xlabel("Episode")
		plt.ylabel("MSE Loss for Dets in Q value")
		plt.savefig("/content/drive/MyDrive/ScotLand_Yard/loss_dets_adv.png")

	#G.print_pos()
print(len(X_agent.memory),X_agent.loss)
