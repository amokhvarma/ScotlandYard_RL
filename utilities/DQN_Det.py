import random
from collections import deque
import numpy as np
# import cv2
import os
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader
from utilities.D_net import D_net
import math

glob_loss = []
class QDataset(Dataset):
    def __init__(self, x, y):
        s = os.getcwd()
        self.x = x
        self.y = y
        # self.x=np.load(type+"_data.npy", allow_pickle=True)
        # self.y=np.load(type+'_label.npy',allow_pickle=True)
        self.x = torch.from_numpy(self.x).float()
        self.y = torch.from_numpy(self.y).float()

    def __getitem__(self, index):
        return self.x[index], self.y[index]

    def __len__(self):
        return self.x.shape[0]


# Convert list of actions to form (action,target)
def convert_from_dict(list_of_actions):
    l = []
    li = [[],[],[],[]]
    for i in range(4):
        if len(list_of_actions[i].keys())==0:
            li[i].append([None,None])
        for key in list_of_actions[i].keys():
            for pos in list_of_actions[i][key]:
                li[i].append([key,pos])
    for a in li[0]:
        for b in li[1]:
            for c in li[2]:
                for d in li[3]:
                    l.append([[a[0],b[0],c[0],d[0]],[a[1],b[1],c[1],d[1]]])

    return l


class DQN_Det():

    def __init__(self,lr):
        self.learning_rate = lr
        self.loss = []
        self.epsilon = 0.9
        self.epoch = 1
        self.no_of_games = 4000 # Not sure if we need this
        self.epsilon_decay = (self.epsilon - 0.01) / (self.no_of_games)
        self.batch_size = 32
        self.model = self.build_model()
        self.input_size = 1000  # TODO: We will update this
        # Each element of memory is ([state,action],next_state,reward) format.
        # By [state,action] we mean feature vector. next_state can be an instance of game (deepcopy)
        self.memory = deque(maxlen=1000)
        self.gamma = 0.95  # We can try multiple values if possible i.e
        self.optimizer = optim.Adadelta(self.model.parameters(), lr=self.learning_rate)
        self.scheduler = StepLR(self.optimizer, step_size=1, gamma=1)
        self.no_cuda = True
        self.use_cuda = not self.no_cuda and torch.cuda.is_available()
        self.device = torch.device("cuda" if self.use_cuda else "cpu")
        self.kwargs = {'num_workers': 0, 'pin_memory': True} if self.use_cuda else {}

    def build_model(self):
        model = D_net()
        return model

    def add_to_memory(self, state_action, next_state, reward):
        self.memory.append((state_action, next_state, reward))

        return
    def train_action(self, game):
        rand = random.uniform(0, 1)
        if (rand < self.epsilon):
            action = game.list_of_action_d()
            if (action is None):
                return
            else:
                act=[]
                #print(action)
                list_act = convert_from_dict(action)
                act=random.sample(list_act, 1)[0]
                #print(act)
            return act

        else:
            #print("Exploitation ... ")
            (act, _) = self.best_action(game)
            return act

    def best_action(self, game):
        # TODO : Change Here
        max_reward =-100
        act = None
        action = game.list_of_action_d()
        list_act = convert_from_dict(action)

        for act_tar in list_act:
            # TODO:Shaurya will Implement this
            feature = game.f_d_action(act_tar)
            #  TODO:Ayush Make this correct
            feature_tensor = torch.from_numpy(feature)
            val = self.model.forward(feature_tensor.float()).detach().numpy()[0][0]

            if (val > max_reward):
                max_reward=val
                act=act_tar

        return (act, max_reward)

    def replay(self):
        mini_batch = random.sample(self.memory, self.batch_size)
        x = []
        y = []
        for (state_action, next_state, reward) in mini_batch:
            if (next_state.end_flag):
                target = next_state.D_reward
            else:
                _, max_rew = self.best_action(next_state)
                target = reward + self.gamma * max_rew
            x.append(state_action)
            y.append(target)
        x = np.asarray(x)
        y = np.asarray(y)
        # Assuming I have x,y np arrays with test data
        data = torch.utils.data.DataLoader(QDataset(x, y), batch_size=y.size, shuffle=True, **self.kwargs)
        # TODO : Ayush (.fit trains the file)
        self.loss.append(train(1, self.model, self.device, data, self.optimizer, self.epoch))
        self.epoch += 1
        self.epsilon -= self.epsilon*self.epsilon_decay
        print("Exploration : ",self.epsilon)

    def save_model(self, path):
        torch.save(self.model,path)
        return None

    def load_model(self, path):
        return None

def train(log_interval, model, device, train_loader, optimizer, epoch):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        target = target.view(-1, 1, 1)

        loss = F.mse_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                       100. * batch_idx / len(train_loader), loss.item()))
    return loss.item()


def test(model, device, test_loader):

    model.eval()
    test_loss = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.mse_loss(output, target, reduction='sum').item()  # sum up batch loss

    test_loss /= len(test_loader.dataset)
