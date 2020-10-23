import random
class detective:
    def __init__(self,index):
        # Order is Taxi,Bus,Underground
        # self.cards = {"Taxi":10, "Bus":10, "Underground" : 10}. Not initialised as per the game

        self.cards = [10,10,10]
        self.index = index
        self.previous_move = None

    # We can change to node object if necessary
    def set_position(self,node_number):
        self.position = node_number


    # Move towards the target node number and throw away the respective card
    def take_action(self,target,start,mode):

        if(self.cards[mode] > 0 ):
            self.cards[mode] -= 1
            self.previous_move = mode
        else:
            print("Not enough Tickets left")
            return -1

        self.set_position(target)

        return 1

    # For random action as baseline
    def random_action(self):
        if(self.action_left()):
            while True:
                k = random.randint(0,len(self.cards)-1)
                if(self.cards[k]>0):
                    return k
        return -1

    # This condition should not arise afaik
    def action_left(self):
        check = False
        for x in self.cards:
            if(x > 0):
                check = True
                break
        return check