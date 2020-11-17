from utilities import MrX,detective,observation,graph_utils
import game

# Start the run
G = game.game()
type = ["detective","x"]
hide_move = [3,6,9]
multi_move = [2,7]
print("\n ################### START GAME ########################################")
while(not G.finish()):
    move_no = G.move
    print("\nMove No", move_no + 1, "Start -------------------------------------------------------------- \n")
    if(move_no in hide_move):
        G.take_action(None,type[1],[4],0,"random")
        print('\n')
    elif(move_no in multi_move):
        print("Multi Move")
        G.take_action(None,type[1],[3],0,"random")
        print('\n')
    else:
        G.take_action(None,type[1],[],0,"random")
        print("\n")
    for i in range(0,4):
        print("Detective ", i, "taking action .. ")
        G.take_action(None,type[0],[],i,"random")
        print("\n")
    G.print_pos()
    print("\nMove No" ,move_no+1, "Over -------------------------------------------------------------- \n")