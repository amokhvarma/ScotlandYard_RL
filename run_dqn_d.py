import torch
from copy import deepcopy
import sys
import os
from utilities.DQN_Det import DQN_Det
from game import game
import time
import matplotlib.pyplot as plt
playouts = int(sys.argv[1])
model_name = str(sys.argv[3])
lr = float(sys.argv[2])
surv = []
win_rate = []
iter = 1
D_agent = DQN_Det(lr)
total_steps = 0
while(iter<=playouts):
    G = game()
    step_rew,rew=0,0
    while(not G.finish()):
        #print("Move No ", G.move ,iter)
        #print(G.list_of_action_x())
        act = D_agent.train_action(G)
        state_action = G.f_d_action(act)
        G.take_action(None,"x",[],0,"random")
        for i in range(4):
            if act[0][i]!=None:
                G.take_action([act[1][i]],"detective",[act[0][i]],i)
        total_steps+=1
        G.update_fv()
        step_rew = G.D_reward-rew
        rew = G.D_reward
        next_state = deepcopy(G)

        D_agent.add_to_memory(state_action,next_state,step_rew)
        #print(rew,step_rew)
        if(total_steps%D_agent.batch_size == 0):
            print("Replaying ... ")
            D_agent.replay()
    print(iter)
    iter+=1
    if(G.move>=20):
        surv.append(0)
    else:
        surv.append(1)
    win_rate.append(sum(surv)/len(surv))
    if(iter%playouts== 0):
        D_agent.save_model("Model/"+model_name)
        plot1 = plt.figure(1)
        #print(D_agent.loss)
        plt.plot(D_agent.loss)
        plt.title("Loss vs Episodes")
        plt.xlabel("Episode")
        plt.ylabel("MSE Loss in Q value")
        plt.savefig("Result\\loss_D2.png")

        plot2 = plt.figure(2)
        plt.title("Win rate vs Episodes")
        plt.xlabel("Episode")
        plt.ylabel("Win rate ")

        plt.plot(win_rate)
        plt.savefig("Result\\win_rate_D2.png")

    #G.print_pos()
print(len(D_agent.memory),D_agent.loss)