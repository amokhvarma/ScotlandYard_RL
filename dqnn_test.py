import torch
from copy import deepcopy
import sys
from utilities.DQN_Agent import DQN_Agent
from game import game
import time
import matplotlib.pyplot as plt

def mean(x):
    return sum(x)/len(x)

playouts = 500
model_name = sys.argv[1]
surv = []
X_reward = []
avg_x,avg_det = [],[]
det_reward = []
win_rate = []
iter = 1
X_agent = DQN_Agent()
X_agent.load_model("Model/"+(model_name))
total_steps = 0
while (iter <= playouts):
    G = game()
    step_rew, rew = 0, 0
    while (not G.finish()):
        print("Move No ", G.move, "\n")
        # print(G.list_of_action_x())
        (act,_) = X_agent.best_action(G)
        state_action = G.f_x_action(act)
        if (act[0] == 4):
            mode = [act[0], act[1]]
            target = [act[2]]
        else:
            mode = [act[0]]
            target = [act[1]]
        print(act)
        G.take_action(target, "x", mode, 0)
        total_steps += 1
        print("\n")
        for i in range(G.no_of_players):
            G.take_action(None, "detective", [], i, "random")
            print("\n")
        G.update_fv()
        step_rew = G.X_reward - rew
        rew = G.X_reward
        next_state = deepcopy(G)

        X_agent.add_to_memory(state_action, next_state, step_rew)
        print(rew, step_rew)

    iter += 1
    if (G.move >= 20):
        surv.append(1)
    else:
        surv.append(0)

    win_rate.append(sum(surv) / len(surv))
    X_reward.append(G.X_reward)
    det_reward.append(G.D_reward/4)
    avg_x.append(mean(X_reward))
    avg_det.append(mean(det_reward))

plot1 = plt.figure(1)

plt.title("Win rate vs Episodes")
plt.xlabel("Episode")
plt.ylabel("Win rate ")
plt.plot(win_rate)
plt.savefig("Result/win_rate_"+sys.argv[1]+".png")

plot2 = plt.figure(2)
plt.title("X Reward vs Episodes")
plt.xlabel("Episode")
plt.ylabel("Reward ")
plt.plot(avg_x)
plt.plot(avg_det)
plt.legend(["X","Detectives"])
plt.savefig("Result/reward_"+sys.argv[1]+".png")

