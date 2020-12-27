#import pytorch as torch
import random
from collections import deque
# Convert list of actions to form (action,target)
def convert_from_dict(list_of_actions):
    l = []
    for key in list_of_actions.keys():
        if(key < 3):
            for pos in list_of_actions[key]:
                l.append((key,pos))

        else:
            for i in list_of_actions.keys():
                if(i==4):
                    break
                for pos in list_of_actions[i]:
                    l.append((4,i,pos))

    return l

class DQN_Agent():
    def __init__(self):
        self.learning_rate = 0.1
        self.epsilon = 0.9
        self.no_of_games = 200 # Not sure if we need this
        self.epsilon_decay = (self.epsilon-0.01)/(self.no_of_games)
        self.batch_size = 32
        self.model = self.build_model
        self.input_size = 1000 # TODO: We will update this
        # Each element of memory is ([state,action],next_state,reward) format.
        # By [state,action] we mean feature vector. next_state can be an instance of game (deepcopy)
        self.memory = deque(maxlen=1000)
        self.gamma = 0.95 # We can try multiple values if possible i.e.


    def build_model(self):
        # TODO:Ayush Build model here
        model = 0
        return model

    def add_to_memory(self,state_action,next_state,reward):
        self.memory.append((state_action,next_state,reward))
        return
    # Chooses next step , accounting for exploitation vs exploration
    def train_action(self,game,type = "x"):
        rand = random.random(0,1)
        if(rand < self.epsilon):
            action = game.list_of_action_x()
            if(action is None):
                return
            else:
                list_act = convert_from_dict(action)
                act = random.sample(list_act,1)[0]

            return act

        else:
            (act,_) = self.best_action(game,type)
            return act

    def best_action(self,game,type="x"):
        # TODO : Change Here
        max_reward = -100
        act = None
        action = game.list_of_action_x()
        list_act = convert_from_dict(action)
        for act_tar in list_act:
            # TODO:Shaurya will Implement this
            feature = game.f_x_action(act_tar)

            #  TODO:Ayush Make this correct
            val = self.model.predict(feature)

            if (val > max_reward):
                max_reward = val
                act = act_tar

        return (act,max_reward)


    def replay(self):
        mini_batch = random.sample(self.memory,self.batch_size,type="x")
        for (state_action,next_state,reward) in mini_batch:
            if(next_state.end_flag):
                target = next_state.X_reward
            else:
                _,max_rew = self.best_action(next_state,type)
                target = reward + self.gamma*max_rew

            # TODO : Ayush (.fit trains the file)
            self.model.fit(state_action,target,epochs=1,verbose=0)

        self.epsilon = self.epsilon*self.epsilon_decay

    # TODO: Save and load to self.model

    def save_model(self,path):
        return None

    def load_model(self,path):
        return None




