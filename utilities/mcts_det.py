import copy
import random
import math

def convert_to_dict(list_of_actions):
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

class Node:
    def __init__(self,game=None,c=2,parent=None):
        self.visits=0
        self.reward=0
        self.child = None
        self.parent = parent
        self.game=game
        self.c = c

    def set_state(self,game):
        self.game=game

    def child_init(self):
        self.child = {}
        for i in range(1,200):
            self.child[(0,i)] = Node(game=None,parent=self)
            self.child[(1,i)] = Node(game=None,parent=self)
            self.child[(2,i)] = Node(game=None,parent=self)

        return

    def simulate_one_step(self,action,index):
        planning = "Normal"
        if(len(action)==0):
            mode = []
            target = None
            planning = "random"
        elif(len(action)==2):
            mode = [action[0]]
            target = [action[1]]
        else:
            mode = [action[0],action[1]]
            target = [action[2]]

        game = copy.deepcopy(self.game)
        for i in range(index,4):
            if(i == index):
                game.take_action(target,"detective",mode,index,planning)
            else:
                game.take_action(None,"detective",[],i,"random")

        game.take_action(None,"x",[],0,"random")
        for i in range(0,index):
            game.take_action(None,"detective",[],i,"random")

        return game

    def ucb1(self,index):
        list_of_actions = self.game.detectives[index].list_actions(self.game.board)
        #print(list_of_actions)
        dict_of_actions = convert_to_dict(list_of_actions)
        val,action = -100,None
        c,N = self.c ,self.visits
        for key in self.child.keys():
            if(key not in dict_of_actions):
                continue
            if(self.child[key].visits == 0):
                action = key
                break
            else:
                if(N > 0):
                    node_val = self.child[key].reward + c*math.sqrt(math.log(N)/self.child[key].visits)
                else:
                    #val = node_val
                    action = key
                    break
                if(node_val > val):
                    val = node_val
                    action = key
        #print(action)
        return action

class mcts_det:
    def __init__(self, game, index=1, c=2, playouts=10,agent=None):
        self.game = copy.deepcopy(game)
        self.c = c
        self.index=index
        print("Monte Carlo Tree Search for det ")
        self.root = Node(self.game, self.c)
        self.playouts = playouts

    def best_action(self):
        max_rew,best_action,target = -200,None,None
        list_of_keys =  convert_to_dict(self.root.game.detectives[self.index].list_actions(self.root.game.board))
        hiddenlist = []
        #print(list_of_keys)
        #print([(self.root.child[key].reward,self.root.child[key].visits,key) for key in self.root.child.keys() if not self.root.child[key].reward==0])
        for key in self.root.child.keys():
            if(key not in list_of_keys):
                continue
            if(self.game.move in hiddenlist):
                if(self.root.child[key].reward > max_rew):
                    max_rew = self.root.child[key].reward

                    best_action = [key[0]]
                    target = [key[1]]
                    if(best_action == [4]):
                        best_action = [key[0],key[1]]
                        target = [key[2]]
            else:
                if(self.root.child[key].reward > max_rew and [key[0]]!=[4]):
                    max_rew = self.root.child[key].reward

                    best_action = [key[0]]
                    target = [key[1]]
                    # if(best_action == [4]):
                    #     best_action = [key[0],key[1]]
                    #     target = [key[2]]
        if(best_action == None):
            return (-1,-1)
        else:
            return (best_action,target)

    def planning(self):
        # playouts = 10
        for temp in range(0,self.playouts):
            print("\n Playout Number : ", temp)
            iter_node = self.root

            # Select Node
            while iter_node.child is not None:
                action = iter_node.ucb1(self.index)
                if(action is None):
                    break
                next_state = iter_node.simulate_one_step(action,self.index)
                iter_node.child[action].set_state(next_state)

                iter_node = iter_node.child[action]
            #print(iter_node.parent==self.root)
            # Expand Node :-
            if(not iter_node.game.finish()):
                iter_node.child_init()
                rand_action = iter_node.ucb1(self.index)
                if(not rand_action==None):
                    iter_node.child[rand_action].set_state(iter_node.simulate_one_step(rand_action,self.index))
                    iter_node = iter_node.child[rand_action]
            #print(iter_node.parent.parent==self.root)
            # Two possibilities : node cannot be expanded / can be expanded
            reward = self.simulate(iter_node)

            # Backprop from the node
            self.backprop(iter_node,reward)
        #print(self.root.reward)
        return self.best_action()

    def simulate(self,node):
        print("Simulation..")
        G = copy.deepcopy(node.game)
        G.take_action(None, "x", [], 0, "random")
        for i in range(0, self.index):
            G.take_action(None, "detective", [], i, "random")

        while(not G.finish()):
            action = []
            x_cards = len(G.X.cards)
            r = random.randint(0,x_cards)

            G.take_action(None,"x",action,0,"random")
            for i in range(0, 4):
                G.take_action(None,"detective", [], i, "random")

        return G.return_reward()[1]


    def backprop(self,node,reward):
        print("Backprop : ",node.reward)
        while(not node == None):
            node.reward = (node.visits*node.reward+reward)/(node.visits+1)
            node.visits+=1
            node = node.parent
            #print("*******************************************************************")
        return 0