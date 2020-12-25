import random
import numpy as np

class MrX:
	# MrX is almost same as detective except he has 2 extra types of cards, multi move (index 3) and hide move  (index 4)
	# Each index 4 move has to be accompanied by the actual move.

	def __init__(self):
		self.cards = [10,6,4,0,2]
		self.previous_move = None
		self.moves = 0
		return

	def set_position(self,node_number):
		self.position = node_number
		print("X moved to " , node_number)
		return

	# Move towards the target node number and throw away the respective card
	# target and mode are lists , even if single element.
	def take_action(self,target,mode):
		if (-1<mode[0]<3):
			success = 1
			if(self.cards[mode[0]] > 0):
				self.cards[mode[0]] -= 1
				self.previous_move = mode[0]
				self.moves += 1
				self.set_position(target[0])

			else:
				self.moves+=1

				print("Not enough Tickets left")
				return -1

		elif (mode[0] == 3):
			success = self.take_action3(target[0], target[1], mode[1], mode[2])
		elif(mode[0] == 4):

			success = self.take_action4(target[0],mode[1])

		return success

	def take_action3(self,target1,target2,mode1,mode2):

		if(mode1>2 or mode2>2):
			return -1
		elif(self.cards[3] > 0):
			self.cards[3] -= 1
			self.previous_move = [mode1,mode2]
			self.take_action([target1],[mode1])
			self.take_action([target2],[mode2])
		else:
			print("Not enough Tickets left")
			return -1
		return 1

	def take_action4(self,target,mode):
		if(mode==3):
			return -1
		elif(self.cards[4] > 0):
			self.cards[4] -= 1
			self.take_action([target],[mode])
		# Move not visible
			self.previous_move = -1
		else:
			print("Not enough Tickets left")
			return -1
		return 1            

	# For random action as baseline
	def random_action(self):
		if(self.action_left()):
			while True:
				k = random.randint(0,2)
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
		# Number of moves = self.moves - (3-self.cards[3])
		if((self.moves + self.cards[3] - 3)%3==0):
			vis = True
		return vis

	def list_actions(self,board,detectives):
		connections = board.connections(self.position)
		action = {}
		for i in range(0,5):
			if(self.cards[i]<=0):
				continue
			if(i<3):
				action[i] = []
				for pos in connections[i]:
					if(pos not in det.position for det in detectives):
						action[i].append(pos)

				if(len(action[i])==0):
					action.pop(i)
			elif(i==4):
				action[i] = []
			else:
				print("")

		return action

