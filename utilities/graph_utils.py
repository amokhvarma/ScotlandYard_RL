import pandas as pd
import networkx as nx
import numpy as np
import random

class graph:

    # Read the csv files and make graph here
    def __init__(self):
        # numbered 1 to 199
        G = nx.MultiGraph()
        # List of empty positions
        self.list_of_positions = [13,26,29,34,50,53,91,94,103,112,117,132,138,141,155,174,197,198]

    # Return all connections of a node.
    def connections(self,node):
        '''
        For each node,
            return arr with 0,1,2 as Taxi, Bus, Underground
            arr[0] = array/list of nodes (node numbers) connected to given node via given mode of Taxi
        '''

        return None

    # Number of agents to initialise (including the detective)
    def initial_pos(self,n):
        return random.sample(self.list_of_positions,n)

    # networkx has inbuilt function for shortest path
    def shortest_path(self,start,target):
        return 0