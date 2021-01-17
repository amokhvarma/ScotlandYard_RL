import torch
from copy import deepcopy
import sys
from utilities.DQN_Agent import DQN_Agent
from game import game
from utilities.mcts_det import mcts_det
import time
import matplotlib.pyplot as plt

try:
    lr = float(sys.argv[2])
except:
    lr = 1.0
try:
    playouts = int(sys.argv[1])
except:
    playouts = 10000
try:
    model_name = sys.argv[3]
except:
    model_name = "X_DQNN_det_mcts"

print(lr,playouts,model_name)

surv = []
win_rate = []
iter = 1
X_agent = DQN_Agent(lr)
total_steps = 0
while (iter <= playouts):
    G = game()
    step_rew, rew = 0, 0
    while (not G.finish()):
        print("Move No ", G.move, "\n")
        # print(G.list_of_action_x())
        act = X_agent.train_action(G)
        state_action = G.f_x_action(act)
        if (act[0] == 4):
            mode = [act[0], act[1]]
            target = [act[2]]
        else:
            mode = [act[0]]
            target = [act[1]]
        # print(act)
        G.take_action(target, "x", mode, 0)
        total_steps += 1
        print("\n")
        for i in range(G.no_of_players):
            if (len(G.detectives[i].list_actions(G.board)) == 0 or G.end_flag):
                print("Detective  Failed ")
                continue
            p = mcts_det(G, i, 2, 3)

            (action, target) = p.planning()

            G.take_action(target[0], "detective", action[0], i, "random")
            print("\n")
        G.update_fv()
        step_rew = G.X_reward - rew
        rew = G.X_reward
        next_state = deepcopy(G)

        X_agent.add_to_memory(state_action, next_state, step_rew)
        print(rew, step_rew)
        if (total_steps % X_agent.batch_size == 0):
            print("Replaying ... ")
            X_agent.replay()
    iter += 1
    if (G.move >= 20):
        surv.append(1)
    else:
        surv.append(0)
    win_rate.append(sum(surv) / len(surv))
    if (iter % 2000 == 0):
        X_agent.save_model("Model/" + model_name)
        plot1 = plt.figure(1)
        plt.plot(X_agent.loss)
        plt.title("Loss vs Episodes")
        plt.xlabel("Episode")
        plt.ylabel("MSE Loss in Q value")
        plt.savefig("Result/" + model_name + "_loss.png")

        plot2 = plt.figure(2)
        plt.title("Win rate vs Episodes")
        plt.xlabel("Episode")
        plt.ylabel("Win rate ")

        plt.plot(win_rate)
        plt.savefig("Result/" + model_name + "_win_rate.png")

    G.print_pos()
print(len(X_agent.memory))
