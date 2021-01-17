import torch
from copy import deepcopy
import sys
from utilities.DQN_Agent import DQN_Agent
from game import game
import time
import matplotlib.pyplot as plt
playouts = int(sys.argv[1])
model_name = sys.argv[3]
lr = float(sys.argv[2])
surv = []
win_rate = []
iter = 1
X_agent = DQN_Agent(lr)
total_steps = 0
while(iter<=playouts):
    G = game()
    step_rew,rew=0,0
    while(not G.finish()):
        print("Move No ", G.move,"\n")
        #print(G.list_of_action_x())
        act = X_agent.train_action(G)
        state_action = G.f_x_action(act)
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
            #print("\n")
        G.update_fv()
        step_rew = G.X_reward-rew
        rew = G.X_reward
        next_state = deepcopy(G)

        X_agent.add_to_memory(state_action,next_state,step_rew)
        print(rew,step_rew)
        if(total_steps%X_agent.batch_size == 0):
            print("Replaying ... ")
            X_agent.replay()
    iter+=1
    if(G.move>=20):
        surv.append(1)
    else:
        surv.append(0)
    win_rate.append(sum(surv)/len(surv))
    if(iter%2000== 0):
        X_agent.save_model("Model/"+model_name)
        plot1 = plt.figure(1)
        plt.plot(X_agent.loss)
        plt.title("Loss vs Episodes")
        plt.xlabel("Episode")
        plt.ylabel("MSE Loss in Q value")
        plt.savefig("Result/loss.png")

        plot2 = plt.figure(2)
        plt.title("Win rate vs Episodes")
        plt.xlabel("Episode")
        plt.ylabel("Win rate ")

        plt.plot(win_rate)
        plt.savefig("Result/win_rate.png")

    G.print_pos()
print(len(X_agent.memory))
