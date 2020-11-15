class observation:
   # n is the number of people
    def __init__(self,n=4):
        #  Positions of all detectives
        self.positions_detective = [[] for i in range(n-1)]
        # Number of cards left for each detective. Each element is an array of number of cards of each transport left
        self.cards_left = [[] for i in range(n-1)]
        # Positions of x whenever he resurfaces
        self.positions_x = []
        # List of cards played by MrX
        self.x_moves = []

    def update_observation(self,type,index,agent):
        # I think we will not needed the action history of detectives as we have position histories.

        if(type == "detective"):
            self.positions_detective[index].append(agent.position)
            self.cards_left[index] = agent.cards
        else:
            if(agent.observable):
                self.positions_x.append(agent.position)
            else:
                self.positions_x.append(-1)

            if(agent.previous_move):
                self.x_moves.append(agent.previous_move)

        return

