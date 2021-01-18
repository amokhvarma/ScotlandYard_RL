from utilities import MrX,detective,observation,graph_utils
import numpy as np
import matplotlib.pyplot as plt
import game
from utilities import mcts
import pygame
#

reward_x,victory = [],0
for i in range(0,1):
# Start the run
<<<<<<< HEAD
	G = game.game()
	pygame.init()
	win = pygame.display.set_mode((1000, 500))
	pygame.display.set_caption("Example Run")
	win.fill((0, 0, 0))
	for i in range(20):
		for j in range(10):
			pygame.draw.circle(win, (255,255,255), (50*i+25, 50*j+25), 20, 5)
	pygame.draw.circle(win, (255,0,0), ((G.X.position%20)*50+25, (G.X.position//20)*50+25), 15, 15)
	for t in range(4):
		pygame.draw.circle(win, (255,255,0), ((G.detectives[t].position%20)*50+25, (G.detectives[t].position//20)*50+25), 15, 15)
	pygame.display.update()
	type = ["detective","x"]
	hide_move = [3,6,9]
	multi_move = []
	print("\n ################### START GAME ########################################")
	print(G.M)
	pygame.time.delay(1000)
	while(not G.finish()):
		win.fill((0, 0, 0))
		move_no = G.move
		print("List of actions ", G.X.list_actions(G.board,G.detectives))
		print("\nMove No", move_no + 1, "Start -------------------------------------------------------------- \n")
		if(move_no in hide_move):
			(_,rew,_,_)=G.take_action(None,type[1],[4],0,"random")
			print('\n')
		elif(move_no in multi_move):
			print("Multi Move")
			(_,rew,_,_)=G.take_action(None,type[1],[3],0,"random")
			print('\n')
		else:
			(_,rew,_,_)=G.take_action(None,type[1],[],0,"random")
			print("\n")
		for i in range(0,4):
			print("Detective ", i, "taking action .. ")
			if(G.end_flag):
				continue
			(_,rew,_,_)=G.take_action(None,type[0],[],i,"random")
			print("\n")
		G.update_fv()
		print(G.f_x_action((2,24)).shape)
		G.print_pos()
		G.print_reward()
		for i in range(20):
			for j in range(10):
				pygame.draw.circle(win, (255,255,255), (50*i+25, 50*j+25), 20, 5)
		pygame.draw.circle(win, (255,0,0), ((G.X.position%20)*50+25, (G.X.position//20)*50+25), 15, 15)
		for t in range(4):
			pygame.draw.circle(win, (255,255,0), ((G.detectives[t].position%20)*50+25, (G.detectives[t].position//20)*50+25), 15, 15)
		pygame.time.delay(1000)
		pygame.display.update()
		if(move_no >= 19):
			victory+=1
		print("\nMove No" ,move_no+1, "Over -------------------------------------------------------------- \n")
		reward_x.append(G.X_reward)
	for i in range(20):
		for j in range(10):
			pygame.draw.circle(win, (255,255,255), (50*i+25, 50*j+25), 20, 5)
	pygame.draw.circle(win, (255,0,0), ((G.X.position%20)*50+25, (G.X.position//20)*50+25), 15, 15)
	for t in range(4):
		pygame.draw.circle(win, (255,255,0), ((G.detectives[t].position%20)*50+25, (G.detectives[t].position//20)*50+25), 15, 15)
	pygame.display.update()
	pygame.time.delay(1000)
	win.fill((0, 0, 0))
	font = pygame.font.Font('freesansbold.ttf', 64)
	if G.move>=19:
		text = font.render('X Won', True, (0,255,0),(0,0,128))
	else:
		text = font.render('Detectives Won', True, (0,255,0),(0,0,128))
	textRect = text.get_rect()
	textRect.center = (500, 250)
	win.blit(text, textRect)
	pygame.display.update()
	pygame.time.delay(5000)
	pygame.quit()
=======
	G = game.game()
	pygame.init()
	win = pygame.display.set_mode((1000, 500))
	pygame.display.set_caption("Scotland Yard")
	win.fill((0, 0, 0))
	for i in range(20):
		for j in range(10):
			pygame.draw.circle(win, (255,255,255), (50*i+25, 50*j+25), 20, 5)
	pygame.draw.circle(win, (255,0,0), ((G.X.position%20)*50+25, (G.X.position//20)*50+25), 15, 15)
	for t in range(4):
		pygame.draw.circle(win, (255,255,0), ((G.detectives[t].position%20)*50+25, (G.detectives[t].position//20)*50+25), 15, 15)
	pygame.display.update()
	type = ["detective","x"]
	hide_move = [3,6,9]
	multi_move = []
	print("\n ################### START GAME ########################################")
	print(G.M)
	pygame.time.delay(1000)
	while(not G.finish()):
		win.fill((0, 0, 0))
		move_no = G.move
		print("List of actions ", G.X.list_actions(G.board,G.detectives))
		print("\nMove No", move_no + 1, "Start -------------------------------------------------------------- \n")
		if(move_no in hide_move):
			(_,rew,_,_)=G.take_action(None,type[1],[4],0,"random")
			print('\n')
		elif(move_no in multi_move):
			print("Multi Move")
			(_,rew,_,_)=G.take_action(None,type[1],[3],0,"random")
			print('\n')
		else:
			(_,rew,_,_)=G.take_action(None,type[1],[],0,"random")
			print("\n")
		for i in range(0,4):
			print("Detective ", i, "taking action .. ")
			if(G.end_flag):
				continue
			(_,rew,_,_)=G.take_action(None,type[0],[],i,"random")
			print("\n")
		G.update_fv()
		print(G.f_x_action((2,24)).shape)
		G.print_pos()
		G.print_reward()
		for i in range(20):
			for j in range(10):
				pygame.draw.circle(win, (255,255,255), (50*i+25, 50*j+25), 20, 5)
		pygame.draw.circle(win, (255,0,0), ((G.X.position%20)*50+25, (G.X.position//20)*50+25), 15, 15)
		for t in range(4):
			pygame.draw.circle(win, (255,255,0), ((G.detectives[t].position%20)*50+25, (G.detectives[t].position//20)*50+25), 15, 15)
		pygame.time.delay(1000)
		pygame.display.update()
		if(move_no >= 19):
			victory+=1
		print("\nMove No" ,move_no+1, "Over -------------------------------------------------------------- \n")
		reward_x.append(G.X_reward)
	for i in range(20):
		for j in range(10):
			pygame.draw.circle(win, (255,255,255), (50*i+25, 50*j+25), 20, 5)
	pygame.draw.circle(win, (255,0,0), ((G.X.position%20)*50+25, (G.X.position//20)*50+25), 15, 15)
	for t in range(4):
		pygame.draw.circle(win, (255,255,0), ((G.detectives[t].position%20)*50+25, (G.detectives[t].position//20)*50+25), 15, 15)
	pygame.display.update()
	pygame.time.delay(1000)
	win.fill((0, 0, 0))
	font = pygame.font.Font('freesansbold.ttf', 64)
	if G.move>=19:
		text = font.render('X Won', True, (0,255,0),(0,0,128))
	else:
		text = font.render('Detectives Won', True, (0,255,0),(0,0,128))
	textRect = text.get_rect()
	textRect.center = (500, 250)
	win.blit(text, textRect)
	pygame.display.update()
	pygame.time.delay(5000)
	pygame.quit()
>>>>>>> 81887f4973da2a033068c8c9b90ed9ca89007ce7

print(victory,np.mean(reward_x))
plt.plot(reward_x)
plt.xlabel("Run")
plt.ylabel("Reward for X")
# plt.title("Reward for X with Random Policies")
y_axis = [x for x in range(-40,40,5)]
x_axis = [x for x in range(1,21)]
plt.yticks(y_axis)
plt.xticks(x_axis)
plt.savefig("Result.png")
