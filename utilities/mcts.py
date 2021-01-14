import copy
import random
import math
import game

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
            self.child[(4,0,i)] = Node(game=None,parent=self)
            self.child[(4,1,i)] = Node(game=None,parent=self)
            self.child[(4,2,i)] = Node(game=None,parent=self)

        return

    def simulate_one_step(self,action):
        if(len(action)==2):
            mode = [action[0]]
            target = [action[1]]
        else:
            mode = [action[0],action[1]]
            target = [action[2]]
        game = copy.deepcopy(self.game)
        game.take_action(target,"x",mode,0)
        for i in range(0,4):
            game.take_action(None,"detective",[],i,"random")

        return game

    def ucb1(self):
        list_of_actions = self.game.list_of_action_x()
        print(list_of_actions)
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
        print(action)
        return action

class mcts:
    def __init__(self, game, c=2, playouts=10, agent=None):
        self.game = copy.deepcopy(game)
        self.c = c
        print("Monte Carlo Tree Search for X ")
        self.root = Node(self.game, self.c)
        self.playouts = playouts

    def best_action(self):
        max_rew,best_action,target = -200,None,None
        list_of_keys =  convert_to_dict(self.root.game.list_of_action_x())
        #print(list_of_keys)
        print([(self.root.child[key].reward,self.root.child[key].visits,key) for key in self.root.child.keys() if not self.root.child[key].reward==0])
        for key in self.root.child.keys():
            if(key not in list_of_keys):
                continue
            if(self.root.child[key].reward > max_rew):
                max_rew = self.root.child[key].reward

                best_action = [key[0]]
                target = [key[1]]
                if(best_action == [4]):
                    best_action = [key[0],key[1]]
                    target = [key[2]]
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
                action = iter_node.ucb1()
                if(action is None):
                    break
                next_state = iter_node.simulate_one_step(action)
                iter_node.child[action].set_state(next_state)

                iter_node = iter_node.child[action]
            print(iter_node.parent==self.root)
            # Expand Node :-
            if(not iter_node.game.finish()):
                iter_node.child_init()
                rand_action = iter_node.ucb1()
                if(not rand_action==None):
                    iter_node.child[rand_action].set_state(iter_node.simulate_one_step(rand_action))
                    iter_node = iter_node.child[rand_action]
            print(iter_node.parent.parent==self.root)
            # Two possibilities : node cannot be expanded / can be expanded
            reward = self.simulate(iter_node)

            # Backprop from the node
            self.backprop(iter_node,reward)
        print(self.root.reward)
        return self.best_action()

    def simulate(self,node):
        print("Simulation..")
        G = copy.deepcopy(node.game)

        while(not G.finish()):
            action = []
            x_cards = len(G.X.cards)
            r = random.randint(0,x_cards)
            if(r<G.X.cards[4]):
                action = [4]
            G.take_action(None,"x",action,0,"random")
            for i in range(0, 4):
                G.take_action(None,"detective", [], i, "random")

        return G.return_reward()[0]


    def backprop(self,node,reward):
        print("Backprop : ",node.reward)
        while(not node == None):
            node.reward = (node.visits*node.reward+reward)/(node.visits+1)
            node.visits+=1
            node = node.parent
            print("*******************************************************************")
        return 0

