from utilities import *
from utilities import detective,graph_utils,MrX,observation
class game:
   def __init__(self,n=4):
      self.board = graph_utils.graph()
      self.no_of_players = n
      positions = graph_utils.initial_pos()

      self.X = MrX.MrX()
      self.detectives = [detective.detective()]

      self.X.set_position(positions[0])
      for i in range(1,n+1):
         self.detectives[i-1].set_position(positions[i])

      self.end_flag = False
      self.move = 0

      self.observation = observation.observation()
      return

   def finish(self):
     for i in range(1,self.no_of_players):
        if(self.X.position == self.detectives[i].position):
           self.end_flag = True
           return self.end_flag

     return False
