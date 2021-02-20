import networkx as nx
import numpy as np
import sys
import time
import ant
import multiprocessing as mp
import matplotlib.pyplot as plt

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap

def PlotGraph(G:nx.DiGraph, pos:dict, i):
    colors = []
    edge_labels = nx.get_edge_attributes(G,'weight')
    edge_labels_t = nx.get_edge_attributes(G,'trail')
    for k in edge_labels.keys():
        edge_labels[k] = round(edge_labels[k], 2)
        colors.append(edge_labels_t[k])
    
    
    nx.draw(G, pos, node_color='#A0CBE2', edgelist = edge_labels.keys(), edge_color=colors, width=4, edge_cmap=plt.cm.Blues, with_labels=False)
    node_labels = nx.get_node_attributes(G,'name')
    nx.draw_networkx_labels(G, pos, labels = node_labels)

    plt.savefig("figs/f_{:04d}".format(i))
    plt.clf()

class Environment(object):
    '''
    Environment Class : Contains the environment for the ants 
    params:
        input_file : str        -> Number of Ants in the colony
        Q : float               -> Ant trail regularizator 
        p : float [0,1]         -> Ant trail persistense 
        initial_trail : float   -> Initial trail over all the edges
    '''

    def __init__(self, inputfile:str, Q = 1, p=0.8, initial_trail = 0.1):
        self.inputfile = inputfile
        self.G = nx.DiGraph()
        self.Q = Q
        self.p = p
        self.TargetNode = 0
        self.initial_trail = initial_trail
        self.readGraph()

    def readGraph(self):
        '''
        Read the input graph
        '''
        fileptr = open(self.inputfile, 'r')
        arr = np.loadtxt(fileptr.readlines(), dtype=np.int)
        node_list = []
        for src,dst,w in arr:
            if not (src in node_list): 
                self.G.add_node(src, name=src)
                node_list.append(src)
            
            if not (dst in node_list):
                self.G.add_node(dst, name=dst)
                node_list.append(dst)

            self.G.add_edge(src, dst, weight=w, trail=self.initial_trail)
        fileptr.close()

        self.TargetNode = np.max(node_list)

    def normFactor(self, u, alfa, beta, tabu):
        '''
        Calculates the normalization factor:
            u : int       -> Current vertex 
            alpha: float  -> Trail Visibility 
            beta : float  -> Weight Visibility 
            tabu : list   -> List of visited edges
        returns:
            s: float -> norm factor
        '''
        s = 0
        for k in list(self.G.neighbors(u)):
            if not(k in tabu):
                t_uk = self.G[u][k]['trail']
                n_uk = self.G[u][k]['weight']
                s += np.power(t_uk, alfa) * np.power(n_uk, beta)

        return s

    def edgeProbability(self, u, v, alfa, beta, tabu):
        '''
        Calculates the normalization factor:
            u : int       -> Current vertex 
            u : int       -> Dest    vertex 
            alpha: float  -> Trail Visibility 
            beta : float  -> Weight Visibility 
            tabu : list   -> List of visited edges
        return:
            P: float    -> Probability to choose the edge [u,v]
        '''
        if v in tabu: #Already Visited
            return 0

        t_uv = self.G[u][v]['trail']
        n_uv = self.G[u][v]['weight'] # Visibility: originaly 1/weight
        P = (np.power(t_uv, alfa) * np.power(n_uv, beta))

        return P

    def UpdateTrail(self, colony):
        '''
        Updates the trails over the graph:
            colony : list of ants -> All ants in the colony
        '''
        for u,v in self.G.edges(): #Trail persistence
            self.G[u][v]['trail'] = self.p * self.G[u][v]['trail']
            print 


        for ant in colony:
            if ant.valid:
                L = ant.total_dist
                deltT = L/self.Q # istead of Q/L

                # Add trail in edges
                for u,v in ant.solution:
                    self.G[u][v]['trail'] = self.G[u][v]['trail'] + deltT
            else:
                pass

#test
def main():
    E = Environment("datasets/graph0.txt")
    G = E.G
    for n in G.nodes():
        print(list(G.neighbors(n)))
    
    for e in G.edges():
        u,v = e
        G[u][v]['trail'] = 1

    print(G.edges(data=True))

    pass

if __name__ == '__main__':
    main()
