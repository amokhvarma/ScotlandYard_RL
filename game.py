from utilities import *
import random
from utilities import detective,graph_utils,MrX,observation
class game:
    def __init__(self,n=4):
        self.board = graph_utils.graph()
        self.no_of_players = n
        positions = self.board.initial_pos(n+1)
        self.M={13,26,29,34,50,53,91,94,103,112,117,132,138,141,155,174,197,198}

        self.X = MrX.MrX()
        self.detectives = [detective.detective(i) for i in range(0,n)]
        for k in range(0,n):
            self.M.remove(positions[k])
        self.X.set_position(positions[0])
        for i in range(1,n+1):
            self.detectives[i-1].set_position(positions[i])

        self.end_flag = False
        self.move = 0

        self.observation = observation.observation()
        self.X_reward=0
        self.D_reward=0
        return

    def finish(self):
        if(self.move >= 24):
            self.end_flag = True
            self.X_reward+=10
            self.D_reward+=-10
            return self.end_flag

        for i in range(1,self.no_of_players):

            if(self.X.position == self.detectives[i].position):
                self.end_flag = True
                self.X_reward+=-10
                self.D_reward+=10
                return self.end_flag
        self.X_reward+=10
        self.D_reward+=-10
        self.end_flag = False

# Takes action . Target and mode are lists. planning is "random" for now
    def take_action(self,target,type,mode,index,planning = "None"):

        if(type == "detective"):
            agent = self.detectives[index]

            print("Detective ",index," Cards left : ", agent.cards)

            if(planning == "random"):
                (target,mode_new) = self.random_action(type,mode,agent)
                # If there is no viable target, action fails.
                if(target == -1):
                    print("Detective ", index, "Failed ... \n")
                    return (-1,-1,-1,self.end_flag)

                print("Target,Mode : ",target,mode_new)
                agent.take_action(target, mode_new)
            else:
                print("Target,Mode : " , target,mode)
                agent.take_action(target,mode)
                mode_new = mode
            # Update the observation
            self.observation.update_observation(type,index,agent)
            self.D_reward+=self.reward('Detective')
            self.print_reward()

        else:
            print("X Cards left : ", self.X.cards)
            if(planning == "random"):
                (target,mode_new) = self.random_action(type,mode,self.X)
                # No viable actions
                if(target == -1):
                    # Failed moved still counted as move here
                    self.X.moves+=1

                    if(len(mode) > 0 and mode[0]==3):
                        self.X.moves+=1

                    self.move = self.X.moves

                    print("X Failed ..")
                    return (-1,-1,-1,self.end_flag)

                print("Target/Mode : ", target,mode_new)
                self.X.take_action(target, mode_new)
            else:
                print("Target,Mode : ", target,mode)
                mode_new = mode
                self.X.take_action(target,mode)
            self.observation.update_observation(type,index,self.X)

            # ATTENTION : This part is all wrong. You should use mode_new for this. Also mode_new is
            # is a list and contains possibly multiple elements. I have printed self.M , If your correction works,
            # self.M will no longer be empty dictionary. Also, remember that X shows himself in some moves. So you have
            # to empty your self.M

            temp={}
            for i in self.M:
                z=self.board.connections(i)
                if type=='taxi':
                    for j in z[0]:
                        temp.add(j)
                if type=='bus':
                    for j in z[1]:
                        temp.add(j)
                if type=='underground':
                    for j in z[2]:
                        temp.add(j)
            for i in self.detectives:
                if i.position in temp:
                    temp.remove(i.position)
            self.M=temp
            self.X_reward+=self.reward('X')
            self.print_reward()

        reward = 0

        self.move = self.X.moves

        self.finish()
        if(not self.end_flag):
            for i in self.detectives:
                if i.position in self.M:
                    self.M.remove(i.position)

        return (self.observation,reward,self.end_flag)

    def random_action(self,type,mode,agent):
        if(type == "detective"):
            (target,action) = self.choose_random_target(agent)

            if(target < 0):
                return [-1,-1]

            return ([target],[action])

        else:
            if(not mode==[] and mode[0] == 3):
                (target1,action1) = self.choose_random_target(agent,type)
                if(target1 == -1):
                    return [-1,-1]
                (target2,action2) = self.choose_random_target(agent,type)
                if(target2 == -1):
                    return [-1,-1]
                return ([target1,target2],[3,action1,action2])

            else:
                (target1,action1) = self.choose_random_target(agent,type)
                if(target1 == -1):
                    return [-1,-1]
                if(not mode == [] and mode == 4):
                    return ([target1],[4,action1])
                else:
                    return ([target1],[action1])

    def isEmpty(self,node):
        for i in range(0,self.no_of_players):
            if(self.detectives[i].position == node):
                return False

        return True

    def choose_random_target(self,agent,type = "detective"):
        for i in range(0,10):
            # Try actions multiple times
            action = agent.random_action()

            if (action < 0):
                print("No actions left ")
                return (-2, -1)

            l = self.board.connections(agent.position)[action]

            #print(action,self.board.connections(agent.position))

            if(l == []):
                # We retry with a new action
                continue

            if(type == "x"):
                for i in range(0,10):
                    target = random.sample(l, 1)[0]
                    if(self.isEmpty(target)):
                        return (target,action)

            else:
                target = random.sample(l,1)[0]
                return (target,action)

        print("No empty spot")
        return (-1,-1)

    def print_pos(self):
        positions = [x.position for x in self.detectives]
        positions.append(self.X.position)
        print("Positions of Detective and X " ,positions)
        return

    def reward(self,t):
        if t=='Detective':
            m=self.M
            d=self.detectives
            l=[]
            for i in d:
                min=200
                for k in m:
                    # Changed this part because you have used shortest_path instead of shortest_path_length
                    c=self.board.shortest_path(i.position,k)
                    if min<c:
                        c=min
                l.append(1/(min+1))
            return sum(l)
        if t=='X':
            X=self.X.position
            m=self.M
            min=200
            c = 0
            for k in m:
                c=self.board.shortest_path(X,k)
                if min<c:
                    c=min
            return c/20
        return 0
    def print_reward(self):
        print("Reward collected by X is ", self.X_reward)
        print("Reward collected by Detective is ",self.D_reward)
