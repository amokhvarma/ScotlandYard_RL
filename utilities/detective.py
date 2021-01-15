import random


class detective:
    def __init__(self, index):
        # Order is Taxi,Bus,Underground
        # self.cards = {"Taxi":10, "Bus":6, "Underground":4}. Not initialised as per the game

        self.cards = [10, 6, 4]
        self.index = index
        self.previous_move = None

    # We can change to node object if necessary
    def set_position(self, node_number):
        self.position = node_number
        #print("Detective ", self.index, "moved to ", node_number)

    # Move towards the target node number and throw away the respective card

    def take_action(self, target, mode):

        if (self.cards[mode[0]] > 0):
            self.cards[mode[0]] -= 1
            self.previous_move = mode[0]
        else:
            print("Not enough Tickets left")
            return -1

        self.set_position(target[0])
        # print(" Action Taken is : " , mode[0])

        return 1

    # For random action as baseline
    def random_action(self):
        if (self.action_left()):
            for i in range(10):
                k = random.randint(0, len(self.cards) - 1)
                if (self.cards[k] > 0):
                    return k
        return -1

    # This condition should not arise afaik
    def action_left(self):
        check = False
        for x in self.cards:
            if (x > 0):
                check = True
                break
        return check

    def list_actions(self, board, detectives):
        connections = board.connections(self.position)
        action = {}
        for i in range(0, 3):
            if (self.cards[i] <= 0):
                continue
            action[i] = []
            for pos in connections[i]:
                # if(pos not in det.position for det in detectives):
                action[i].append(pos)

            if (len(action[i]) == 0):
                action.pop(i)

        return action
