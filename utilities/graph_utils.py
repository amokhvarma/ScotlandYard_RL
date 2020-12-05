import pandas as pd
import networkx as nx
import numpy as np
import random
import os
class graph:

    # Read the csv files and make graph here
    def __init__(self):
        # numbered 1 to 199
        path = os.getcwd()+"/utilities/"
        taxi = pd.read_csv(path+'taxi.csv')
        bus = pd.read_csv(path+'bus.csv')
        underground = pd.read_csv(path+'underground.csv')
        G = nx.MultiGraph()
        G.add_nodes_from( range(1,200) )
        for i in range(len(taxi)):
            G.add_edge( taxi['Node1'][i] , taxi['Node2'][i] , type = 'taxi' , color = 'yellow' )
        for i in range(len(bus)):
            G.add_edge( bus['Node1'][i] , bus['Node2'][i] , type = 'bus' , color = 'blue' )
        for i in range(len(underground)):
            G.add_edge( underground['Node1'][i] , underground['Node2'][i] , type = 'underground' , color = 'red' )
        # List of empty positions
        self.list_of_positions = [13,26,29,34,50,53,91,94,103,112,117,132,138,141,155,174,197,198]
        self.G=G
    # Return all connections of a node.
    def connections(self,node):
        '''
        For each node,
            return arr with 0,1,2 as Taxi, Bus, Underground
            arr[0] = array/list of nodes (node numbers) connected to given node via given mode of Taxi
        '''
        l1=[]
        l2=[]
        l3=[]
        d=self.G.__getitem__(node)
        for i in d:
            for j in d[i]:
                if d[i][j]['type']=='taxi':
                    l1.append(i)
                if d[i][j]['type']=='bus':
                    l2.append(i)
                if d[i][j]['type']=='underground':
                    l3.append(i)
        l=[l1,l2,l3]
        return l

    # Number of agents to initialise (including the detective)
    def initial_pos(self,n):
        return random.sample(self.list_of_positions,n)

    # networkx has inbuilt function for shortest path
    def shortest_path(self,start,target):
        print("Shortest path ",nx.shortest_path(self.G,start,target))
        return nx.shortest_path_length(self.G,start,target)
