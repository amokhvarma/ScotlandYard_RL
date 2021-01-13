from utilities import MrX,detective,observation,graph_utils
import numpy as np
import matplotlib.pyplot as plt
import game
from utilities import mcts
#

reward_x,victory = [],0
reward_d=[]
l=[]
l1=[]
l2=[]
for it in range(0,2000):
# Start the run
    G = game.game()
    type = ["detective","x"]
    hide_move = [3,6,9]
    multi_move = []
    #print("\n ################### START GAME ########################################")
    #print(G.M)
    while(not G.finish()):
        move_no = G.move
        #print("List of actions ", G.X.list_actions(G.board,G.detectives))
        #print("\nMove No", move_no + 1, "Start -------------------------------------------------------------- \n")
        if(move_no in hide_move):
            (_,rew,_,_)=G.take_action(None,type[1],[4],0,"random")
            #print('\n')
        elif(move_no in multi_move):
            #print("Multi Move")
            (_,rew,_,_)=G.take_action(None,type[1],[3],0,"random")
            #print('\n')
        else:
            (_,rew,_,_)=G.take_action(None,type[1],[],0,"random")
            #print("\n")
        for i in range(0,4):
            #print("Detective ", i, "taking action .. ")
            (_,rew,_,_)=G.take_action(None,type[0],[],i,"random")
            #print("\n")
        G.update_fv()
        #print(G.f_x_action((2,24)).shape)
        #G.print_pos()
        #G.print_reward()

        #print("\nMove No" ,move_no+1, "Over -------------------------------------------------------------- \n")
    reward_x.append(G.X_reward)
    reward_d.append(G.D_reward)
    if(G.move >= 19):
        victory+=1
        if it>0:
            l.append((len(l)*l[len(l)-1]+1)/(len(l)+1))
        else:
            l.append(1)
    else:
        if it>0:
            l.append((len(l)*l[len(l)-1])/(len(l)+1))
        else:
            l.append(0)
    if it>0:
        l1.append((len(l1)*l[len(l1)-1]+G.X_reward)/(len(l1)+1))
        l2.append((len(l2)*l[len(l2)-1]+G.D_reward)/(len(l2)+1))
    else:
        l1.append(G.X_reward)
        l2.append(G.D_reward)

print(victory,np.mean(reward_x))
plt.figure(0)
plt.plot(l1[100:])
plt.xlabel("Run")
plt.ylabel("Mean Reward for X")
zt=[]
for jt in range(41):
    zt.append(-1+jt*0.05)
# plt.title("Reward for X with Random Policies")
y_axis = [x for x in range(-15,25,5)]
x_axis = [x for x in range(1,2001,100)]
#plt.yticks(zt)
plt.xticks(x_axis)
plt.savefig("Result.png")
plt.figure(1)
plt.plot(l[100:])
plt.xlabel("Run")
plt.ylabel("Win ratio for X")
zt=[]
for jt in range(41):
    zt.append(jt*0.025)
# plt.title("Reward for X with Random Policies")
#y_axis = [x for x in range(0,1,0.05)]
x_axis = [x for x in range(1,2001,100)]
#plt.yticks(zt)
plt.xticks(x_axis)
plt.savefig("Result1.png")

plt.figure(2)
plt.plot(l2[100:])
plt.xlabel("Run")
plt.ylabel("Mean Reward for D")
zt=[]
for jt in range(41):
    zt.append(jt*0.025)
# plt.title("Reward for X with Random Policies")
#y_axis = [x for x in range(0,1,0.05)]
x_axis = [x for x in range(1,2001,100)]
#plt.yticks(zt)
plt.xticks(x_axis)
plt.savefig("Result2.png")

plt.figure(3)
plt.plot(reward_x[100:])
plt.xlabel("Run")
plt.ylabel("Reward for X")
zt=[]
for jt in range(41):
    zt.append(jt*0.025)
# plt.title("Reward for X with Random Policies")
#y_axis = [x for x in range(0,1,0.05)]
x_axis = [x for x in range(1,2001,100)]
#plt.yticks(zt)
plt.xticks(x_axis)
plt.savefig("Result3.png")

plt.figure(4)
plt.plot(reward_d[100:])
plt.xlabel("Run")
plt.ylabel("Reward for D")
zt=[]
for jt in range(41):
    zt.append(jt*0.025)
# plt.title("Reward for X with Random Policies")
#y_axis = [x for x in range(0,1,0.05)]
x_axis = [x for x in range(1,2001,100)]
#plt.yticks(zt)
plt.xticks(x_axis)
plt.savefig("Result4.png")
print(l)
print(l1)
print(l2)
