import torch
from copy import deepcopy
import sys
from utilities.DQN_Agent import DQN_Agent
from game import game
import time

playouts = int(sys.argv[1])
model_name = "D_DQNN"
lr = float(sys.argv[2])

iter = 1
D_agent = DQN_Det(lr)
total_steps = 0
while(iter<=playouts):
    G = game()
    step_rew,rew=0,0
    while(not G.finish()):
        print("Move No ", G.move,"\n")
        #print(G.list_of_action_x())
        act = D_agent.train_action(G)
        state_action = G.f_d_action(act)
        G.take_action(None,"x",[],0,"random")
        print("\n")
        for i in range(4):
            G.take_action([act[1][i]],"detective",[act[0][i]],i)
            print("\n")
        total_steps+=1
        G.update_fv()
        step_rew = G.D_reward-rew
        rew = G.D_reward
        next_state = deepcopy(G)

        D_agent.add_to_memory(state_action,next_state,step_rew)
        print(rew,step_rew)
        if(total_steps%D_agent.batch_size == 0):
            print("Replaying ... ")
            D_agent.replay()
    iter+=1
    if(iter%2000== 0):
        D_agent.save_model("Model/"+model_name)
    G.print_pos()
print(len(D_agent.memory),D_agent.loss)
