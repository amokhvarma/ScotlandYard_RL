class MrX:
    # MrX is almost same as detective except he has 2 extra types of cards, multi move (index 3) and hide move  (index 4)
    # Each index 4 move has to be accompanied by the actual move.

    def __init__(self):
        return

    def set_position(self,node_number):
        return


    # Move towards the target node number and throw away the respective card
    def take_action(self,target,start,mode):
        return 1

    # For random action as baseline
    def random_action(self):
        return -1

    # This condition should not arise afaik. Checks if there is any action left.
    def action_left(self):
        return True