import random
import numpy as np

class MrX:
    # MrX is almost same as detective except he has 2 extra types of cards, multi move (index 3) and hide move  (index 4)
    # Each index 4 move has to be accompanied by the actual move.

    def initX(self):
        self.cards = [3,3,3,3,2]
        self.previous_move = None
        self.moves = 0
        return

    def set_position(self,node_number):
        self.position = node_number
        return

    # Move towards the target node number and throw away the respective card
    def take_action(self,target,start,mode):
        if (-1<mode<3):
            if(self.cards[mode] > 0):
                self.cards[mode] -= 1
                self.previous_move = mode
                self.moves += 1
            else:
                print("Not enough Tickets left")
                return -1
            self.set_position(self,target)
            start = target
        return 1

    def take_action3(self,target1,target2,start,mode1,mode2):
        if(mode1>2 or mode2>2):
            return -1
        elif(self.cards[3] > 0):
            self.cards[3] -= 1
            take_action(self,target1,start,mode1)
            take_action(self,target2,start,mode2)
            self.moves -= 1
        else:
            print("Not enough Tickets left")
            return -1
        return 1

    def take_action4(self,target,start,mode):
        if(mode==3):
            return -1
        elif(self.cards[4] > 0):
            self.cards[4] -= 1
            take_action(self,target,start,mode)
            self.previous_move = 4
        else:
            print("Not enough Tickets left")
            return -1
        return 1            

    # For random action as baseline
    def random_action(self):
        if(self.action_left()):
            while True:
                k = random.randint(0,len(self.cards)-1)
                if(self.cards[k]>0):
                    return k
        return -1

    # This condition should not arise afaik. Checks if there is any action left.
    def action_left(self):
        check = False
        for x in self.cards:
            if(x > 0):
                check = True
                break
        return check

    def visibility(self):
        vis = False
        if(self.moves%3==0):
            vis = True
        return vis
