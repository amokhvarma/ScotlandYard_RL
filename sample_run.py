from utilities import MrX,detective,observation,graph_utils
import numpy as np
import matplotlib.pyplot as plt
import game
from utilities import mcts
#

reward_x,victory = [],0
for i in range(0,1):
# Start the run
    G = game.game()
    type = ["detective","x"]
    hide_move = [3,6,9]
    multi_move = []
    print("\n ################### START GAME ########################################")
    print(G.M)
    while(not G.finish()):
        move_no = G.move
        print("List of actions ", G.X.list_actions(G.board,G.detectives))
        print("\nMove No", move_no + 1, "Start -------------------------------------------------------------- \n")
        if(move_no in hide_move):
            (_,rew,_,_)=G.take_action(None,type[1],[4],0,"random")
            print('\n')
        elif(move_no in multi_move):
            print("Multi Move")
            (_,rew,_,_)=G.take_action(None,type[1],[3],0,"random")
            print('\n')
        else:
            (_,rew,_,_)=G.take_action(None,type[1],[],0,"random")
            print("\n")
        for i in range(0,4):
            print("Detective ", i, "taking action .. ")
            (_,rew,_,_)=G.take_action(None,type[0],[],i,"random")
            print("\n")
        G.update_fv()
        print(G.f_x_action((2,24)).shape)
        G.print_pos()
        G.print_reward()
        if(move_no >= 19):
            victory+=1
        print("\nMove No" ,move_no+1, "Over -------------------------------------------------------------- \n")
    reward_x.append(G.X_reward)
print(victory,np.mean(reward_x))
plt.plot(reward_x)
plt.xlabel("Run")
plt.ylabel("Reward for X")
# plt.title("Reward for X with Random Policies")
y_axis = [x for x in range(-40,40,5)]
x_axis = [x for x in range(1,21)]
plt.yticks(y_axis)
plt.xticks(x_axis)
plt.savefig("Result.png")
